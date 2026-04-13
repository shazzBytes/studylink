from datetime import datetime, timedelta, timezone

from sqlmodel import Session, col, select

from app.models.publication import Publication
from app.models.publication_analytics import (
    PublicationAnalyticsEvent,
    PublicationEngagementType,
)
from app.schemas.publications import (
    AnalyticsTimelinePoint,
    PublicationAnalyticsEventCreate,
    PublicationAnalyticsSummary,
    PublicationAnalyticsUpdate,
    ResearcherAnalyticsPublication,
    ResearcherAnalyticsSummary,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def track_publication_event(
    *,
    session: Session,
    publication: Publication,
    event_in: PublicationAnalyticsEventCreate,
    actor_user_id: object | None,
) -> Publication:
    event = PublicationAnalyticsEvent(
        publication_id=publication.id,
        actor_user_id=actor_user_id,
        event_type=event_in.event_type,
        value=event_in.value,
    )
    session.add(event)

    if event_in.event_type == PublicationEngagementType.CITATION:
        publication.citation_count += event_in.value
    elif event_in.event_type == PublicationEngagementType.DOWNLOAD:
        publication.download_count += event_in.value
    elif event_in.event_type == PublicationEngagementType.VIEW:
        publication.view_count += event_in.value
    elif event_in.event_type == PublicationEngagementType.SAVE:
        publication.save_count += event_in.value
    elif event_in.event_type == PublicationEngagementType.SHARE:
        publication.share_count += event_in.value

    publication.last_engagement_at = utcnow()
    session.add(publication)
    session.commit()
    session.refresh(publication)
    return publication


def update_publication_analytics(
    *,
    session: Session,
    publication: Publication,
    analytics_in: PublicationAnalyticsUpdate,
) -> Publication:
    for field, value in analytics_in.model_dump(exclude_unset=True).items():
        setattr(publication, field, value)
    publication.last_engagement_at = utcnow()
    session.add(publication)
    session.commit()
    session.refresh(publication)
    return publication


def list_publication_events(
    *,
    session: Session,
    publication_id: object,
    since: datetime,
) -> list[PublicationAnalyticsEvent]:
    statement = (
        select(PublicationAnalyticsEvent)
        .where(PublicationAnalyticsEvent.publication_id == publication_id)
        .where(PublicationAnalyticsEvent.occurred_at >= since)
        .order_by(col(PublicationAnalyticsEvent.occurred_at))
    )
    return list(session.exec(statement).all())


def build_publication_analytics_summary(
    *,
    session: Session,
    publication: Publication,
) -> PublicationAnalyticsSummary:
    since = utcnow() - timedelta(days=6)
    events = list_publication_events(
        session=session,
        publication_id=publication.id,
        since=since.replace(hour=0, minute=0, second=0, microsecond=0),
    )

    timeline_map: dict[str, int] = {}
    current_day = since.date()
    for day_offset in range(7):
        key = (current_day + timedelta(days=day_offset)).isoformat()
        timeline_map[key] = 0
    for event in events:
        day_key = event.occurred_at.date().isoformat()
        if day_key in timeline_map:
            timeline_map[day_key] += event.value

    return PublicationAnalyticsSummary(
        publication_id=str(publication.id),
        citation_count=publication.citation_count,
        download_count=publication.download_count,
        view_count=publication.view_count,
        save_count=publication.save_count,
        share_count=publication.share_count,
        last_engagement_at=(
            publication.last_engagement_at.isoformat()
            if publication.last_engagement_at
            else None
        ),
        engagement_last_7_days=[
            AnalyticsTimelinePoint(date=date, value=value)
            for date, value in timeline_map.items()
        ],
    )


def build_researcher_analytics_summary(
    *,
    session: Session,
    researcher_id: object,
    publications: list[Publication],
) -> ResearcherAnalyticsSummary:
    since = utcnow() - timedelta(days=29)
    publication_ids = [publication.id for publication in publications]
    timeline_map: dict[str, int] = {}
    current_day = since.date()
    for day_offset in range(30):
        key = (current_day + timedelta(days=day_offset)).isoformat()
        timeline_map[key] = 0

    if publication_ids:
        statement = (
            select(PublicationAnalyticsEvent)
            .where(col(PublicationAnalyticsEvent.publication_id).in_(publication_ids))
            .where(PublicationAnalyticsEvent.occurred_at >= since.replace(hour=0, minute=0, second=0, microsecond=0))
        )
        for event in session.exec(statement).all():
            day_key = event.occurred_at.date().isoformat()
            if day_key in timeline_map:
                timeline_map[day_key] += event.value

    return ResearcherAnalyticsSummary(
        researcher_id=str(researcher_id),
        publication_count=len(publications),
        total_citations=sum(publication.citation_count for publication in publications),
        total_downloads=sum(publication.download_count for publication in publications),
        total_views=sum(publication.view_count for publication in publications),
        total_saves=sum(publication.save_count for publication in publications),
        total_shares=sum(publication.share_count for publication in publications),
        engagement_last_30_days=[
            AnalyticsTimelinePoint(date=date, value=value)
            for date, value in timeline_map.items()
        ],
        publications=[
            ResearcherAnalyticsPublication(
                publication_id=str(publication.id),
                title=publication.title,
                year=publication.year,
                citation_count=publication.citation_count,
                download_count=publication.download_count,
                view_count=publication.view_count,
                save_count=publication.save_count,
                share_count=publication.share_count,
            )
            for publication in publications
        ],
    )
