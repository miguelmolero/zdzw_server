from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import jwt, JWTError
from config.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=403, detail="Token inválido o no autorizado")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido o no autorizado")
