import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.crud.institution import (
    count_members_for_institution,
    create_institution,
    get_institution_by_domain,
    get_institution_by_id,
    get_institution_by_slug,
    get_institution_membership,
    list_institution_memberships,
    list_institutions,
    list_memberships_for_user,
    upsert_institution_membership,
    update_institution,
)
from app.models.institution import InstitutionRole
from app.models.users import User
from app.models.users import UserCreate
from app.crud.researcher import get_researcher_by_email
from app.crud.researcher import create_researcher, update_researcher
from app.schemas.institution import (
    InstitutionBulkOnboardRequest,
    InstitutionBulkOnboardResult,
    InstitutionCreate,
    InstitutionMembershipCreate,
    InstitutionMembershipPublic,
    InstitutionPublic,
    InstitutionUpdate,
)
from app.schemas.researcher import CreateResearcherInfo
from app.schemas.researcher import UpdateResearcherInfo

router = APIRouter(prefix="/institutions", tags=["institutions"])


def _serialize_membership(membership: Any) -> InstitutionMembershipPublic:
    institution = membership.institution
    user = membership.user
    return InstitutionMembershipPublic(
        id=membership.id,
        institution_id=membership.institution_id,
        institution_name=institution.name,
        institution_slug=institution.slug,
        role=membership.role,
        department=membership.department,
        title=membership.title,
        is_primary=membership.is_primary,
        is_verified=membership.is_verified,
        user_id=membership.user_id,
        user_email=user.email,
        user_full_name=user.full_name,
    )


def _serialize_institution(session: SessionDep, institution: Any) -> InstitutionPublic:
    return InstitutionPublic(
        id=institution.id,
        name=institution.name,
        slug=institution.slug,
        domain=institution.domain,
        institution_type=institution.institution_type,
        description=institution.description,
        is_verified=institution.is_verified,
        is_active=institution.is_active,
        onboarding_enabled=institution.onboarding_enabled,
        member_count=count_members_for_institution(
            session=session,
            institution_id=institution.id,
        ),
    )


def _assert_institution_manager(
    *,
    session: SessionDep,
    institution_id: uuid.UUID,
    current_user: CurrentUser,
) -> None:
    if current_user.is_superuser:
        return
    membership = get_institution_membership(
        session=session,
        institution_id=institution_id,
        user_id=current_user.id,
    )
    if membership and membership.role == InstitutionRole.ADMIN:
        return
    raise HTTPException(
        status_code=403,
        detail="You do not have permission to manage this institution",
    )


@router.get("/", response_model=list[InstitutionPublic])
def read_institutions(
    session: SessionDep,
    current_user: CurrentUser,
    verified_only: bool = False,
) -> list[InstitutionPublic]:
    _ = current_user
    institutions = list_institutions(
        session=session,
        verified_only=verified_only,
    )
    return [_serialize_institution(session, institution) for institution in institutions]


@router.get("/me/memberships", response_model=list[InstitutionMembershipPublic])
def read_my_institution_memberships(
    session: SessionDep,
    current_user: CurrentUser,
) -> list[InstitutionMembershipPublic]:
    memberships = list_memberships_for_user(session=session, user_id=current_user.id)
    return [_serialize_membership(membership) for membership in memberships]


