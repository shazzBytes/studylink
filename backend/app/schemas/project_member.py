from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel, Field


class ProjectMemberBase(SQLModel):
    user_id: UUID
    role: str = Field(
        default="viewer",
        max_length=20,
        nullable=False,)


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberPublic(SQLModel):
    user_id: UUID
    role: str
    added_at: datetime
    class Config:
        from_attributes = True


