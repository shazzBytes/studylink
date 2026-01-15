import uuid
from sqlmodel import Session, select
from app.models.publication_member import PublicationMember
from app.models.publication import PublicationRole

def get_publication_member(*,session: Session,publication_id: uuid.UUID,user_id: uuid.UUID,) -> PublicationMember | None:
    statement = select(PublicationMember).where(
        PublicationMember.publication_id == publication_id,
        PublicationMember.user_id == user_id,
    )
    return session.exec(statement).first()

def add_publication_member(*,session: Session,publication_id: uuid.UUID,user_id: uuid.UUID,role: PublicationRole,added_by: uuid.UUID,) -> PublicationMember:
    member = PublicationMember(
        publication_id=publication_id,
        user_id=user_id,
        role=role,
        added_by=added_by,
    )
    session.add(member)
    session.commit()
    return member

def remove_publication_member(*,session: Session,publication_id: uuid.UUID,user_id: uuid.UUID,) -> None:
    statement = select(PublicationMember).where(
        PublicationMember.publication_id == publication_id,
        PublicationMember.user_id == user_id,
    )
    member = session.exec(statement).first()
    if member:
        session.delete(member)
        session.commit()