@router.get("/{institution_id}", response_model=InstitutionPublic)
def read_institution(
    institution_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> InstitutionPublic:
    _ = current_user
    institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return _serialize_institution(session, institution)


@router.post("/", response_model=InstitutionPublic)
def create_institution_route(
    institution_in: InstitutionCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> InstitutionPublic:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    if institution_in.slug and get_institution_by_slug(session=session, slug=institution_in.slug):
        raise HTTPException(status_code=409, detail="Institution slug already exists")
    if institution_in.domain and get_institution_by_domain(session=session, domain=institution_in.domain):
        raise HTTPException(status_code=409, detail="Institution domain already exists")
    institution = create_institution(session=session, institution_in=institution_in)
    return _serialize_institution(session, institution)


@router.patch("/{institution_id}", response_model=InstitutionPublic)
def update_institution_route(
    institution_id: uuid.UUID,
    institution_in: InstitutionUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> InstitutionPublic:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    if institution_in.slug:
        existing = get_institution_by_slug(session=session, slug=institution_in.slug)
        if existing and existing.id != institution.id:
            raise HTTPException(status_code=409, detail="Institution slug already exists")
    if institution_in.domain:
        existing_domain = get_institution_by_domain(session=session, domain=institution_in.domain)
        if existing_domain and existing_domain.id != institution.id:
            raise HTTPException(status_code=409, detail="Institution domain already exists")
    institution = update_institution(
        session=session,
        institution=institution,
        institution_in=institution_in,
    )
    return _serialize_institution(session, institution)


@router.get("/{institution_id}/members", response_model=list[InstitutionMembershipPublic])
def read_institution_members(
    institution_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> list[InstitutionMembershipPublic]:
    _ = current_user
    institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    memberships = list_institution_memberships(
        session=session,
        institution_id=institution_id,
    )
    return [_serialize_membership(membership) for membership in memberships]


@router.post("/{institution_id}/members", response_model=InstitutionMembershipPublic)
def add_institution_member(
    institution_id: uuid.UUID,
    member_in: InstitutionMembershipCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> InstitutionMembershipPublic:
    institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    _assert_institution_manager(
        session=session,
        institution_id=institution_id,
        current_user=current_user,
    )
    user = session.get(User, member_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    membership, _ = upsert_institution_membership(
        session=session,
        institution_id=institution_id,
        user_id=member_in.user_id,
        role=member_in.role,
        department=member_in.department,
        title=member_in.title,
        is_primary=member_in.is_primary,
        is_verified=member_in.is_verified,
        created_by_id=current_user.id,
    )

    researcher = get_researcher_by_email(session=session, researcher_email=user.email)
    if researcher:
        update_researcher(
            session=session,
            db_researcher=researcher,
            researcher_in=UpdateResearcherInfo(
                institute=institution.name,
                department=member_in.department,
            ),
        )
        researcher.affiliation_verified = member_in.is_verified
        session.add(researcher)
        session.commit()

    return _serialize_membership(membership)


@router.post(
    "/{institution_id}/bulk-onboard",
    response_model=InstitutionBulkOnboardResult,
)
def bulk_onboard_institution_members(
    institution_id: uuid.UUID,
    request: InstitutionBulkOnboardRequest,
    session: SessionDep,
    current_user: CurrentUser,
) -> InstitutionBulkOnboardResult:
    institution = get_institution_by_id(session=session, institution_id=institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    _assert_institution_manager(
        session=session,
        institution_id=institution_id,
        current_user=current_user,
    )

    created_users = 0
    updated_memberships = 0
    memberships: list[InstitutionMembershipPublic] = []

    for member in request.members:
        existing_user = crud.get_user_by_email(session=session, email=member.email)
        if existing_user is None:
            existing_user = crud.create_user(
                session=session,
                user_create=UserCreate(
                    email=member.email,
                    password=member.password,
                    full_name=member.full_name,
                    account_type=member.account_type,
                ),
            )
            created_users += 1

        membership, created = upsert_institution_membership(
            session=session,
            institution_id=institution_id,
            user_id=existing_user.id,
            role=member.role,
            department=member.department,
            title=member.title,
            is_primary=member.is_primary,
            is_verified=member.is_verified,
            created_by_id=current_user.id,
        )
        if not created:
            updated_memberships += 1

        if member.account_type == "researcher":
            researcher = get_researcher_by_email(
                session=session,
                researcher_email=existing_user.email,
            )
            if researcher is None:
                researcher = create_researcher(
                    session=session,
                    researcher_in=CreateResearcherInfo(
                        full_name=existing_user.full_name or member.full_name or member.email,
                        email=existing_user.email,
                        qualification=member.title or "Researcher",
                        institute=institution.name,
                        department=member.department,
                        bio=None,
                    ),
                )
            researcher.user_id = existing_user.id
            researcher.institute = institution.name
            researcher.department = member.department
            researcher.affiliation_verified = member.is_verified
            session.add(researcher)
            session.commit()
            session.refresh(researcher)

        memberships.append(_serialize_membership(membership))

    return InstitutionBulkOnboardResult(
        created_users=created_users,
        updated_memberships=updated_memberships,
        memberships=memberships,
    )
