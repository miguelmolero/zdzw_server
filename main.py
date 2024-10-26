from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from .middlewares.cors_middleware import add_middlewares
from routes.static_routes import register_static_routes
from routes.auth import router as auth_router
from services.auth_service import verify_token 

app = FastAPI(dependencies=[Depends(verify_token)])

# Add CORS middleware
add_middlewares(app)

#Register static routes
register_static_routes(app)

# Register authentication routes
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

