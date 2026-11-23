from fastapi import APIRouter

from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_engine import search_chunks
from app.database.repository import get_document_by_id


router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/", response_model=SearchResponse)
def search_documents(request: SearchRequest):

    results = search_chunks(query=request.query, top_k=request.top_k)

    return {"query": request.query, "results": results}