import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.users import User


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    title: str | None = None
    participants: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    last_message: str | None = None
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime | None = None
    is_deleted: bool = Field(default=False, index=True)

    owner: "User" = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
