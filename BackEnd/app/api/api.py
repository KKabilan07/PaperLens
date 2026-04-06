from fastapi import APIRouter
from app.api.routes import health, auth, papers, chat

router = APIRouter()

router.include_router(health.router, prefix="/health")
router.include_router(auth.router, prefix="/auth")
router.include_router(papers.router, prefix="/papers")
router.include_router(chat.router, prefix="/chat")