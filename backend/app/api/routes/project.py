import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.project import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects_for_user,
    update_project,
)
from app.crud.project_member import (
    add_project_member,
    get_project_members,
    is_project_member,
    remove_project_member,
)
from app.schemas.project import ProjectCreate, ProjectPublic, ProjectUpdate
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberPublic

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectPublic])
def get_projects_for_current_user_route(
    *,
    session: SessionDep,
    current_user: CurrentUser,
):
    return get_projects_for_user(session=session, user_id=current_user.id)


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
def create_project_route(
    *,
    session: SessionDep,
    project_in: ProjectCreate,
    current_user: CurrentUser,
):
    return create_project(
        session=session,
        project_in=project_in,
        owner_id=current_user.id,
    )


@router.get("/{project_id}", response_model=ProjectPublic)
def get_project_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id and not project.is_public:
        raise HTTPException(status_code=403, detail="Not authorized")

    return project


@router.patch("/{project_id}", response_model=ProjectPublic)
def update_project_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    project_in: ProjectUpdate,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update project")

    return update_project(session=session, project=project, project_in=project_in)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete project")

    delete_project(session=session, project=project)
    return None


@router.get("/{project_id}/members", response_model=list[ProjectMemberPublic])
def get_project_members_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if (
        project.owner_id != current_user.id
        and not is_project_member(
            session=session,
            project_id=project_id,
            user_id=current_user.id,
        )
    ):
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_project_members(session=session, project_id=project_id)


@router.post("/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_project_member_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    member_data: ProjectMemberCreate,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can add members")

    if is_project_member(
        session=session,
        project_id=project_id,
        user_id=member_data.user_id,
    ):
        raise HTTPException(status_code=400, detail="User already a member")

    add_project_member(
        session=session,
        project_id=project_id,
        user_id=member_data.user_id,
        role=member_data.role,
    )

    return {"message": "Member added successfully"}


@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project_member_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: CurrentUser,
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can remove members")

    if user_id == project.owner_id:
        raise HTTPException(status_code=400, detail="Owner cannot be removed")

    success = remove_project_member(
        session=session,
        project_id=project_id,
        user_id=user_id,
    )
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")

    return None
