import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.publication import Publication


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PublicationEngagementType(str, Enum):
    VIEW = "view"
    DOWNLOAD = "download"
    SAVE = "save"
    SHARE = "share"
    CITATION = "citation"


class PublicationAnalyticsEvent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    publication_id: uuid.UUID = Field(foreign_key="publication.id", index=True)
    actor_user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    event_type: PublicationEngagementType = Field(index=True, max_length=32)
    value: int = Field(default=1, ge=1)
    occurred_at: datetime = Field(default_factory=utcnow, index=True)

    publication: "Publication" = Relationship(back_populates="analytics_events")
