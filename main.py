import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verificar si el script está empaquetado por PyInstaller
if getattr(sys, 'frozen', False):
    # Carpeta temporal donde PyInstaller descomprime los archivos
    base_path = sys._MEIPASS
else:
    # En desarrollo, usa la carpeta actual
    base_path = os.path.abspath(os.path.dirname(__file__))

# Ruta a los archivos estáticos (ajustado para PyInstaller)
static_folder_path = os.path.join(base_path, 'static/dist')

# Imprimir la ruta para depurar
print(f"Serving static files from: {static_folder_path}")

# Montar los archivos estáticos en FastAPI
app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

# Ruta para servir el index.html en la raíz
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(static_folder_path, "index.html"))

# Ruta catch-all para manejar otras rutas de la aplicación frontend
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse(os.path.join(static_folder_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

