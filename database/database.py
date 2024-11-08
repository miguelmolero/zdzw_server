# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from config.config import DATABASE_URL

# create the database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session local to perform database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crete base class for models
Base = declarative_base()

# initialize the database
def init_db():
    if not os.path.exists("./zdzw.db"):
        print("Database not found, creating...")
    Base.metadata.create_all(bind=engine)  # Crea las tablas si no existen
