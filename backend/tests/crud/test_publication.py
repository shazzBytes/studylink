import uuid
from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.crud.publication import create_publication
from app.schemas.publications import CreatePublication
from tests.utils.researcher import create_random_researcher
from tests.utils.utils import random_lower_string


def test_create_publication(db: Session) -> None:
    """Test creating a publication"""
    researcher = create_random_researcher(db)
    
    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Test Publisher",
        year=2023,
        description="Test description",
        domains=["AI", "Machine Learning"]
    )
    
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )
    
    assert publication.title == "Test Publication"
    assert publication.publisher == "Test Publisher"
    assert publication.year == 2023
    assert publication.researcher_id == researcher.id
    assert "AI" in publication.domains


def test_get_publications_by_researcher(db: Session) -> None:
    """Test retrieving publications for a researcher"""
    from app.crud.publication import get_publications_by_researcher
    
    researcher = create_random_researcher(db)
    
    # Create multiple publications
    for i in range(3):
        publication_in = CreatePublication(
            title=f"Publication {i}",
            publisher=f"Publisher {i}",
            year=2020 + i,
            domains=["Domain"]
        )
        create_publication(
            session=db,
            publication_in=publication_in,
            researcher_id=researcher.id
        )
    
    publications = get_publications_by_researcher(
        session=db,
        researcher_id=researcher.id
    )
    
    assert len(publications) == 3
    # Should be sorted by year descending
    if publications[0].year is not None and publications[1].year is not None:
        assert publications[0].year >= publications[1].year


def test_update_publication(db: Session) -> None:
    """Test updating a publication"""
    from app.crud.publication import update_publication
    from app.schemas.publications import UpdatePublication
    
    researcher = create_random_researcher(db)
    
    publication_in = CreatePublication(
        title="Original Title",
        publisher="Original Publisher",
        year=2023,
        domains=["AI"]
    )
    
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )
    
    update_in = UpdatePublication(
        title="Updated Title",
        year=2024
    )
    
    updated = update_publication(
        session=db,
        db_publication=publication,
        publication_in=update_in
    )
    
    assert updated.title == "Updated Title"
    assert updated.year == 2024
    assert updated.publisher == "Original Publisher"  # Unchanged


def test_delete_publication(db: Session) -> None:
    """Test deleting a publication"""
    from app.crud.publication import delete_publication, get_publication_by_id
    
    researcher = create_random_researcher(db)
    
    publication_in = CreatePublication(
        title="To Delete",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )
    
    pub_id = publication.id
    
    delete_publication(session=db, db_publication=publication)
    
    deleted = get_publication_by_id(session=db, publication_id=pub_id)
    assert deleted is None


def test_search_publications_by_domain(db: Session) -> None:
    """Test searching publications by domain"""
    from app.crud.publication import search_publications_by_domain
    
    researcher = create_random_researcher(db)
    
    # Create publications with different domains
    domains_list = [
        ["AI", "Machine Learning"],
        ["Data Science", "Statistics"],
        ["AI", "Robotics"]
    ]
    
    for i, domains in enumerate(domains_list):
        publication_in = CreatePublication(
            title=f"Publication {i}",
            publisher="Publisher",
            year=2023,
            domains=domains
        )
        create_publication(
            session=db,
            publication_in=publication_in,
            researcher_id=researcher.id
        )
    
    ai_publications = search_publications_by_domain(
        session=db,
        domain="AI",
        skip=0,
        limit=10
    )
    
    assert len(ai_publications) >= 2
    for pub in ai_publications:
        assert "AI" in pub.domains


def test_replace_researcher_publications(db: Session) -> None:
    """Test replacing all publications for a researcher"""
    from app.crud.publication import (
        replace_researcher_publications,
        get_publications_by_researcher
    )
    
    researcher = create_random_researcher(db)
    
    # Create initial publications
    for i in range(2):
        publication_in = CreatePublication(
            title=f"Old Publication {i}",
            publisher="Old Publisher",
            year=2020,
            domains=["Old"]
        )
        create_publication(
            session=db,
            publication_in=publication_in,
            researcher_id=researcher.id
        )
    
    # Replace with new publications
    new_publications = [
        CreatePublication(
            title="New Publication 1",
            publisher="New Publisher",
            year=2024,
            domains=["New"]
        ),
        CreatePublication(
            title="New Publication 2",
            publisher="New Publisher",
            year=2024,
            domains=["New"]
        ),
        CreatePublication(
            title="New Publication 3",
            publisher="New Publisher",
            year=2024,
            domains=["New"]
        )
    ]
    
    replaced = replace_researcher_publications(
        session=db,
        researcher_id=researcher.id,
        publications_in=new_publications
    )
    
    assert len(replaced) == 3
    assert all("New" in pub.domains for pub in replaced)
    
    # Verify old publications are gone
    all_pubs = get_publications_by_researcher(
        session=db,
        researcher_id=researcher.id
    )
    assert len(all_pubs) == 3
    assert all(pub.year == 2024 for pub in all_pubs)


def test_publication_domains_as_list(db: Session) -> None:
    """Test that domains are properly stored and retrieved as lists"""
    researcher = create_random_researcher(db)
    
    publication_in = CreatePublication(
        title="Multi-domain Publication",
        publisher="Publisher",
        year=2023,
        domains=["AI", "Machine Learning", "Deep Learning", "NLP"]
    )
    
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )
    
    assert isinstance(publication.domains, list)
    assert len(publication.domains) == 4
    assert "AI" in publication.domains
    assert "NLP" in publication.domains
