"""WebSocket connection manager for real-time messaging."""

import json
import uuid

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages WebSocket connections for real-time messaging."""

    def __init__(self):
        # Maps room_id to set of WebSocket connections
        self.active_connections: dict[str, set[WebSocket]] = {}
        # Maps WebSocket to user_id for tracking
        self.connection_user_map: dict[WebSocket, uuid.UUID] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: uuid.UUID):
        """Accept a new WebSocket connection and add to room."""
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()

        self.active_connections[room_id].add(websocket)
        self.connection_user_map[websocket] = user_id

    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove WebSocket connection from room."""
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        if websocket in self.connection_user_map:
            del self.connection_user_map[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to a specific WebSocket connection."""
        await websocket.send_text(message)

    async def broadcast_to_room(self, message: dict, room_id: str, exclude: WebSocket | None = None):
        """Broadcast message to all connections in a room."""
        if room_id not in self.active_connections:
            return

        message_json = json.dumps(message, default=str)

        disconnected = set()
        for connection in self.active_connections[room_id]:
            if connection == exclude:
                continue
            try:
                await connection.send_text(message_json)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection, room_id)

    def get_room_connection_count(self, room_id: str) -> int:
        """Get the number of active connections in a room."""
        return len(self.active_connections.get(room_id, set()))

    def is_user_online_in_room(self, user_id: uuid.UUID, room_id: str) -> bool:
        """Check if a user is online in a specific room."""
        if room_id not in self.active_connections:
            return False

        for connection in self.active_connections[room_id]:
            if self.connection_user_map.get(connection) == user_id:
                return True
        return False


# Global connection manager instance
manager = ConnectionManager()
