from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy import or_, desc

from app.models.publication import Publication


def search_publications(*,session: Session,q: Optional[str] = None,domain: Optional[str] = None,keyword: Optional[str] = None,publisher: Optional[str] = None,year: Optional[int] = None,skip: int = 0,limit: int = 20,) -> List[Publication]:
    """
    Academic-grade publication search.

    - Title / abstract / keyword matching
    - Domain-based filtering
    - Soft-delete safe
    - Ordered by recency
    """

    statement = select(Publication).where(
        Publication.is_deleted == False,
    )

    # 🔍 Free-text search
    if q:
        statement = statement.where(
            or_(
                Publication.title.ilike(f"%{q}%"),
                Publication.abstract.ilike(f"%{q}%"),
                Publication.description.ilike(f"%{q}%"),
                Publication.keywords.any(q),
            )
        )

    # 🧠 Domain filter
    if domain:
        statement = statement.where(
            Publication.domains.any(domain)
        )

    # 🏷 Keyword filter (explicit)
    if keyword:
        statement = statement.where(
            Publication.keywords.any(keyword)
        )

    # 🏛 Publisher filter
    if publisher:
        statement = statement.where(
            Publication.publisher.ilike(f"%{publisher}%")
        )

    # 📅 Year filter
    if year:
        statement = statement.where(
            Publication.year == year
        )

    # 📊 Ordering & pagination
    statement = (
        statement
        .order_by(desc(Publication.__table__.c.year))
        .offset(skip)
        .limit(limit)
    )

    return list(session.exec(statement).all())
