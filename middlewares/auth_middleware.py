
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from services.auth_service import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Lista de rutas que no requieren autenticación
        open_routes = ["/login"]

        # Si la ruta es pública, permite el acceso sin autenticación
        if request.url.path in open_routes:
            return await call_next(request)

        # De lo contrario, verifica el token
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        
        # Elimina el prefijo "Bearer " si está presente
        token = token.replace("Bearer ", "")
        try:
            verify_token(token)  # Verifica el token usando tu función de verificación
        except HTTPException as e:
            raise HTTPException(status_code=403, detail="Invalid or expired token")

        return await call_next(request)