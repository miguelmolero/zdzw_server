from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config.config import DATABASE_URL

# create the database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

# Create session local to perform database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crete base class for models
Base = declarative_base()

def GetDbInstance() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()