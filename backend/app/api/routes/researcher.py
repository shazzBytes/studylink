import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import CurrentUser, get_db
from app.crud.collaborator import get_researcher_collaborators
from app.crud.publication import (
    get_publications_by_researcher,
    replace_researcher_publications,
)
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

    return create_researcher(
        session=session,
        researcher_in=researcher_data,
    )


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

    return update_researcher(
        session=session,
        db_researcher=researcher,
        researcher_in=researcher_in,
    )


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
