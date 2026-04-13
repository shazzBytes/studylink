from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.publication import Publication


def test_track_publication_event_and_read_analytics(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    publication = db.exec(select(Publication)).first()
    assert publication is not None

    track_response = client.post(
        f"/api/v1/publications/{publication.id}/analytics/events",
        headers=normal_user_token_headers,
        json={"event_type": "view", "value": 3},
    )

    assert track_response.status_code == 200
    tracked_publication = track_response.json()
    assert tracked_publication["id"] == str(publication.id)
    assert tracked_publication["view_count"] >= publication.view_count

    analytics_response = client.get(
        f"/api/v1/publications/{publication.id}/analytics",
        headers=normal_user_token_headers,
    )

    assert analytics_response.status_code == 200
    analytics = analytics_response.json()
    assert analytics["publication_id"] == str(publication.id)
    assert analytics["view_count"] >= tracked_publication["view_count"]
    assert len(analytics["engagement_last_7_days"]) == 7
