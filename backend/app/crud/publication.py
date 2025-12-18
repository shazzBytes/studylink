import uuid
from sqlmodel import Session, select, col
from app.models.publication import Publication
from app.schemas.publications import CreatePublication, UpdatePublication
from datetime import datetime

def create_publication(
    *,
    session: Session,
    publication_in: CreatePublication,
    researcher_id: uuid.UUID,
) -> Publication:
    db_publication = Publication.model_validate(
        publication_in,
        update={"researcher_id": researcher_id},
    )

    session.add(db_publication)
    session.commit()
    session.refresh(db_publication)

    return db_publication

def get_publication_by_id(
    *,
    session: Session,
    publication_id: uuid.UUID,
) -> Publication | None:
    return session.get(Publication, publication_id)

def update_publication(
    *,
    session: Session,
    db_publication: Publication,
    publication_in: UpdatePublication,
) -> Publication:
    update_data = publication_in.model_dump(exclude_unset=True)

    db_publication.sqlmodel_update(update_data)

    session.add(db_publication)
    session.commit()
    session.refresh(db_publication)

    return db_publication

def delete_publication(
    *,
    session: Session,
    db_publication: Publication,
) -> None:
    db_publication.is_deleted = True
    db_publication.deleted_at = datetime.utcnow()

    session.add(db_publication)
    session.commit()

def get_publications_by_researcher(
    *,
    session: Session,
    researcher_id: uuid.UUID,
) -> list[Publication]:
    statement = (
        select(Publication)
        .where(Publication.researcher_id == researcher_id)
        .order_by(col(Publication.year).desc())
    )

    return list(session.exec(statement).all())


def search_publications_by_domain(
    *,
    session: Session,
    domain: str,
    skip: int = 0,
    limit: int = 50,
) -> list[Publication]:
    # For JSON/Array fields, we need to filter differently
    # This will work with SQLModel's list field
    statement = (
        select(Publication)
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()
    # Filter by domain in Python since SQLModel handles this as JSON
    return [pub for pub in results if domain in pub.domains]

def replace_researcher_publications(
    *,
    session: Session,
    researcher_id: uuid.UUID,
    publications_in: list[CreatePublication],
) -> list[Publication]:
    # Delete existing publications
    statement = select(Publication).where(
        Publication.researcher_id == researcher_id
    )
    existing = session.exec(statement).all()

    for pub in existing:
        session.delete(pub)

    session.commit()

    # Create new publications
    new_publications: list[Publication] = []

    for pub_in in publications_in:
        pub = Publication.model_validate(
            pub_in,
            update={"researcher_id": researcher_id},
        )
        session.add(pub)
        new_publications.append(pub)

    session.commit()

    for pub in new_publications:
        session.refresh(pub)

    return new_publications
