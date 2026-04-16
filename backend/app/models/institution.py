import re
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.users import User


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class InstitutionType(str, Enum):
    UNIVERSITY = "university"
    COLLEGE = "college"
    RESEARCH_INSTITUTE = "research_institute"


class InstitutionRole(str, Enum):
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"
    RESEARCHER = "researcher"
    STAFF = "staff"


class InstitutionBase(SQLModel):
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255, index=True, unique=True)
    domain: str | None = Field(default=None, max_length=255, index=True, unique=True)
    institution_type: InstitutionType = Field(
        default=InstitutionType.UNIVERSITY,
        max_length=64,
    )
    description: str | None = Field(default=None, max_length=1000)
    is_verified: bool = True
    is_active: bool = True
    onboarding_enabled: bool = True

    model_config = ConfigDict(use_enum_values=True)


class Institution(InstitutionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    memberships: list["InstitutionMembership"] = Relationship(
        back_populates="institution"
    )


class InstitutionMembership(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "user_id",
            name="uq_institution_membership_institution_user",
        ),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    institution_id: uuid.UUID = Field(foreign_key="institution.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    role: InstitutionRole = Field(default=InstitutionRole.STUDENT, max_length=64)
    department: str | None = Field(default=None, max_length=255)
    title: str | None = Field(default=None, max_length=255)
    is_primary: bool = True
    is_verified: bool = False
    joined_at: datetime = Field(default_factory=utcnow)
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")

    institution: Institution = Relationship(back_populates="memberships")
    user: "User" = Relationship(
        back_populates="institution_memberships",
        sa_relationship_kwargs={"foreign_keys": "[InstitutionMembership.user_id]"},
    )


def slugify_institution_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "institution"
