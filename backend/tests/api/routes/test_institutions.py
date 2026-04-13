from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Institution, InstitutionMembership, User
from tests.utils.utils import random_email


def test_create_institution_and_bulk_onboard_members(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    db: Session,
) -> None:
    create_response = client.post(
        "/api/v1/institutions/",
        headers=superuser_token_headers,
        json={
            "name": "Test Partner University",
            "domain": "partner.example.edu",
            "institution_type": "university",
            "description": "Partner campus for onboarding tests.",
        },
    )

    assert create_response.status_code == 200
    institution = create_response.json()
    assert institution["name"] == "Test Partner University"
    assert institution["member_count"] == 0

    onboard_email = random_email()
    onboard_response = client.post(
        f"/api/v1/institutions/{institution['id']}/bulk-onboard",
        headers=superuser_token_headers,
        json={
            "members": [
                {
                    "email": onboard_email,
                    "password": "StrongPass123!",
                    "full_name": "Onboarded Researcher",
                    "account_type": "researcher",
                    "role": "researcher",
                    "department": "AI Lab",
                    "title": "Research Fellow",
                    "is_primary": True,
                    "is_verified": True,
                }
            ]
        },
    )

    assert onboard_response.status_code == 200
    body = onboard_response.json()
    assert body["created_users"] == 1
    assert len(body["memberships"]) == 1
    assert body["memberships"][0]["institution_name"] == "Test Partner University"
    assert body["memberships"][0]["role"] == "researcher"

    user = db.exec(select(User).where(User.email == onboard_email)).first()
    assert user is not None
    membership = db.exec(
        select(InstitutionMembership).where(InstitutionMembership.user_id == user.id)
    ).first()
    assert membership is not None
    assert membership.department == "AI Lab"
    db_institution = db.exec(
        select(Institution).where(Institution.id == institution["id"])
    ).first()
    assert db_institution is not None


def test_read_my_institution_memberships(
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/institutions/me/memberships",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    memberships = response.json()
    assert isinstance(memberships, list)
