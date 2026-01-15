import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

if TYPE_CHECKING:
    from app.models.publication import Publication
    from app.models.collaborator import ResearcherCollaborator


class ResearcherInfo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Core identity
    full_name: str
    email: str = Field(index=True, unique=True)
    qualification: str
    institute: Optional[str] = None
    bio: Optional[str] = None

    # 🔍 Search & discovery fields
    research_interests: List[str] = Field(default_factory=list)
    expertise_keywords: List[str] = Field(default_factory=list)

    # Academic identity
    orcid: Optional[str] = Field(default=None, index=True)

    # Visibility & soft delete
    is_public: bool = Field(default=True, index=True)
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = None

    # Relationships
    publications: List["Publication"] = Relationship(back_populates="researcher")

    collaborator_links: List["ResearcherCollaborator"] = Relationship(
        back_populates="researcher",
        sa_relationship_kwargs={
            "foreign_keys": "[ResearcherCollaborator.researcher_id]"
        },
    )
    collaborator_of_links: List["ResearcherCollaborator"] = Relationship(
        back_populates="collaborator",
        sa_relationship_kwargs={
            "foreign_keys": "[ResearcherCollaborator.collaborator_id]"
        },
    )
