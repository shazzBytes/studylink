from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select

from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
)

from app.models import Project, ProjectMember


def create_project(
    *,
    session: Session,
    project_in: ProjectCreate,
    owner_id: UUID,
) -> Project:
    project = Project(
        **project_in.model_dump(),
        owner_id=owner_id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_project_by_id(
    *,
    session: Session,
    project_id: UUID,
) -> Project | None:
    return session.exec(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.is_deleted == False)
    ).first()

def get_projects_for_user(
    *,
    session: Session,
    user_id: UUID,
) -> list[Project]:
    return session.exec(
        select(Project)
        .where(Project.is_deleted == False)
        .where(Project.owner_id == user_id)
    ).all()

def update_project(
    *,
    session: Session,
    project: Project,
    project_in: ProjectUpdate,
) -> Project:
    data = project_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def delete_project(
    *,
    session: Session,
    project: Project,
) -> None:
    project.is_deleted = True
    project.deleted_at = datetime.utcnow()
    session.add(project)
    session.commit()


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
