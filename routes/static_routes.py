from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config.config import STATIC_FOLDER_PATH

def register_static_routes(app: FastAPI):
    # Monta la carpeta de archivos estáticos
    STATIC_FOLDER_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATIC_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=STATIC_FOLDER_PATH), name="static")

    # Ruta para servir el index.html
    @app.get("/")
    async def serve_root():
        return FileResponse(STATIC_FOLDER_PATH / "index.html")

    # Ruta catch-all para manejar el frontend
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse(STATIC_FOLDER_PATH / "index.html")
