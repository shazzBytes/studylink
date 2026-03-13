import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.researcher import ResearcherInfo


class ResearcherCollaborator(SQLModel, table=True):
    researcher_id: uuid.UUID = Field(
        foreign_key="researcherinfo.id",
        primary_key=True,
    )
    collaborator_id: uuid.UUID = Field(
        foreign_key="researcherinfo.id",
        primary_key=True,
    )

    added_by: uuid.UUID | None = Field(
        default=None,
        foreign_key="user.id",
    )
    added_at: datetime = Field(default_factory=datetime.utcnow)

    researcher: Optional["ResearcherInfo"] = Relationship(
        back_populates="collaborator_links",
        sa_relationship_kwargs={"foreign_keys": "[ResearcherCollaborator.researcher_id]"},
    )
    collaborator: Optional["ResearcherInfo"] = Relationship(
        back_populates="collaborator_of_links",
        sa_relationship_kwargs={"foreign_keys": "[ResearcherCollaborator.collaborator_id]"},
    )
