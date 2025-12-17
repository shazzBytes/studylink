import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.publication import Publication, PublicationRole
from app.schemas.publications import CreatePublication, UpdatePublication
from app.crud import (
    get_publication_by_id,
    create_publication,
    update_publication,
    delete_publication,
    get_publication_member,
)

router = APIRouter(
    prefix="/publications",
    tags=["Publications"],
)

@router.get("/{publication_id}", response_model=Publication)
def get_publication_route(
    *,
    session: Session = Depends(get_session),
    publication_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
):
    publication = get_publication_by_id(
        session=session,
        publication_id=publication_id,
    )
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    member = get_publication_member(
        session=session,
        publication_id=publication_id,
        user_id=current_user.id,
    )
    if not member:
        raise HTTPException(status_code=403, detail="Not authorized")

    return publication
