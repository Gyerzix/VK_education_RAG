import httpx

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from app.services.parser import parse_url
from app.services.chunker import split_into_chunks
from app.services.search_engine import index_chunks
from app.database.repository import create_document, create_chunks, get_document_by_url


router = APIRouter(prefix="/ingest", tags=["Ingestion"])


class IngestRequest(BaseModel):
    url: HttpUrl


class IngestResponse(BaseModel):
    id: int
    title: str
    url: str
    text: str
    created_at: datetime


@router.post("/", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """Парсит веб-страницу и сохраняет документ в БД."""

    url = str(request.url)

    existing = get_document_by_url(url)

    if existing:
        raise HTTPException(status_code=409, detail="Документ уже существует")

    try:
        parsed_document = await parse_url(url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка загрузки страницы: {e}")

    try:
        document = create_document(
            title=parsed_document["title"],
            url=parsed_document["url"],
            text=parsed_document["text"]
        )

        chunks = split_into_chunks(document.text)
        saved_chunks = create_chunks(document_id=document.id, chunks=chunks)
        index_chunks(saved_chunks)

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {
        "id": document.id,
        "title": document.title,
        "url": document.url,
        "text": document.text,
        "created_at": document.created_at
    }
