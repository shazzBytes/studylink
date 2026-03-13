from sqlmodel import Session, col, select

from app.models.publication import Publication


def search_publications(
    *,
    session: Session,
    q: str | None = None,
    domain: str | None = None,
    keyword: str | None = None,
    publisher: str | None = None,
    year: int | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Publication]:
    statement = select(Publication)

    if q:
        statement = statement.where(
            col(Publication.title).ilike(f"%{q}%")
            | col(Publication.description).ilike(f"%{q}%")
        )

    if domain:
        rows = list(session.exec(statement).all())
        rows = [pub for pub in rows if domain in pub.domains]
        statement = select(Publication).where(Publication.id.in_([row.id for row in rows]))

    # Kept for API compatibility, mapped to description search in current schema.
    if keyword:
        statement = statement.where(col(Publication.description).ilike(f"%{keyword}%"))

    if publisher:
        statement = statement.where(col(Publication.publisher).ilike(f"%{publisher}%"))

    if year:
        statement = statement.where(Publication.year == year)

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())
