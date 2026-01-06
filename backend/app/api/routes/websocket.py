"""WebSocket endpoints for real-time messaging."""

import uuid
import json
from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.core.websocket_manager import manager
from app.models.users import User
from app.models.chats import Room, Message, RoomMembers
from app.schemas.chat import WSMessage, WSTypingIndicator

router = APIRouter()


async def get_ws_current_user(
    websocket: WebSocket,
    token: str = Query(...),
    session: Session = Depends(get_db),
) -> User:
    """Authenticate WebSocket connection using token query parameter."""
    from app.core.security import decode_access_token
    from fastapi import HTTPException
    
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = session.get(User, uuid.UUID(user_id))
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise


@router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    session: Session = Depends(get_db),
):
    """
    WebSocket endpoint for real-time chat in a specific room.
    
    Connection: ws://localhost:8000/api/v1/ws/chat/{room_id}?token={jwt_token}
    """
    # Authenticate user
    try:
        from app.core.security import decode_access_token
        
        payload = decode_access_token(token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        user_id = uuid.UUID(user_id_str)
        user = session.get(User, user_id)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Verify user is a member of the room
    room_uuid = uuid.UUID(room_id)
    room = session.get(Room, room_uuid)
    if not room:
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        return

    membership = session.exec(
        select(RoomMembers).where(
            RoomMembers.room_id == room_uuid,
            RoomMembers.sender_id == user_id
        )
    ).first()

    if not membership:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Connect to room
    await manager.connect(websocket, room_id, user_id)
    
    # Notify room that user joined
    await manager.broadcast_to_room(
        {
            "type": "user_joined",
            "room_id": room_id,
            "user_id": str(user_id),
            "user_email": user.email,
        },
        room_id,
        exclude=websocket
    )

    try:
        while True:
            # Receive message from WebSocket
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type", "message")
            
            if message_type == "message":
                # Save message to database
                content = message_data.get("content", "")
                if content.strip():
                    db_message = Message(
                        room_id=room_uuid,
                        sender_id=user_id,
                        content=content
                    )
                    session.add(db_message)
                    
                    # Update room's last message timestamp
                    room.last_message_at = db_message.timestamp
                    session.add(room)
                    
                    session.commit()
                    session.refresh(db_message)
                    
                    # Broadcast to all users in the room
                    await manager.broadcast_to_room(
                        {
                            "type": "message",
                            "message_id": str(db_message.id),
                            "room_id": room_id,
                            "sender_id": str(user_id),
                            "sender_email": user.email,
                            "content": content,
                            "timestamp": db_message.timestamp.isoformat(),
                        },
                        room_id
                    )
            
            elif message_type == "typing":
                # Broadcast typing indicator (don't save to DB)
                is_typing = message_data.get("is_typing", False)
                await manager.broadcast_to_room(
                    {
                        "type": "typing",
                        "room_id": room_id,
                        "sender_id": str(user_id),
                        "sender_email": user.email,
                        "is_typing": is_typing,
                    },
                    room_id,
                    exclude=websocket
                )
            
            elif message_type == "read":
                # Mark messages as read (implement read receipts)
                message_ids = message_data.get("message_ids", [])
                await manager.broadcast_to_room(
                    {
                        "type": "read",
                        "room_id": room_id,
                        "user_id": str(user_id),
                        "message_ids": message_ids,
                    },
                    room_id,
                    exclude=websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        # Notify room that user left
        await manager.broadcast_to_room(
            {
                "type": "user_left",
                "room_id": room_id,
                "user_id": str(user_id),
                "user_email": user.email,
            },
            room_id
        )
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, room_id)


@router.get("/rooms/{room_id}/online-users")
async def get_online_users(
    room_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Get count of online users in a room."""
    count = manager.get_room_connection_count(room_id)
    return {
        "room_id": room_id,
        "online_count": count
    }
