
from sqlalchemy import desc, or_
from sqlmodel import Session, select

from app.models.project import Project


def search_projects(*,session: Session,q: str | None = None,domain: str | None = None,skip: int = 0,limit: int = 20,) -> list[Project]:
    """
    Academic-grade project search.

    - Title & description matching
    - Domain filtering
    - Public-only visibility
    - Soft-delete safe
    - Ordered by recent activity
    """

    statement = select(Project).where(
        Project.is_deleted.is_(False),
        Project.is_public.is_(True),
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
