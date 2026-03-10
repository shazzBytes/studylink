import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class CreateChat(SQLModel):
    title: str | None = None
    participants: list[str] = Field(default_factory=list)


class UpdateChat(SQLModel):
    title: str | None = None
    participants: list[str] | None = None
    last_message: str | None = None


class ChatPublic(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str | None = None
    participants: list[str] = Field(default_factory=list)
    last_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ChatsPublic(SQLModel):
    data: list[ChatPublic]
    count: int
