from typing import Optional, List
from sqlmodel import SQLModel


class CreateResearcherInfo(SQLModel):
    full_name: str
    email: str
    qualification: str
    institute: Optional[str] = None
    bio: Optional[str] = None

    research_interests: List[str] = []
    expertise_keywords: List[str] = []

    orcid: Optional[str] = None
    is_public: bool = True


class UpdateResearcherInfo(SQLModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    qualification: Optional[str] = None
    institute: Optional[str] = None
    bio: Optional[str] = None

    research_interests: Optional[List[str]] = None
    expertise_keywords: Optional[List[str]] = None

    orcid: Optional[str] = None
    is_public: Optional[bool] = None
