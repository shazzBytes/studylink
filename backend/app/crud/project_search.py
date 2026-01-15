from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy import or_, desc

from app.models.project import Project


def search_projects(*,session: Session,q: Optional[str] = None,domain: Optional[str] = None,skip: int = 0,limit: int = 20,) -> List[Project]:
    """
    Academic-grade project search.

    - Title & description matching
    - Domain filtering
    - Public-only visibility
    - Soft-delete safe
    - Ordered by recent activity
    """

    statement = select(Project).where(
        Project.is_deleted == False,
        Project.is_public == True,
    )

    # 🔍 Free-text search
    if q:
        statement = statement.where(
            or_(
                Project.title.ilike(f"%{q}%"),
                Project.description.ilike(f"%{q}%"),
            )
        )

    # 🧠 Domain filter
    if domain:
        statement = statement.where(
            Project.domain.ilike(f"%{domain}%")
        )

    # 📊 Ordering & pagination
    statement = (
        statement
        .order_by(desc(Project.__table__.c.updated_at))
        .offset(skip)
        .limit(limit)
    )

    return list(session.exec(statement).all())
