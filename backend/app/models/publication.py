import uuid
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from datetime import datetime

if TYPE_CHECKING:
    from app.models.researcher import ResearcherInfo
    from app.models.publication_member import PublicationMember

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

    title: str
    publisher: str
    year: Optional[int] = None
    description: Optional[str] = None

    # Domains / research areas
    domains: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    # 🔒 Soft delete fields
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = None

    # Relationships
    researcher: Optional["ResearcherInfo"] = Relationship(back_populates="publications")
    members: List["PublicationMember"] = Relationship(back_populates="publication")

