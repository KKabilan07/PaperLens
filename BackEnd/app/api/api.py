from fastapi import APIRouter
from app.api.routes import health, auth, papers, chat, dashboard, search

router = APIRouter(prefix="/api/v1")

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(papers.router, prefix="/papers", tags=["papers"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(search.router, prefix="/search", tags=["search"])