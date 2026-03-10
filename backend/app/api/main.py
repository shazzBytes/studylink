from fastapi import APIRouter

from app.api.routes import (
    chats,
    items,
    login,
    messages,
    private,
    researcher,
    users,
    utils,
)
from app.api.routes.search import router as search_router
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(search_router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(researcher.router)
api_router.include_router(chats.router)
api_router.include_router(messages.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
