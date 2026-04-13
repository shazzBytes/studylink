import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.crud.publication import get_publication_by_id
from app.crud.publication_analytics import (
    build_publication_analytics_summary,
    track_publication_event,
    update_publication_analytics,
)
from app.models import Publication
from app.schemas.publications import (
    PublicationAnalyticsEventCreate,
    PublicationAnalyticsSummary,
    PublicationAnalyticsUpdate,
)

router = APIRouter(prefix="/publications", tags=["publications"])


def _get_publication_or_404(*, session: SessionDep, publication_id: uuid.UUID) -> Publication:
    publication = get_publication_by_id(
        session=session,
        publication_id=publication_id,
    )
    if not publication or publication.is_deleted:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication


def _assert_publication_manager(
    *,
    publication: Publication,
    current_user: CurrentUser,
) -> None:
    if current_user.is_superuser:
        return
    if publication.researcher and publication.researcher.email == current_user.email:
        return
    raise HTTPException(
        status_code=403,
        detail="You do not have permission to manage this publication",
    )


@router.get("/{publication_id}", response_model=Publication)
def get_publication_route(
    publication_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    _ = current_user
    publication = _get_publication_or_404(
        session=session,
        publication_id=publication_id,
    )
    return publication


@router.get("/{publication_id}/analytics", response_model=PublicationAnalyticsSummary)
def get_publication_analytics_route(
    publication_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> PublicationAnalyticsSummary:
    _ = current_user
    publication = _get_publication_or_404(
        session=session,
        publication_id=publication_id,
    )
    return build_publication_analytics_summary(
        session=session,
        publication=publication,
    )


@router.post("/{publication_id}/analytics/events", response_model=Publication)
def track_publication_event_route(
    publication_id: uuid.UUID,
    event_in: PublicationAnalyticsEventCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    publication = _get_publication_or_404(
        session=session,
        publication_id=publication_id,
    )
    return track_publication_event(
        session=session,
        publication=publication,
        event_in=event_in,
        actor_user_id=current_user.id,
    )


@router.patch("/{publication_id}/analytics", response_model=Publication)
def update_publication_analytics_route(
    publication_id: uuid.UUID,
    analytics_in: PublicationAnalyticsUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    publication = _get_publication_or_404(
        session=session,
        publication_id=publication_id,
    )
    _assert_publication_manager(publication=publication, current_user=current_user)
    return update_publication_analytics(
        session=session,
        publication=publication,
        analytics_in=analytics_in,
    )
