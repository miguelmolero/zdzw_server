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

# Verify if the script is running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Temporal folder where PyInstaller stores the files
    base_path = sys._MEIPASS
else:
    # In development mode, the base path is the current directory
    base_path = os.path.abspath(os.path.dirname(__file__))

# Route to the static folder
static_folder_path = os.path.join(base_path, 'static/dist')

# Check the static folder path
# print(f"Serving static files from: {static_folder_path}")

# Mount the static folder
app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

# Route to serve the frontend index.html
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(static_folder_path, "index.html"))

# Catch all route to serve the frontend index.html
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse(os.path.join(static_folder_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

