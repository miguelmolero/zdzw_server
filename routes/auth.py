# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from services.auth_service import create_access_token, verify_token
from models.user import User, Token
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(username: str, password: str):
    # Aquí deberías validar el usuario contra tu base de datos
    # y validar contraseña. Este es solo un ejemplo simplificado.
    user = User(username=username, role="user")  # Asigna roles según corresponda
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route", dependencies=[Depends(verify_token)])
async def protected_route(token: str = Depends(verify_token)):
    if token and token.get("role") == "admin":
        return {"message": "Este es un contenido solo para administradores"}
    raise HTTPException(status_code=403, detail="No tienes acceso")
