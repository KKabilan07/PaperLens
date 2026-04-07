from fastapi import APIRouter

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