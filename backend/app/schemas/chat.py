import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, field_validator


# ============ Base Schemas (DRY principle) ============

class TimestampBase(SQLModel):
    """Base class with timestamp fields"""
    created_at: datetime
    updated_at: datetime


class IDMixin(SQLModel):
    """Base class for schemas with ID field"""
    id: uuid.UUID


# ============ Room Schemas ============

class RoomBase(SQLModel):
    """Shared room properties"""
    type: int = Field(ge=1, le=4)  # ConversationType values
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class RoomCreate(RoomBase):
    """Properties to receive on room creation"""
    pass


class RoomUpdate(SQLModel):
    """Properties to receive on room update - all optional"""
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    is_archived: bool | None = None
    status: int | None = Field(default=None, ge=1, le=3)  # ConversationStatus values


class RoomPublic(RoomBase, IDMixin, TimestampBase):
    """Properties to return to client"""
    created_by: uuid.UUID
    status: int
    is_archived: bool
    last_message_at: datetime
    member_count: int | None = None
    unread_count: int | None = None


class RoomWithMembers(RoomPublic):
    """Room with member details"""
    members: list["RoomMemberPublic"]


class RoomsPublic(SQLModel):
    """Paginated rooms response"""
    data: list[RoomPublic]
    count: int


# ============ Room Member Schemas ============

class RoomMemberBase(SQLModel):
    """Shared room member properties"""
    room_id: uuid.UUID
    user_id: uuid.UUID


class RoomMemberCreate(RoomMemberBase):
    """Properties to receive on member creation"""
    pass


class RoomMemberUpdate(SQLModel):
    """Properties to receive on member update"""
    status: int | None = Field(default=None, ge=1, le=3)  # MemberStatus values
    is_muted: bool | None = None
    last_read_at: datetime | None = None


class RoomMemberPublic(RoomMemberBase, IDMixin):
    """Properties to return to client"""
    status: int
    joined_at: datetime
    left_at: datetime | None
    last_read_at: datetime | None
    is_muted: bool
    user_name: str | None = None  # Populated via join
    user_email: str | None = None  # Populated via join


class RoomMembersPublic(SQLModel):
    """Paginated room members response"""
    data: list[RoomMemberPublic]
    count: int


# ============ Room Admin Schemas ============

class RoomAdminBase(SQLModel):
    """Shared room admin properties"""
    room_id: uuid.UUID
    user_id: uuid.UUID


class RoomAdminCreate(RoomAdminBase):
    """Properties to receive on admin creation"""
    pass


class RoomAdminPublic(RoomAdminBase, IDMixin):
    """Properties to return to client"""
    assigned_at: datetime
    assigned_by: uuid.UUID | None


# ============ Message Schemas ============

class MessageBase(SQLModel):
    """Shared message properties"""
    content: str = Field(max_length=4000)


class MessageCreate(MessageBase):
    """Properties to receive on message creation"""
    room_id: uuid.UUID
    reply_to_id: uuid.UUID | None = None


class MessageUpdate(SQLModel):
    """Properties to receive on message update"""
    content: str = Field(max_length=4000)


class MessagePublic(MessageBase, IDMixin, TimestampBase):
    """Properties to return to client"""
    room_id: uuid.UUID
    sender_id: uuid.UUID
    status: int
    is_edited: bool
    is_deleted: bool
    reply_to_id: uuid.UUID | None
    sender_name: str | None = None  # Populated via join
    reaction_count: int | None = None
    attachment_count: int | None = None


class MessageWithDetails(MessagePublic):
    """Message with reactions and attachments"""
    reactions: list["MessageReactionPublic"] = []
    attachments: list["MessageAttachmentPublic"] = []
    reply_to: "MessagePublic | None" = None


class MessagesPublic(SQLModel):
    """Paginated messages response"""
    data: list[MessagePublic]
    count: int


# ============ Message Reaction Schemas ============

class MessageReactionBase(SQLModel):
    """Shared reaction properties"""
    emoji: str = Field(max_length=10)

    @field_validator('emoji')
    @classmethod
    def validate_emoji(cls, v: str) -> str:
        # Basic validation for emoji (can be enhanced)
        if not v or len(v) > 10:
            raise ValueError('Invalid emoji')
        return v


class MessageReactionCreate(MessageReactionBase):
    """Properties to receive on reaction creation"""
    message_id: uuid.UUID


class MessageReactionPublic(MessageReactionBase, IDMixin):
    """Properties to return to client"""
    message_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class MessageReactionsPublic(SQLModel):
    """Grouped reactions response"""
    data: list[MessageReactionPublic]
    count: int


# ============ Message Attachment Schemas ============

class MessageAttachmentBase(SQLModel):
    """Shared attachment properties"""
    file_name: str = Field(max_length=255)
    file_type: str = Field(max_length=100)
    file_size: int = Field(gt=0)


class MessageAttachmentCreate(MessageAttachmentBase):
    """Properties to receive on attachment creation"""
    message_id: uuid.UUID
    file_url: str = Field(max_length=1000)


class MessageAttachmentPublic(MessageAttachmentBase, IDMixin):
    """Properties to return to client"""
    message_id: uuid.UUID
    file_url: str
    created_at: datetime


# ============ WebSocket Message Schemas ============

class WSMessageBase(BaseModel):
    """Base WebSocket message"""
    type: str
    room_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WSMessage(WSMessageBase):
    """WebSocket chat message"""
    type: str = "message"
    sender_id: str
    content: str
    message_id: str | None = None
    reply_to_id: str | None = None


class WSTypingIndicator(BaseModel):
    """WebSocket typing indicator"""
    type: str = "typing"
    room_id: str
    sender_id: str
    is_typing: bool


class WSUserStatus(WSMessageBase):
    """WebSocket user status (joined/left)"""
    user_id: str


class WSMessageRead(WSMessageBase):
    """WebSocket message read receipt"""
    type: str = "read"
    user_id: str
    message_id: str


class WSMessageReaction(WSMessageBase):
    """WebSocket message reaction"""
    type: str = "reaction"
    message_id: str
    user_id: str
    emoji: str
    action: str = Field(default="add")  # "add" or "remove"


class WSError(BaseModel):
    """WebSocket error message"""
    type: str = "error"
    error: str
    details: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

