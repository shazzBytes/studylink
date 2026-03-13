import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.collaborator import ResearcherCollaborator
    from app.models.publication import Publication


class ResearcherInfo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Core identity
    full_name: str
    email: str = Field(index=True, unique=True)
    qualification: str
    institute: str | None = None
    bio: str | None = None

    # Relationships
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
