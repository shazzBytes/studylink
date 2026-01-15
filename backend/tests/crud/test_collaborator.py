import uuid

import pytest
from sqlmodel import Session

from app.crud.collaborator import (
    add_researcher_collaborator,
    remove_researcher_collaborator,
    get_researcher_collaborators,
)
from tests.utils.researcher import create_random_researcher


def test_add_researcher_collaborator(db: Session) -> None:
    """Test adding a collaborator to a researcher"""
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    
    link = add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    assert link.researcher_id == researcher1.id
    assert link.collaborator_id == researcher2.id


def test_add_researcher_collaborator_prevents_self_collaboration(
    db: Session
) -> None:
    """Test that a researcher cannot collaborate with themselves"""
    researcher = create_random_researcher(db)
    
    with pytest.raises(ValueError, match="cannot collaborate with themselves"):
        add_researcher_collaborator(
            session=db,
            researcher_id=researcher.id,
            collaborator_id=researcher.id
        )


def test_add_researcher_collaborator_prevents_duplicates(db: Session) -> None:
    """Test that duplicate collaborations return the existing link"""
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    
    link1 = add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    link2 = add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    assert link1.researcher_id == link2.researcher_id
    assert link1.collaborator_id == link2.collaborator_id


def test_remove_researcher_collaborator(db: Session) -> None:
    """Test removing a collaborator"""
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    
    add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    remove_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    collaborators = get_researcher_collaborators(
        session=db,
        researcher_id=researcher1.id
    )
    
    assert len(collaborators) == 0


def test_remove_nonexistent_collaborator(db: Session) -> None:
    """Test removing a collaborator that doesn't exist"""
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    
    # Should not raise an error
    remove_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )


def test_get_researcher_collaborators(db: Session) -> None:
    """Test retrieving all collaborators for a researcher"""
    researcher = create_random_researcher(db)
    
    # Add multiple collaborators
    collaborators = []
    for _ in range(3):
        collab = create_random_researcher(db)
        collaborators.append(collab)
        add_researcher_collaborator(
            session=db,
            researcher_id=researcher.id,
            collaborator_id=collab.id
        )
    
    retrieved = get_researcher_collaborators(
        session=db,
        researcher_id=researcher.id
    )
    
    assert len(retrieved) == 3
    retrieved_ids = {c.id for c in retrieved}
    expected_ids = {c.id for c in collaborators}
    assert retrieved_ids == expected_ids


def test_get_researcher_collaborators_empty(db: Session) -> None:
    """Test getting collaborators when there are none"""
    researcher = create_random_researcher(db)
    
    collaborators = get_researcher_collaborators(
        session=db,
        researcher_id=researcher.id
    )
    
    assert len(collaborators) == 0


def test_bidirectional_collaboration(db: Session) -> None:
    """Test that collaboration can be set up bidirectionally"""
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    
    # Add researcher2 as collaborator of researcher1
    add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id
    )
    
    # Add researcher1 as collaborator of researcher2
    add_researcher_collaborator(
        session=db,
        researcher_id=researcher2.id,
        collaborator_id=researcher1.id
    )
    
    # Both should have each other as collaborators
    collab1 = get_researcher_collaborators(
        session=db,
        researcher_id=researcher1.id
    )
    collab2 = get_researcher_collaborators(
        session=db,
        researcher_id=researcher2.id
    )
    
    assert len(collab1) == 1
    assert collab1[0].id == researcher2.id
    
    assert len(collab2) == 1
    assert collab2[0].id == researcher1.id


def test_collaborator_added_by_tracking(db: Session) -> None:
    """Test that we can track who added a collaborator"""
    from tests.utils.user import create_random_user
    
    researcher1 = create_random_researcher(db)
    researcher2 = create_random_researcher(db)
    user = create_random_user(db)
    
    link = add_researcher_collaborator(
        session=db,
        researcher_id=researcher1.id,
        collaborator_id=researcher2.id,
        added_by=user.id
    )
    
    assert link.added_by == user.id
    assert link.added_at is not None
