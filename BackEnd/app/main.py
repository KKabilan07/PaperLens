from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import router

app = FastAPI(
    title="PaperLens API",
    description="Backend API for PaperLens - AI-powered paper analysis and collaboration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {
        "message": "PaperLens API running",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/api/v1")
def api_root():
    """
    API v1 root
    """
    return {
        "message": "PaperLens API v1",
        "endpoints": {
            "papers": "/papers",
            "chat": "/chat",
            "auth": "/auth",
            "health": "/health"
        }
    }