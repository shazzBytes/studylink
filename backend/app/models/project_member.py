from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class ProjectMember(SQLModel, table=True):
    project_id: UUID = Field(
        foreign_key="project.id",
        primary_key=True,
        index=True,
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True,
        index=True,
    )

    role: str = Field(
        default="viewer",
        max_length=20,
        nullable=False,
        index=True
    )

    added_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
