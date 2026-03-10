import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.publication import Publication, PublicationRole


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
    added_by: uuid.UUID | None = Field(
        default=None,
        foreign_key="user.id",
    )
    added_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    publication: Optional["Publication"] = Relationship(back_populates="members")
