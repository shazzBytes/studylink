import uuid

from sqlmodel import Session

from app.crud.publication import create_publication
from app.crud.publication_member import (
    add_publication_member,
    get_publication_member,
    remove_publication_member,
)
from app.models.publication import PublicationRole
from app.schemas.publications import CreatePublication
from tests.utils.researcher import create_random_researcher
from tests.utils.user import create_random_user


def test_add_publication_member(db: Session) -> None:
    """Test adding a member to a publication"""
    researcher = create_random_researcher(db)
    user = create_random_user(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Test Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    member = add_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id,
        role=PublicationRole.editor,
        added_by=added_by_user.id
    )

    assert member.publication_id == publication.id
    assert member.user_id == user.id
    assert member.role == PublicationRole.editor
    assert member.added_by == added_by_user.id


def test_get_publication_member(db: Session) -> None:
    """Test retrieving a publication member"""
    researcher = create_random_researcher(db)
    user = create_random_user(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    add_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id,
        role=PublicationRole.viewer,
        added_by=added_by_user.id
    )

    member = get_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id
    )

    assert member is not None
    assert member.user_id == user.id
    assert member.role == PublicationRole.viewer


def test_get_publication_member_not_found(db: Session) -> None:
    """Test getting a non-existent publication member"""
    publication_id = uuid.uuid4()
    user_id = uuid.uuid4()

    member = get_publication_member(
        session=db,
        publication_id=publication_id,
        user_id=user_id
    )

    assert member is None


def test_remove_publication_member(db: Session) -> None:
    """Test removing a member from a publication"""
    researcher = create_random_researcher(db)
    user = create_random_user(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    add_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id,
        role=PublicationRole.editor,
        added_by=added_by_user.id
    )

    remove_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id
    )

    member = get_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id
    )

    assert member is None


def test_remove_nonexistent_publication_member(db: Session) -> None:
    """Test removing a member that doesn't exist"""
    publication_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Should not raise an error
    remove_publication_member(
        session=db,
        publication_id=publication_id,
        user_id=user_id
    )


def test_publication_member_roles(db: Session) -> None:
    """Test different publication member roles"""
    researcher = create_random_researcher(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    # Test different roles
    roles = [
        (create_random_user(db).id, PublicationRole.owner),
        (create_random_user(db).id, PublicationRole.editor),
        (create_random_user(db).id, PublicationRole.viewer),
    ]

    for user_id, role in roles:
        member = add_publication_member(
            session=db,
            publication_id=publication.id,
            user_id=user_id,
            role=role,
            added_by=added_by_user.id
        )
        assert member.role == role


def test_multiple_members_on_publication(db: Session) -> None:
    """Test adding multiple members to the same publication"""
    researcher = create_random_researcher(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    # Add multiple members
    user_ids = [create_random_user(db).id for _ in range(3)]

    for user_id in user_ids:
        add_publication_member(
            session=db,
            publication_id=publication.id,
            user_id=user_id,
            role=PublicationRole.viewer,
            added_by=added_by_user.id
        )

    # Verify all members exist
    for user_id in user_ids:
        member = get_publication_member(
            session=db,
            publication_id=publication.id,
            user_id=user_id
        )
        assert member is not None


def test_publication_member_added_at_timestamp(db: Session) -> None:
    """Test that added_at timestamp is set automatically"""
    researcher = create_random_researcher(db)
    user = create_random_user(db)
    added_by_user = create_random_user(db)

    publication_in = CreatePublication(
        title="Test Publication",
        publisher="Publisher",
        year=2023,
        domains=["Test"]
    )
    publication = create_publication(
        session=db,
        publication_in=publication_in,
        researcher_id=researcher.id
    )

    member = add_publication_member(
        session=db,
        publication_id=publication.id,
        user_id=user.id,
        role=PublicationRole.editor,
        added_by=added_by_user.id
    )

    assert member.added_at is not None
