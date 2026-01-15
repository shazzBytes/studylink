from typing import Optional, List
from sqlmodel import SQLModel


class CreatePublication(SQLModel):
    title: str
    publisher: str
    year: Optional[int] = None
    description: Optional[str] = None
    domains: List[str] = []


class UpdatePublication(SQLModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    domains: Optional[List[str]] = None
