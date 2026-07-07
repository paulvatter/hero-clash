import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DEFAULT_DB_FILE = Path(__file__).resolve().parent / "data" / "hero_clash.db"
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DEFAULT_DB_FILE.as_posix()}"

if DATABASE_URL.startswith("sqlite://"):
    db_path = DEFAULT_DB_FILE
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite:") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
