import uuid

import pytest
from sqlmodel import Session

from app.crud.researcher import (
    create_researcher,
    get_researcher_by_id,
    get_researcher_by_email,
    update_researcher,
    delete_researcher,
    search_researchers,
)
from app.schemas.researcher import CreateResearcherInfo, UpdateResearcherInfo
from tests.utils.utils import random_email, random_lower_string


def test_create_researcher(db: Session) -> None:
    """Test creating a researcher"""
    email = random_email()
    full_name = "John Doe"
    qualification = "PhD"
    institute = "MIT"
    
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name=full_name,
        qualification=qualification,
        institute=institute,
        bio="Test bio"
    )
    
    researcher = create_researcher(session=db, researcher_in=researcher_in)
    
    assert researcher.email == email
    assert researcher.full_name == full_name
    assert researcher.qualification == qualification
    assert researcher.institute == institute
    assert researcher.id is not None


def test_get_researcher_by_id(db: Session) -> None:
    """Test retrieving a researcher by ID"""
    email = random_email()
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name="Jane Doe",
        qualification="PhD",
        institute="Stanford"
    )
    
    created = create_researcher(session=db, researcher_in=researcher_in)
    
    retrieved = get_researcher_by_id(session=db, researcher_id=created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.email == email


def test_get_researcher_by_id_not_found(db: Session) -> None:
    """Test retrieving a non-existent researcher"""
    fake_id = uuid.uuid4()
    
    researcher = get_researcher_by_id(session=db, researcher_id=fake_id)
    
    assert researcher is None


def test_get_researcher_by_email(db: Session) -> None:
    """Test retrieving a researcher by email"""
    email = random_email()
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name="Test Researcher",
        qualification="MSc"
    )
    
    create_researcher(session=db, researcher_in=researcher_in)
    
    retrieved = get_researcher_by_email(session=db, researcher_email=email)
    
    assert retrieved is not None
    assert retrieved.email == email


def test_get_researcher_by_email_not_found(db: Session) -> None:
    """Test retrieving a researcher by non-existent email"""
    fake_email = random_email()
    
    researcher = get_researcher_by_email(session=db, researcher_email=fake_email)
    
    assert researcher is None


def test_update_researcher(db: Session) -> None:
    """Test updating a researcher"""
    email = random_email()
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name="Original Name",
        qualification="BSc",
        institute="Original Institute"
    )
    
    researcher = create_researcher(session=db, researcher_in=researcher_in)
    
    update_in = UpdateResearcherInfo(
        full_name="Updated Name",
        qualification="PhD",
        bio="New bio"
    )
    
    updated = update_researcher(
        session=db,
        db_researcher=researcher,
        researcher_in=update_in
    )
    
    assert updated.full_name == "Updated Name"
    assert updated.qualification == "PhD"
    assert updated.bio == "New bio"
    assert updated.email == email  # Unchanged
    assert updated.institute == "Original Institute"  # Unchanged


def test_update_researcher_partial(db: Session) -> None:
    """Test partial update of a researcher"""
    email = random_email()
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name="Test Name",
        qualification="MSc",
        institute="Test Institute"
    )
    
    researcher = create_researcher(session=db, researcher_in=researcher_in)
    
    # Only update qualification
    update_in = UpdateResearcherInfo(qualification="PhD")
    
    updated = update_researcher(
        session=db,
        db_researcher=researcher,
        researcher_in=update_in
    )
    
    assert updated.qualification == "PhD"
    assert updated.full_name == "Test Name"
    assert updated.email == email


def test_delete_researcher(db: Session) -> None:
    """Test deleting a researcher"""
    email = random_email()
    researcher_in = CreateResearcherInfo(
        email=email,
        full_name="To Delete",
        qualification="PhD"
    )
    
    researcher = create_researcher(session=db, researcher_in=researcher_in)
    researcher_id = researcher.id
    
    delete_researcher(session=db, db_researcher=researcher)
    
    deleted = get_researcher_by_id(session=db, researcher_id=researcher_id)
    assert deleted is None


def test_search_researchers_by_full_name(db: Session) -> None:
    """Test searching researchers by full name"""
    # Create researchers with distinct names
    names = ["Alice Johnson", "Bob Smith", "Alice Williams"]
    
    for name in names:
        researcher_in = CreateResearcherInfo(
            email=random_email(),
            full_name=name,
            qualification="PhD"
        )
        create_researcher(session=db, researcher_in=researcher_in)
    
    results = search_researchers(
        session=db,
        full_name="Alice",
        skip=0,
        limit=10
    )
    
    assert len(results) >= 2
    assert all("Alice" in r.full_name for r in results)


