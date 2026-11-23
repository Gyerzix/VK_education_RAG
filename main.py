from fastapi import FastAPI

from app.api.search import router as search_router
from app.database.connection import engine
from app.database.models import Base, Document, Chunk
from app.api.ingest import router as ingest_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG System",
    description="Document Retrieval and Question Answering System",
    version="0.1.0",
)

app.include_router(ingest_router)
app.include_router(search_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
