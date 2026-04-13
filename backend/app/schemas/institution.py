import uuid

from sqlmodel import SQLModel

from app.models.institution import InstitutionRole, InstitutionType
from app.models.users import AccountType


class InstitutionCreate(SQLModel):
    name: str
    slug: str | None = None
    domain: str | None = None
    institution_type: InstitutionType = InstitutionType.UNIVERSITY
    description: str | None = None
    is_verified: bool = True
    onboarding_enabled: bool = True


class InstitutionUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
    domain: str | None = None
    institution_type: InstitutionType | None = None
    description: str | None = None
    is_verified: bool | None = None
    is_active: bool | None = None
    onboarding_enabled: bool | None = None


class InstitutionPublic(SQLModel):
    id: uuid.UUID
    name: str
    slug: str
    domain: str | None = None
    institution_type: InstitutionType
    description: str | None = None
    is_verified: bool
    is_active: bool
    onboarding_enabled: bool
    member_count: int


class InstitutionMembershipCreate(SQLModel):
    user_id: uuid.UUID
    role: InstitutionRole = InstitutionRole.STUDENT
    department: str | None = None
    title: str | None = None
    is_primary: bool = True
    is_verified: bool = True


class InstitutionMembershipPublic(SQLModel):
    id: uuid.UUID
    institution_id: uuid.UUID
    institution_name: str
    institution_slug: str
    role: InstitutionRole
    department: str | None = None
    title: str | None = None
    is_primary: bool
    is_verified: bool
    user_id: uuid.UUID
    user_email: str
    user_full_name: str | None = None


class InstitutionBulkOnboardMember(SQLModel):
    email: str
    password: str
    full_name: str | None = None
    account_type: AccountType = AccountType.STUDENT
    role: InstitutionRole = InstitutionRole.STUDENT
    department: str | None = None
    title: str | None = None
    is_primary: bool = True
    is_verified: bool = True


class InstitutionBulkOnboardRequest(SQLModel):
    members: list[InstitutionBulkOnboardMember]


class InstitutionBulkOnboardResult(SQLModel):
    created_users: int
    updated_memberships: int
    memberships: list[InstitutionMembershipPublic]
