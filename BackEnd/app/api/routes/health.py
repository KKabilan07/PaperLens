from fastapi import APIRouter
from app.services.supabase_client import get_supabase

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
    Verifies database schema connectivity
    """
    try:
        supabase = get_supabase()
        response = supabase.table("sections").select("id").limit(1).execute()
        return {
            "status": "success",
            "message": "Database is ready for embeddings",
            "table_accessible": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not query sections table: {str(e)}",
            "table_accessible": False
        }