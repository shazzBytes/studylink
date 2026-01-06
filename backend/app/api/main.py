from fastapi import APIRouter

from app.api.routes import items, login, private, researcher, users, utils, messages, websocket
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(researcher.router)
api_router.include_router(messages.router, prefix="/chat", tags=["chat"])
api_router.include_router(websocket.router, tags=["websocket"])


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

