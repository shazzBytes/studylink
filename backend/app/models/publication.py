import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.publication_member import PublicationMember
    from app.models.researcher import ResearcherInfo

class PublicationRole(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class Publication(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    researcher_id: uuid.UUID = Field(
        foreign_key="researcherinfo.id",
        index=True,
    )

    # Core publication info
    title: str
    publisher: str
    year: int | None = None
    description: str | None = None

    domains: list[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Relationships
    researcher: Optional["ResearcherInfo"] = Relationship(back_populates="publications")
    members: list["PublicationMember"] = Relationship(back_populates="publication")
