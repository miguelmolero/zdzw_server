from fastapi import FastAPI
from contextlib import asynccontextmanager
from middlewares.cors_middleware import add_middlewares
from routes.static_routes import register_static_routes
from routes.auth import router as auth_router
from routes.data_visualization import router as data_visualization_router
from services.Initialize import initialize
from dotenv import load_dotenv
import sys
import os

load_dotenv()
is_pyinstaller = hasattr(sys, '_MEIPASS')
environment = os.getenv("ENVIRONMENT", "development")
if is_pyinstaller or environment == "production":
    print("Running in production mode")
    port = 4000
else:
    print("Running in development mode")
    port = int(os.getenv("PORT", 8000))

# Initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
add_middlewares(app)

# Register authentication routes
app.include_router(auth_router)
app.include_router(data_visualization_router)

#Register static routes
register_static_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=port)

