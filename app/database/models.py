# Сохранение документов в БД с полями title, url, text, дата.

from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)

    chunk_index: Mapped[int] = mapped_column(nullable=False)