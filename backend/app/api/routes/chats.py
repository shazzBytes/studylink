import uuid
from typing import Any

import jwt
from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.api.deps import CurrentUser, SessionDep
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.crud.chats import (
    count_chats_for_user,
    create_chat,
    delete_chat,
    get_chat_by_id,
    leave_chat,
    list_chat_contacts,
    list_chats_for_user,
    report_chat,
    update_chat,
)
from app.models import TokenPayload, User
from app.models.auth import Message
from app.realtime.chat_events import chat_event_manager
from app.schemas.chat import (
    ChatContactPublic,
    ChatPublic,
    ChatsPublic,
    CreateChat,
    UpdateChat,
)

router = APIRouter(prefix="/chats", tags=["chats"])


def get_user_from_token(*, session: Session, token: str) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.get(User, token_data.sub)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return user


def serialize_chat_event(chat: Any) -> dict[str, Any]:
    return ChatPublic.model_validate(chat).model_dump(mode="json")


@router.websocket("/ws")
async def chats_websocket(websocket: WebSocket, token: str = Query(...)) -> None:
    with Session(engine) as session:
        try:
            user = get_user_from_token(session=session, token=token)
        except HTTPException:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    await chat_event_manager.connect(user_id=user.id, websocket=websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        chat_event_manager.disconnect(user_id=user.id, websocket=websocket)


@router.get("/contacts", response_model=list[ChatContactPublic])
def read_chat_contacts(
    session: SessionDep,
    current_user: CurrentUser,
    q: str | None = None,
    limit: int = 20,
) -> Any:
    return list_chat_contacts(
        session=session,
        current_user_id=current_user.id,
        q=q,
        limit=limit,
    )


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
    try:
        chat = create_chat(session=session, user_id=current_user.id, chat_in=chat_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    chat_event_manager.broadcast_to_users(
        user_ids=chat.participants,
        event={"type": "chat.created", "chat": serialize_chat_event(chat)},
    )
    return chat


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
    previous_participants = list(chat.participants)
    try:
        updated_chat = update_chat(
            session=session,
            db_chat=chat,
            chat_in=chat_in,
            actor_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    chat_event_manager.broadcast_to_users(
        user_ids={*previous_participants, *updated_chat.participants},
        event={"type": "chat.updated", "chat": serialize_chat_event(updated_chat)},
    )
    return updated_chat


@router.delete("/{chat_id}", response_model=Message)
def delete_chat_route(
    chat_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Message:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    participants = list(chat.participants)
    delete_chat(session=session, db_chat=chat)
    chat_event_manager.broadcast_to_users(
        user_ids=participants,
        event={"type": "chat.deleted", "chat_id": str(chat_id)},
    )
    return Message(message="Chat deleted successfully")


@router.post("/{chat_id}/leave", response_model=Message)
def leave_chat_route(
    chat_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Message:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    remaining_participants = list(chat.participants)
    try:
        updated_chat = leave_chat(session=session, db_chat=chat, user_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    chat_event_manager.broadcast_to_users(
        user_ids=[str(current_user.id)],
        event={"type": "chat.left", "chat_id": str(chat_id)},
    )
    chat_event_manager.broadcast_to_users(
        user_ids=[
            participant_id
            for participant_id in remaining_participants
            if participant_id != str(current_user.id)
        ],
        event={"type": "chat.updated", "chat": serialize_chat_event(updated_chat)},
    )
    return Message(message="You left the chat")


@router.post("/{chat_id}/report", response_model=Message)
def report_chat_route(
    chat_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Message:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    report_chat(session=session, db_chat=chat, user_id=current_user.id)
    return Message(message="Chat reported successfully")
