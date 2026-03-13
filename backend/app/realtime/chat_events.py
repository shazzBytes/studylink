import asyncio
import uuid
from collections import defaultdict
from collections.abc import Iterable
from concurrent.futures import Future
from typing import Any

from fastapi import WebSocket


class ChatEventManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._loop: asyncio.AbstractEventLoop | None = None

    def attach_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def connect(self, *, user_id: uuid.UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[str(user_id)].add(websocket)

    def disconnect(self, *, user_id: uuid.UUID, websocket: WebSocket) -> None:
        user_key = str(user_id)
        sockets = self._connections.get(user_key)
        if not sockets:
            return
        sockets.discard(websocket)
        if not sockets:
            self._connections.pop(user_key, None)

    async def _broadcast_to_users(
        self, *, user_ids: Iterable[str], event: dict[str, Any]
    ) -> None:
        seen_users: set[str] = set()
        for user_id in user_ids:
            if user_id in seen_users:
                continue
            seen_users.add(user_id)
            for websocket in tuple(self._connections.get(user_id, ())):
                try:
                    await websocket.send_json(event)
                except Exception:
                    self.disconnect(user_id=uuid.UUID(user_id), websocket=websocket)

    def broadcast_to_users(
        self, *, user_ids: Iterable[str], event: dict[str, Any]
    ) -> Future[None] | None:
        if self._loop is None or self._loop.is_closed():
            return None
        return asyncio.run_coroutine_threadsafe(
            self._broadcast_to_users(user_ids=user_ids, event=event),
            self._loop,
        )


chat_event_manager = ChatEventManager()
