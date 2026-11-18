from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Document


def create_document(title: str, url: str, text: str) -> Document:

    with SessionLocal() as session:
        try:
            existing = session.scalar(select(Document).where(Document.url == url))

            if existing:
                raise ValueError("Документ с таким URL уже существует")

            document = Document(title=title, url=url, text=text)

            session.add(document)
            session.commit()
            session.refresh(document)

            return document

        except Exception:
            session.rollback()
            raise


def get_document_by_id(document_id: int) -> Document | None:

    with SessionLocal() as session:
        return session.get(Document, document_id)


def get_document_by_url(url: str) -> Document | None:

    with SessionLocal() as session:
        return session.scalar(select(Document).where(Document.url == url))


def get_all_documents() -> list[Document]:

    with SessionLocal() as session:
        return list(session.scalars(select(Document)).all())
