import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.chat import Chat


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Foreign keys
    chat_id: uuid.UUID = Field(foreign_key="chat.id", index=True)
    sender_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    # Content
    content: str
    attachments: list[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Timestamps
    created_at: datetime | None = Field(default_factory=get_datetime_utc, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime | None = None

    # Soft delete
    is_deleted: bool = Field(default=False, index=True)

    # Relationships
    chat: Optional["Chat"] = Relationship(back_populates="messages")
