from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "data" / "rag.db"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


engine = create_engine(url=f"sqlite:///{DATABASE_PATH.as_posix()}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

