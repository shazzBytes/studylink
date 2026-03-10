import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.researcher import create_random_researcher


def test_get_researcher_by_id(
    client: TestClient, db: Session
) -> None:
    """Test retrieving a researcher by ID"""
    researcher = create_random_researcher(db)

    r = client.get(f"/api/v1/researchers/{researcher.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == str(researcher.id)
    assert data["email"] == researcher.email
    assert data["full_name"] == researcher.full_name


def test_get_researcher_not_found(
    client: TestClient, db: Session
) -> None:
    _ = db
    """Test retrieving a non-existent researcher"""
    fake_id = uuid.uuid4()

    r = client.get(f"/api/v1/researchers/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Researcher not found"


def test_put_researcher_publications(
    client: TestClient, db: Session
) -> None:
    """Test replacing researcher publications"""
    researcher = create_random_researcher(db)

    publications_data = [
        {
            "title": "Test Publication 1",
            "publisher": "Test Publisher 1",
            "year": 2023,
            "description": "Test description 1",
            "domains": ["AI", "Machine Learning"]
        },
        {
            "title": "Test Publication 2",
            "publisher": "Test Publisher 2",
            "year": 2024,
            "description": "Test description 2",
            "domains": ["Data Science"]
        }
    ]

    r = client.put(
        f"/api/v1/researchers/{researcher.id}/publications",
        json=publications_data
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Publication 1"
    assert data[1]["title"] == "Test Publication 2"


def test_put_researcher_publications_not_found(
    client: TestClient, db: Session
) -> None:
    _ = db
    """Test replacing publications for non-existent researcher"""
    fake_id = uuid.uuid4()

    publications_data = [
        {
            "title": "Test Publication",
            "publisher": "Test Publisher",
            "year": 2023,
            "domains": ["AI"]
        }
    ]

    r = client.put(
        f"/api/v1/researchers/{fake_id}/publications",
        json=publications_data
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Researcher not found"


def test_search_researchers_by_full_name(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers by full name"""
    researcher = create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={"full_name": researcher.full_name[:5]}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(r["id"] == str(researcher.id) for r in data)


def test_search_researchers_by_email(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers by email"""
    researcher = create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={"email": researcher.email}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(r["email"] == researcher.email for r in data)


def test_search_researchers_by_institute(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers by institute"""
    researcher = create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={"institute": researcher.institute}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(r["institute"] == researcher.institute for r in data)


def test_search_researchers_multiple_params(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers with multiple parameters"""
    researcher = create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={
            "full_name": researcher.full_name[:5],
            "email": researcher.email[:5],
            "institute": researcher.institute
        }
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


def test_search_researchers_with_pagination(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers with skip and limit"""
    # Create multiple researchers
    for _ in range(5):
        create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={"skip": 0, "limit": 3}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 3


def test_search_researchers_no_params(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers without any filter parameters"""
    create_random_researcher(db)

    r = client.get("/api/v1/researchers/search")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


def test_search_researchers_empty_result(
    client: TestClient, db: Session
) -> None:
    _ = db
    """Test searching researchers with non-existent criteria"""
    r = client.get(
        "/api/v1/researchers/search",
        params={"full_name": "NonExistentResearcher123456789"}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_search_researchers_partial_match(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers with partial name match"""
    researcher = create_random_researcher(db)
    partial_name = researcher.full_name[:4]

    r = client.get(
        "/api/v1/researchers/search",
        params={"full_name": partial_name}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(partial_name.lower() in r["full_name"].lower() for r in data)


def test_search_researchers_custom_limit(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers with custom limit"""
    for _ in range(10):
        create_random_researcher(db)

    r = client.get(
        "/api/v1/researchers/search",
        params={"limit": 5}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_search_researchers_with_skip(
    client: TestClient, db: Session
) -> None:
    """Test searching researchers with skip parameter"""
    for _ in range(10):
        create_random_researcher(db)

    # Get first page
    r1 = client.get(
        "/api/v1/researchers/search",
        params={"skip": 0, "limit": 5}
    )
    assert r1.status_code == 200
    page1 = r1.json()

    # Get second page
    r2 = client.get(
        "/api/v1/researchers/search",
        params={"skip": 5, "limit": 5}
    )
    assert r2.status_code == 200
    page2 = r2.json()

    # Ensure pages are different
    page1_ids = {r["id"] for r in page1}
    page2_ids = {r["id"] for r in page2}
    assert page1_ids.isdisjoint(page2_ids)
