from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from ..config import CORS_ORIGINS

def add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
