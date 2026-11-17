from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import engine
from app.database.models import Base, Document

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG System",
    description="Document Retrieval and Question Answering System",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

