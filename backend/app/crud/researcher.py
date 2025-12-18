import uuid
from sqlmodel import Session, select, col
from datetime import datetime

from app.models.researcher import ResearcherInfo
from app.schemas.researcher import (
    CreateResearcherInfo,
    UpdateResearcherInfo,
)

def create_researcher(
    *,
    session: Session,
    researcher_in: CreateResearcherInfo,
) -> ResearcherInfo:
    db_researcher = ResearcherInfo.model_validate(researcher_in)

    session.add(db_researcher)
    session.commit()
    session.refresh(db_researcher)

    return db_researcher

def get_researcher_by_id(
    *,
    session: Session,
    researcher_id: uuid.UUID,
) -> ResearcherInfo | None:
    return session.get(ResearcherInfo, researcher_id)

def get_researcher_by_email(
    *,
    session: Session,
    researcher_email: str,
) -> ResearcherInfo | None:
    statement = select(ResearcherInfo).where(
        ResearcherInfo.email == researcher_email
    )
    return session.exec(statement).first()

def update_researcher(
    *,
    session: Session,
    db_researcher: ResearcherInfo,
    researcher_in: UpdateResearcherInfo,
) -> ResearcherInfo:
    update_data = researcher_in.model_dump(exclude_unset=True)

    db_researcher.sqlmodel_update(update_data)

    session.add(db_researcher)
    session.commit()
    session.refresh(db_researcher)

    return db_researcher


def delete_researcher(
    *,
    session: Session,
    db_researcher: ResearcherInfo,
) -> None:
    db_researcher.is_deleted = True
    db_researcher.deleted_at = datetime.utcnow()

    session.add(db_researcher)
    session.commit()

def search_researchers(
    *,
    session: Session,
    full_name: str | None = None,
    email: str | None = None,
    institute: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[ResearcherInfo]:
    statement = select(ResearcherInfo)

    if full_name:
        statement = statement.where(
            col(ResearcherInfo.full_name).ilike(f"%{full_name}%")
        )

    if email:
        statement = statement.where(
            col(ResearcherInfo.email).ilike(f"%{email}%")
        )

    if institute:
        statement = statement.where(
            col(ResearcherInfo.institute).ilike(f"%{institute}%")
        )

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())

