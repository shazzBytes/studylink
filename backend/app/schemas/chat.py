import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class CreateRoom(SQLModel):
    type: int
    name: str | None = Field(default=None, max_length=255)
    created_by: uuid.UUID
    description: str | None = None


class UpdateRoom(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    is_archived: bool | None = None


class RoomPublic(SQLModel):
    id: uuid.UUID
    type: int
    name: str | None
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    last_message_at: datetime


class MessageCreate(SQLModel):
    room_id: uuid.UUID
    content: str


class MessageUpdate(SQLModel):
    content: str


class MessagePublic(SQLModel):
    id: uuid.UUID
    room_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    timestamp: datetime


class MessagesPublic(SQLModel):
    data: list[MessagePublic]
    count: int


class RoomMemberCreate(SQLModel):
    room_id: uuid.UUID
    sender_id: uuid.UUID


# WebSocket message types
class WSMessageType(BaseModel):
    type: str  # 'message', 'typing', 'read', 'user_joined', 'user_left'
    

class WSMessage(BaseModel):
    type: str = "message"
    room_id: str
    sender_id: str
    content: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_id: str | None = None


class WSTypingIndicator(BaseModel):
    type: str = "typing"
    room_id: str
    sender_id: str
    is_typing: bool


class WSUserStatus(BaseModel):
    type: str
    room_id: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

