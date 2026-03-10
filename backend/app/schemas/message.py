import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class MessageCreate(SQLModel):
    content: str
    attachments: list[str] = Field(default_factory=list)


class MessageUpdate(SQLModel):
    content: str | None = None
    attachments: list[str] | None = None


class MessagePublic(SQLModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    attachments: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool = False

    class Config:
        from_attributes = True


class MessagesPublic(SQLModel):
    data: list[MessagePublic]
    count: int
