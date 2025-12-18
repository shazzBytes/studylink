from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    title: str
    description: str | None = None
    domain: str = Field(index=True, unique=True)

    owner_id: UUID = Field(foreign_key="user.id", index=True)

    is_public: bool = False

    is_deleted: bool = False
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
