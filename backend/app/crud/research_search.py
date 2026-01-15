from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy import or_

from app.models.researcher import ResearcherInfo


def search_researchers(*,session: Session,q: Optional[str] = None,institute: Optional[str] = None,qualification: Optional[str] = None,domain: Optional[str] = None,skip: int = 0,limit: int = 20,) -> List[ResearcherInfo]:
    """
    Academic-grade researcher search.

    - Partial matching
    - Domain-based discovery
    - Visibility-aware
    - Soft-delete safe
    """

    statement = select(ResearcherInfo).where(
        ResearcherInfo.is_deleted == False,
        ResearcherInfo.is_public == True,
    )

    # 🔍 Free-text search
    if q:
        statement = statement.where(
            or_(
                ResearcherInfo.full_name.ilike(f"%{q}%"),
                ResearcherInfo.bio.ilike(f"%{q}%"),
                ResearcherInfo.expertise_keywords.any(q),
            )
        )

    # 🏫 Institute filter
    if institute:
        statement = statement.where(
            ResearcherInfo.institute.ilike(f"%{institute}%")
        )

    # 🎓 Qualification filter
    if qualification:
        statement = statement.where(
            ResearcherInfo.qualification.ilike(f"%{qualification}%")
        )

    # 🧠 Domain / research interest filter
    if domain:
        statement = statement.where(
            ResearcherInfo.research_interests.any(domain)
        )

    # 📊 Pagination
    statement = statement.offset(skip).limit(limit)

    return list(session.exec(statement).all())
