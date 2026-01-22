from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User

# classify it into a dm, gc, mentorship or research group
class ConversationType(IntEnum):
    DIRECT = 1
    GROUP = 2
    MENTORSHIP = 3
    RESEARCH = 4

class ConversationStatus(IntEnum):
    ACTIVE = 1
    ARCHIVED = 2
    MUTED = 3

class MemberStatus(IntEnum):
    ACTIVE = 1
    LEFT = 2
    REMOVED = 3

class MessageStatus(IntEnum):
    SENT = 1
    DELIVERED = 2
    READ = 3
    DELETED = 4


# Base class for timestamp fields (DRY principle)
class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Chat Room model
class Room(TimestampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: int = Field(index=True)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    created_by: uuid.UUID = Field(foreign_key="users.id", index=True)
    status: int = Field(default=ConversationStatus.ACTIVE)
    is_archived: bool = Field(default=False, index=True)
    last_message_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Relationships
    members: list["RoomMember"] = Relationship(back_populates="room", cascade_delete=True)
    messages: list["Message"] = Relationship(back_populates="room", cascade_delete=True)
    admins: list["RoomAdmin"] = Relationship(back_populates="room", cascade_delete=True)


# Room Members model
class RoomMember(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="room.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    status: int = Field(default=MemberStatus.ACTIVE)
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    left_at: datetime | None = Field(default=None)
    last_read_at: datetime | None = Field(default=None)
    is_muted: bool = Field(default=False)
    
    # Relationships
    room: Room = Relationship(back_populates="members")


# Room Admins model
class RoomAdmin(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="room.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: uuid.UUID | None = Field(foreign_key="users.id", default=None)
    
    # Relationships
    room: Room = Relationship(back_populates="admins")


# Message model
class Message(TimestampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="room.id", index=True)
    sender_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    content: str = Field(max_length=4000)
    status: int = Field(default=MessageStatus.SENT)
    is_edited: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    reply_to_id: uuid.UUID | None = Field(foreign_key="message.id", default=None)
    
    # Relationships
    room: Room = Relationship(back_populates="messages")
    reactions: list["MessageReaction"] = Relationship(back_populates="message", cascade_delete=True)
    attachments: list["MessageAttachment"] = Relationship(back_populates="message", cascade_delete=True)


# Message Reactions model
class MessageReaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    message_id: uuid.UUID = Field(foreign_key="message.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    emoji: str = Field(max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    message: Message = Relationship(back_populates="reactions")


# Message Attachments model
class MessageAttachment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    message_id: uuid.UUID = Field(foreign_key="message.id", index=True)
    file_name: str = Field(max_length=255)
    file_url: str = Field(max_length=1000)
    file_type: str = Field(max_length=100)
    file_size: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    message: Message = Relationship(back_populates="attachments")