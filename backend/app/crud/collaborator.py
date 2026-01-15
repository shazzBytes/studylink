import uuid
from sqlmodel import Session, select

from app.models.collaborator import ResearcherCollaborator
from app.models.researcher import ResearcherInfo

def add_researcher_collaborator(
    *,
    session: Session,
    researcher_id: uuid.UUID,
    collaborator_id: uuid.UUID,
    added_by: uuid.UUID | None = None,
) -> ResearcherCollaborator:
    # Prevent self-collaboration
    if researcher_id == collaborator_id:
        raise ValueError("Researcher cannot collaborate with themselves")

    # Prevent duplicates
    statement = select(ResearcherCollaborator).where(
        ResearcherCollaborator.researcher_id == researcher_id,
        ResearcherCollaborator.collaborator_id == collaborator_id,
    )
    existing = session.exec(statement).first()
    if existing:
        return existing

    link = ResearcherCollaborator(
        researcher_id=researcher_id,
        collaborator_id=collaborator_id,
        added_by=added_by,
    )

    session.add(link)
    session.commit()
    session.refresh(link)

    return link

def remove_researcher_collaborator(
    *,
    session: Session,
    researcher_id: uuid.UUID,
    collaborator_id: uuid.UUID,
) -> None:
    statement = select(ResearcherCollaborator).where(
        ResearcherCollaborator.researcher_id == researcher_id,
        ResearcherCollaborator.collaborator_id == collaborator_id,
    )

    link = session.exec(statement).first()
    if link:
        session.delete(link)
        session.commit()

def get_researcher_collaborators(
    *,
    session: Session,
    researcher_id: uuid.UUID,
) -> list[ResearcherInfo]:
    statement = (
        select(ResearcherInfo)
        .join(
            ResearcherCollaborator,
            ResearcherCollaborator.collaborator_id == ResearcherInfo.id
        )
        .where(
            ResearcherCollaborator.researcher_id == researcher_id
        )
    )

    return list(session.exec(statement).all())
