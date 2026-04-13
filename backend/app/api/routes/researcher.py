import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import CurrentUser, get_db
from app.crud.institution import list_memberships_for_user
from app.crud.collaborator import get_researcher_collaborators
from app.crud.publication import (
    get_publications_by_researcher,
    replace_researcher_publications,
)
from app.crud.publication_analytics import build_researcher_analytics_summary
from app.crud.researcher import (
    create_researcher,
    get_researcher_by_email,
    get_researcher_by_id,
    search_researchers,
    update_researcher,
)
from app.models.publication import Publication
from app.models.researcher import ResearcherInfo
from app.schemas.publications import CreatePublication
from app.schemas.publications import ResearcherAnalyticsSummary
from app.schemas.researcher import CreateResearcherInfo, UpdateResearcherInfo

router = APIRouter(
    prefix="/researchers",
    tags=["Researchers"],
)


@router.get(
    "/me",
    response_model=ResearcherInfo,
)
def get_my_researcher_profile(
    *,
    session: Session = Depends(get_db),
    current_user: CurrentUser,
):
    """Get the current user's researcher profile."""
    researcher = get_researcher_by_email(
        session=session,
        researcher_email=current_user.email,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher profile not found. Please create one first.",
        )
    return researcher


@router.post(
    "/me",
    response_model=ResearcherInfo,
)
def create_my_researcher_profile(
    *,
    session: Session = Depends(get_db),
    current_user: CurrentUser,
    researcher_in: CreateResearcherInfo,
):
    """Create a researcher profile for the current user."""
    # Check if profile already exists
    existing = get_researcher_by_email(
        session=session,
        researcher_email=current_user.email,
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Researcher profile already exists. Use PUT to update.",
        )

    # Ensure the email matches the current user
    researcher_data = researcher_in.model_copy(
        update={"email": current_user.email}
    )
    memberships = list_memberships_for_user(session=session, user_id=current_user.id)
    primary_membership = next((membership for membership in memberships if membership.is_primary), None)
    if primary_membership:
        researcher_data = researcher_data.model_copy(
            update={
                "institute": primary_membership.institution.name,
                "department": primary_membership.department,
            }
        )

    researcher = create_researcher(
        session=session,
        researcher_in=researcher_data,
    )
    researcher.user_id = current_user.id
    researcher.affiliation_verified = bool(primary_membership and primary_membership.is_verified)
    session.add(researcher)
    session.commit()
    session.refresh(researcher)
    return researcher


@router.put(
    "/me",
    response_model=ResearcherInfo,
)
def update_my_researcher_profile(
    *,
    session: Session = Depends(get_db),
    current_user: CurrentUser,
    researcher_in: UpdateResearcherInfo,
):
    """Update the current user's researcher profile."""
    researcher = get_researcher_by_email(
        session=session,
        researcher_email=current_user.email,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher profile not found. Please create one first.",
        )

    updated = update_researcher(
        session=session,
        db_researcher=researcher,
        researcher_in=researcher_in,
    )
    memberships = list_memberships_for_user(session=session, user_id=current_user.id)
    primary_membership = next((membership for membership in memberships if membership.is_primary), None)
    updated.user_id = current_user.id
    if primary_membership:
        updated.institute = primary_membership.institution.name
        updated.department = researcher_in.department or primary_membership.department
        updated.affiliation_verified = primary_membership.is_verified
        session.add(updated)
        session.commit()
        session.refresh(updated)
    return updated


@router.get(
    "/search",
    response_model=list[ResearcherInfo],
)
def search_researchers_route(
    *,
    session: Session = Depends(get_db),
    full_name: str | None = None,
    email: str | None = None,
    institute: str | None = None,
    skip: int = 0,
    limit: int = 50,
):
    return search_researchers(
        session=session,
        full_name=full_name,
        email=email,
        institute=institute,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{researcher_id}",
    response_model=ResearcherInfo,
)
def get_researcher_route(
    *,
    session: Session = Depends(get_db),
    researcher_id: uuid.UUID,
):
    researcher = get_researcher_by_id(
        session=session,
        researcher_id=researcher_id,
    )

    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher not found",
        )

    return researcher

@router.get(
    "/{researcher_id}/publications",
    response_model=list[Publication],
)
def get_researcher_publications_route(
    *,
    session: Session = Depends(get_db),
    researcher_id: uuid.UUID,
):
    researcher = get_researcher_by_id(
        session=session,
        researcher_id=researcher_id,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher not found",
        )

    return get_publications_by_researcher(
        session=session,
        researcher_id=researcher_id,
    )

@router.put(
    "/{researcher_id}/publications",
    response_model=list[Publication],
)
def put_researcher_publications(
    *,
    session: Session = Depends(get_db),
    researcher_id: uuid.UUID,
    publications: list[CreatePublication],
):
    researcher = get_researcher_by_id(
        session=session,
        researcher_id=researcher_id,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher not found",
        )

    return replace_researcher_publications(
        session=session,
        researcher_id=researcher_id,
        publications_in=publications,
    )


@router.get(
    "/me/analytics",
    response_model=ResearcherAnalyticsSummary,
)
def get_my_researcher_analytics(
    *,
    session: Session = Depends(get_db),
    current_user: CurrentUser,
):
    researcher = get_researcher_by_email(
        session=session,
        researcher_email=current_user.email,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher profile not found. Please create one first.",
        )

    publications = get_publications_by_researcher(
        session=session,
        researcher_id=researcher.id,
    )
    return build_researcher_analytics_summary(
        session=session,
        researcher_id=researcher.id,
        publications=publications,
    )

def get_researcher_collaborators_route(
    *,
    session: Session = Depends(get_db),
    researcher_id: uuid.UUID,
):
    # Ensure researcher exists
    researcher = get_researcher_by_id(
        session=session,
        researcher_id=researcher_id,
    )
    if not researcher:
        raise HTTPException(
            status_code=404,
            detail="Researcher not found",
        )

    return get_researcher_collaborators(
        session=session,
        researcher_id=researcher_id,
    )
