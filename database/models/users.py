# database/models/users.py
from sqlalchemy import Column, Integer, String
from database.database import Base  # import base model

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    password = Column(String, unique=True)
