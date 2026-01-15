from typing import Optional, List
from sqlmodel import SQLModel


class CreatePublication(SQLModel):
    title: str
    publisher: str
    year: Optional[int] = None

    abstract: Optional[str] = None
    description: Optional[str] = None

    domains: List[str] = []
    keywords: List[str] = []

    publication_type: Optional[str] = None
    doi: Optional[str] = None


class UpdatePublication(SQLModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None

    abstract: Optional[str] = None
    description: Optional[str] = None

    domains: Optional[List[str]] = None
    keywords: Optional[List[str]] = None

    publication_type: Optional[str] = None
    doi: Optional[str] = None
