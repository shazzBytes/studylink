import uuid
from datetime import datetime, timezone

from sqlmodel import Session, col, select

from app.models.institution import (
    Institution,
    InstitutionMembership,
    InstitutionRole,
    slugify_institution_name,
)
from app.schemas.institution import InstitutionCreate, InstitutionUpdate


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def list_institutions(
    *,
    session: Session,
    verified_only: bool = False,
    active_only: bool = True,
) -> list[Institution]:
    statement = select(Institution)
    if verified_only:
        statement = statement.where(Institution.is_verified == True)  # noqa: E712
    if active_only:
        statement = statement.where(Institution.is_active == True)  # noqa: E712
    statement = statement.order_by(col(Institution.name))
    return list(session.exec(statement).all())


def get_institution_by_id(
    *,
    session: Session,
    institution_id: uuid.UUID,
) -> Institution | None:
    return session.get(Institution, institution_id)


def get_institution_by_slug(
    *,
    session: Session,
    slug: str,
) -> Institution | None:
    statement = select(Institution).where(Institution.slug == slug)
    return session.exec(statement).first()


def get_institution_by_domain(
    *,
    session: Session,
    domain: str,
) -> Institution | None:
    statement = select(Institution).where(Institution.domain == domain)
    return session.exec(statement).first()


def create_institution(
    *,
    session: Session,
    institution_in: InstitutionCreate,
) -> Institution:
    payload = institution_in.model_dump(exclude_unset=True)
    payload["slug"] = payload.get("slug") or slugify_institution_name(institution_in.name)
    institution = Institution.model_validate(payload)
    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution


def update_institution(
    *,
    session: Session,
    institution: Institution,
    institution_in: InstitutionUpdate,
) -> Institution:
    update_data = institution_in.model_dump(exclude_unset=True)
    if "name" in update_data and "slug" not in update_data:
        update_data["slug"] = slugify_institution_name(str(update_data["name"]))
    institution.sqlmodel_update(update_data, update={"updated_at": utcnow()})
    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution


def count_members_for_institution(*, session: Session, institution_id: uuid.UUID) -> int:
    statement = (
        select(func.count())
        .select_from(InstitutionMembership)
        .where(InstitutionMembership.institution_id == institution_id)
    )
    return int(session.exec(statement).one())


def get_institution_membership(
    *,
    session: Session,
    institution_id: uuid.UUID,
    user_id: uuid.UUID,
) -> InstitutionMembership | None:
    statement = (
        select(InstitutionMembership)
        .where(InstitutionMembership.institution_id == institution_id)
        .where(InstitutionMembership.user_id == user_id)
    )
    return session.exec(statement).first()


def list_institution_memberships(
    *,
    session: Session,
    institution_id: uuid.UUID,
) -> list[InstitutionMembership]:
    statement = (
        select(InstitutionMembership)
        .where(InstitutionMembership.institution_id == institution_id)
        .order_by(col(InstitutionMembership.joined_at))
    )
    return list(session.exec(statement).all())


def list_memberships_for_user(
    *,
    session: Session,
    user_id: uuid.UUID,
) -> list[InstitutionMembership]:
    statement = (
        select(InstitutionMembership)
        .where(InstitutionMembership.user_id == user_id)
        .order_by(col(InstitutionMembership.is_primary).desc(), col(InstitutionMembership.joined_at))
    )
    return list(session.exec(statement).all())


def upsert_institution_membership(
    *,
    session: Session,
    institution_id: uuid.UUID,
    user_id: uuid.UUID,
    role: InstitutionRole,
    department: str | None,
    title: str | None,
    is_primary: bool,
    is_verified: bool,
    created_by_id: uuid.UUID | None,
) -> tuple[InstitutionMembership, bool]:
    membership = get_institution_membership(
        session=session,
        institution_id=institution_id,
        user_id=user_id,
    )
    created = membership is None

    if membership is None:
        membership = InstitutionMembership(
            institution_id=institution_id,
            user_id=user_id,
            role=role,
            department=department,
            title=title,
            is_primary=is_primary,
            is_verified=is_verified,
            created_by_id=created_by_id,
        )
    else:
        membership.role = role
        membership.department = department
        membership.title = title
        membership.is_primary = is_primary
        membership.is_verified = is_verified
        membership.created_by_id = created_by_id

    if is_primary:
        statement = select(InstitutionMembership).where(
            InstitutionMembership.user_id == user_id
        )
        for existing in session.exec(statement).all():
            if existing.id != membership.id:
                existing.is_primary = False
                session.add(existing)

    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership, created
