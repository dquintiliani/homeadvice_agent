# db_setup.py (you can also put this at the top of your current file)

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    print("get_db created session:", db)  # debug
    try:
        yield db
    finally:
        db.close()