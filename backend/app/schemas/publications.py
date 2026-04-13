from sqlmodel import SQLModel

from app.models.publication_analytics import PublicationEngagementType

class CreatePublication(SQLModel):
    title: str
    publisher: str
    year: int | None = None

    description: str | None = None

    domains: list[str] = []


class UpdatePublication(SQLModel):
    title: str | None = None
    publisher: str | None = None
    year: int | None = None

    description: str | None = None

    domains: list[str] | None = None


class PublicationAnalyticsEventCreate(SQLModel):
    event_type: PublicationEngagementType
    value: int = 1


class PublicationAnalyticsUpdate(SQLModel):
    citation_count: int | None = None
    download_count: int | None = None
    view_count: int | None = None
    save_count: int | None = None
    share_count: int | None = None


class AnalyticsTimelinePoint(SQLModel):
    date: str
    value: int


class PublicationAnalyticsSummary(SQLModel):
    publication_id: str
    citation_count: int
    download_count: int
    view_count: int
    save_count: int
    share_count: int
    last_engagement_at: str | None = None
    engagement_last_7_days: list[AnalyticsTimelinePoint]


class ResearcherAnalyticsPublication(SQLModel):
    publication_id: str
    title: str
    year: int | None = None
    citation_count: int
    download_count: int
    view_count: int
    save_count: int
    share_count: int


class ResearcherAnalyticsSummary(SQLModel):
    researcher_id: str
    publication_count: int
    total_citations: int
    total_downloads: int
    total_views: int
    total_saves: int
    total_shares: int
    engagement_last_30_days: list[AnalyticsTimelinePoint]
    publications: list[ResearcherAnalyticsPublication]
