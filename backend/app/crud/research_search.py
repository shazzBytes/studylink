from sqlmodel import Session, col, select

from app.models.researcher import ResearcherInfo


def search_researchers(
    *,
    session: Session,
    q: str | None = None,
    institute: str | None = None,
    qualification: str | None = None,
    domain: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[ResearcherInfo]:
    statement = select(ResearcherInfo)

    if q:
        statement = statement.where(
            col(ResearcherInfo.full_name).ilike(f"%{q}%")
            | col(ResearcherInfo.email).ilike(f"%{q}%")
            | col(ResearcherInfo.bio).ilike(f"%{q}%")
        )

    if institute:
        statement = statement.where(col(ResearcherInfo.institute).ilike(f"%{institute}%"))

    if qualification:
        statement = statement.where(
            col(ResearcherInfo.qualification).ilike(f"%{qualification}%")
        )

    # Kept for API compatibility, not persisted in current schema.
    if domain:
        statement = statement.where(col(ResearcherInfo.bio).ilike(f"%{domain}%"))

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())
