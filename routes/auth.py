# backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Body
from datetime import timedelta
from sqlalchemy.orm import Session
from services.auth_service import create_access_token, verify_token
from models.user import User, Token
from database.models.Users.users import User as DatabaseUser
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from database.models.Users import users_database_handler as database
from database.database_conection import GetDbInstance
from utils.security import verify_password

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(username: str = Body(...), password: str = Body(...), db: Session = Depends(GetDbInstance)):
    
    print('USERNAME', username)
    print('PASSWORD',password)
    database_user = database.SelectByUserName(db, DatabaseUser, username)
    if not database_user:
        print("Invalid username")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    isCorrect = verify_password(password, database_user.password)
    if not isCorrect:
        print("Invalid password")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    login_user = User(username=username, role="admin")  # Asigna roles según corresponda
    access_token = create_access_token(
        data={"sub": login_user.username, "role": login_user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route", dependencies=[Depends(verify_token)])
async def protected_route(token: str = Depends(verify_token)):
    if token and token.get("role") == "admin":
        return {"message": "Este es un contenido solo para administradores"}
    raise HTTPException(status_code=403, detail="No tienes acceso")
