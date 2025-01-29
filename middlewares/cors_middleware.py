from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config.config import CORS_ORIGINS

def add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
