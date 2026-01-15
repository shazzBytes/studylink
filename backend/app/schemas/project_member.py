from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class ProjectMemberBase(SQLModel):
    user_id: UUID
    role: str = "viewer"


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberPublic(SQLModel):
    user_id: UUID
    role: str
    added_at: datetime
