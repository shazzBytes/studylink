import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.publication import PublicationRole, Publication

class PublicationMember(SQLModel, table=True):
    publication_id: uuid.UUID = Field(
        foreign_key="publication.id",
        primary_key=True,
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        primary_key=True,
    )

    role: PublicationRole = Field(default=PublicationRole.viewer)

    # Metadata
    added_by: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="user.id",
    )
    added_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    publication: Optional["Publication"] = Relationship(back_populates="members")
