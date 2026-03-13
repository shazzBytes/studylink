from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    domain: str = Field(index=True, unique=True, max_length=255)

    owner_id: UUID = Field(foreign_key="user.id", index=True, nullable=False)

    is_public: bool = False

    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = None

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
        )
    )
