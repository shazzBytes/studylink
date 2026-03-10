
from sqlmodel import SQLModel


class CreateResearcherInfo(SQLModel):
    full_name: str
    email: str
    qualification: str
    institute: str | None = None
    bio: str | None = None


class UpdateResearcherInfo(SQLModel):
    full_name: str | None = None
    email: str | None = None
    qualification: str | None = None
    institute: str | None = None
    bio: str | None = None
