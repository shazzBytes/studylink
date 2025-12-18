from uuid import UUID
from sqlmodel import SQLModel

class ProjectCreate(SQLModel):
    title: str
    description: str | None = None
    domain: str
    is_public: bool = False


class ProjectUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    is_public: bool | None = None

class ProjectPublic(SQLModel):
    id: UUID
    title: str
    description: str | None
    domain: str
    owner_id: UUID
    is_public: bool
