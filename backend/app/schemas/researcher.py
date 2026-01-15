from typing import Optional
from sqlmodel import SQLModel


class CreateResearcherInfo(SQLModel):
    full_name: str
    email: str
    qualification: str
    institute: Optional[str] = None
    bio: Optional[str] = None


class UpdateResearcherInfo(SQLModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    qualification: Optional[str] = None
    institute: Optional[str] = None
    bio: Optional[str] = None
