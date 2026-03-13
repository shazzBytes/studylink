import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.project import get_project_by_id
from app.crud.project_member import (
    add_project_member,
    get_project_members,
    is_project_member,
    remove_project_member,
)
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberPublic

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)



@router.get("/{project_id}/members", response_model=list[ProjectMemberPublic])
def get_project_members_route(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    current_user: CurrentUser
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
    current_user: CurrentUser
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
    current_user: CurrentUser
):
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can remove members")

    success = remove_project_member(
        session=session,
        project_id=project_id,
        user_id=user_id,
    )
    if user_id == project.owner_id:
        raise HTTPException(status_code=400, detail="Owner cannot be removed")

    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return None


