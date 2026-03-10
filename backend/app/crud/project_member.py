from uuid import UUID

from sqlmodel import Session, select

from app.models import ProjectMember


def get_project_members(
    *,
    session: Session,
    project_id: UUID,
) -> list[ProjectMember]:
    return session.exec(
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
    ).all()



def is_project_member(
    *,
    session: Session,
    project_id: UUID,
    user_id: UUID,
) -> bool:
    return session.exec(
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .where(ProjectMember.user_id == user_id)
    ).first() is not None




def add_project_member(
    *,
    session: Session,
    project_id: UUID,
    user_id: UUID,
    role: str = "viewer",
) -> None:
    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role,
    )
    session.add(member)
    session.commit()




def remove_project_member(
    *,
    session: Session,
    project_id: UUID,
    user_id: UUID,
) -> bool:
    member = session.exec(
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .where(ProjectMember.user_id == user_id)
    ).first()

    if not member:
        return False

    session.delete(member)
    session.commit()
    return True
