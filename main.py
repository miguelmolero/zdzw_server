from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .middlewares.cors_middleware import add_middlewares
from routes.static_routes import register_static_routes 

app = FastAPI()

# Add CORS middleware
add_middlewares(app)

#Register static routes
register_static_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

