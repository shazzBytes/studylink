from uuid import UUID

from sqlmodel import Field, SQLModel


class ProjectCreate(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    domain: str = Field(max_length=255)
    is_public: bool = False

class ProjectUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    is_public: bool | None = None

class ProjectPublic(SQLModel):
    id: UUID
    title: str
    description: str | None
    domain: str
    owner_id: UUID
    is_public: bool

    class Config:
        from_attributes = True


#Might need ProjectList Item Later
