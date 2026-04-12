from fastapi import APIRouter
from app.services.embedding_storage_service import check_database_setup

router = APIRouter()


@router.get("/")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "service": "PaperLens API",
        "version": "1.0.0"
    }


@router.get("/ready")
def readiness_check():
    """
    Readiness check for Kubernetes or deployment orchestration
    """
    return {
        "ready": True,
        "service": "PaperLens API"
    }


@router.get("/embeddings")
def check_embeddings():
    """
    Check if embeddings/RAG system is properly configured
    Verifies database schema, pgvector extension, and connectivity
    """
    return check_database_setup()