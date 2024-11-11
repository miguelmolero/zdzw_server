import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

# create the database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session local to perform database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crete base class for models
Base = declarative_base()