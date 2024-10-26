# backend/models/user.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    role: str  # Ej. "admin", "user"

class Token(BaseModel):
    access_token: str
    token_type: str
