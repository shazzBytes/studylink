from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from enum import IntEnum

# classify it into a dm, gc, mentorship or research group
class ConversationType(IntEnum):
    DIRECT = 1
    GROUP = 2
    MENTORSHIP = 3
    RESEARCH = 4


# Chat model
class Room(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: int
    name: str | None = Field(default=None, max_length=255)
    created_by: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_archived: bool = Field(default=False)
    last_message_at: datetime = Field(default_factory=datetime.utcnow)
    content: str | None = None

# Chat Members model
class RoomMembers(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="rooms.id")
    sender_id: uuid.UUID = Field(foreign_key="users.id")
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="rooms.id")
    sender_id: uuid.UUID = Field(foreign_key="users.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)