def test_search_researchers_by_email(db: Session) -> None:
    """Test searching researchers by email pattern"""
    email1 = "test.user1@example.com"
    email2 = "test.user2@example.com"
    email3 = "other@domain.com"
    
    for email in [email1, email2, email3]:
        researcher_in = CreateResearcherInfo(
            email=email,
            full_name=random_lower_string(),
            qualification="PhD"
        )
        create_researcher(session=db, researcher_in=researcher_in)
    
    results = search_researchers(
        session=db,
        email="test.user",
        skip=0,
        limit=10
    )
    
    assert len(results) >= 2
    assert all("test.user" in r.email for r in results)


def test_search_researchers_by_institute(db: Session) -> None:
    """Test searching researchers by institute"""
    institutes = ["MIT", "Stanford", "MIT Lab"]
    
    for institute in institutes:
        researcher_in = CreateResearcherInfo(
            email=random_email(),
            full_name=random_lower_string(),
            qualification="PhD",
            institute=institute
        )
        create_researcher(session=db, researcher_in=researcher_in)
    
    results = search_researchers(
        session=db,
        institute="MIT",
        skip=0,
        limit=10
    )
    
    assert len(results) >= 2
    assert all("MIT" in (r.institute or "") for r in results)


def test_search_researchers_multiple_filters(db: Session) -> None:
    """Test searching with multiple filter criteria"""
    researcher_in = CreateResearcherInfo(
        email="unique.test@example.com",
        full_name="Unique Researcher",
        qualification="PhD",
        institute="Unique Institute"
    )
    created = create_researcher(session=db, researcher_in=researcher_in)
    
    results = search_researchers(
        session=db,
        full_name="Unique",
        email="unique.test",
        institute="Unique",
        skip=0,
        limit=10
    )
    
    assert len(results) >= 1
    assert any(r.id == created.id for r in results)


def test_search_researchers_pagination(db: Session) -> None:
    """Test researcher search pagination"""
    # Create multiple researchers
    for i in range(10):
        researcher_in = CreateResearcherInfo(
            email=random_email(),
            full_name=f"Researcher {i}",
            qualification="PhD"
        )
        create_researcher(session=db, researcher_in=researcher_in)
    
    # Get first page
    page1 = search_researchers(session=db, skip=0, limit=5)
    assert len(page1) <= 5
    
    # Get second page
    page2 = search_researchers(session=db, skip=5, limit=5)
    assert len(page2) <= 5
    
    # Ensure pages are different
    page1_ids = {r.id for r in page1}
    page2_ids = {r.id for r in page2}
    assert page1_ids.isdisjoint(page2_ids)


def test_search_researchers_no_results(db: Session) -> None:
    """Test search with no matching results"""
    results = search_researchers(
        session=db,
        full_name="NonExistentResearcher123456789",
        skip=0,
        limit=10
    )
    
    assert len(results) == 0


def test_search_researchers_case_insensitive(db: Session) -> None:
    """Test that search is case insensitive"""
    researcher_in = CreateResearcherInfo(
        email="TestCase@Example.COM",
        full_name="TestCase Researcher",
        qualification="PhD",
        institute="TestCase Institute"
    )
    created = create_researcher(session=db, researcher_in=researcher_in)
    
    # Search with lowercase
    results = search_researchers(
        session=db,
        full_name="testcase",
        skip=0,
        limit=10
    )
    
    assert len(results) >= 1
    assert any(r.id == created.id for r in results)


def test_researcher_email_unique_constraint(db: Session) -> None:
    """Test that duplicate emails are not allowed"""
    email = random_email()
    
    researcher_in1 = CreateResearcherInfo(
        email=email,
        full_name="First Researcher",
        qualification="PhD"
    )
    create_researcher(session=db, researcher_in=researcher_in1)
    
    # Try to create another with same email
    researcher_in2 = CreateResearcherInfo(
        email=email,
        full_name="Second Researcher",
        qualification="MSc"
    )
    
    with pytest.raises(Exception):  # Will raise IntegrityError
        create_researcher(session=db, researcher_in=researcher_in2)
        db.commit()
