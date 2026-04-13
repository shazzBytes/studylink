import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.collaborator import ResearcherCollaborator
    from app.models.publication import Publication
    from app.models.users import User


class ResearcherInfo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)

    # Core identity
    full_name: str
    email: str = Field(index=True, unique=True)
    qualification: str
    institute: str | None = None
    department: str | None = None
    bio: str | None = None
    affiliation_verified: bool = Field(default=False, index=True)
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = None

    # Relationships
    user: Optional["User"] = Relationship()
    publications: list["Publication"] = Relationship(back_populates="researcher")

    collaborator_links: list["ResearcherCollaborator"] = Relationship(
        back_populates="researcher",
        sa_relationship_kwargs={
            "foreign_keys": "[ResearcherCollaborator.researcher_id]"
        },
    )
    collaborator_of_links: list["ResearcherCollaborator"] = Relationship(
        back_populates="collaborator",
        sa_relationship_kwargs={
            "foreign_keys": "[ResearcherCollaborator.collaborator_id]"
        },
    )
