import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.chats import (
    count_chats_for_user,
    create_chat,
    delete_chat,
    get_chat_by_id,
    list_chats_for_user,
    update_chat,
)
from app.models.auth import Message
from app.schemas.chat import ChatPublic, ChatsPublic, CreateChat, UpdateChat

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/", response_model=ChatsPublic)
def read_chats(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 50
) -> Any:
    chats = list_chats_for_user(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    count = count_chats_for_user(session=session, user_id=current_user.id)
    return ChatsPublic(data=chats, count=count)


@router.get("/{chat_id}", response_model=ChatPublic)
def read_chat(chat_id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ChatPublic)
def create_chat_route(
    *, session: SessionDep, current_user: CurrentUser, chat_in: CreateChat
) -> Any:
    return create_chat(session=session, user_id=current_user.id, chat_in=chat_in)


@router.patch("/{chat_id}", response_model=ChatPublic)
def update_chat_route(
    *,
    chat_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    chat_in: UpdateChat,
) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return update_chat(session=session, db_chat=chat, chat_in=chat_in)


@router.delete("/{chat_id}", response_model=Message)
def delete_chat_route(
    chat_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Message:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    delete_chat(session=session, db_chat=chat)
    return Message(message="Chat deleted successfully")
