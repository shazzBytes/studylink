import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.chats import get_chat_by_id
from app.crud.messages import (
    count_messages_for_chat,
    create_message,
    delete_message,
    get_message_by_id,
    list_messages_for_chat,
    update_message,
)
from app.models.auth import Message
from app.realtime.chat_events import chat_event_manager
from app.schemas.chat import ChatPublic
from app.schemas.message import (
    MessageCreate,
    MessagePublic,
    MessagesPublic,
    MessageUpdate,
)

router = APIRouter(prefix="/chats/{chat_id}/messages", tags=["messages"])


def serialize_chat(chat: Any) -> dict[str, Any]:
    return ChatPublic.model_validate(chat).model_dump(mode="json")


def serialize_message(message: Any) -> dict[str, Any]:
    return MessagePublic.model_validate(message).model_dump(mode="json")


@router.get("/", response_model=MessagesPublic)
def read_messages(
    *,
    chat_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 50,
) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = list_messages_for_chat(
        session=session,
        chat=chat,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    count = count_messages_for_chat(session=session, chat=chat, user_id=current_user.id)
    return MessagesPublic(data=messages, count=count)


@router.get("/{message_id}", response_model=MessagePublic)
def read_message(
    *,
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = get_message_by_id(
        session=session,
        chat=chat,
        user_id=current_user.id,
        message_id=message_id,
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessagePublic)
def create_message_route(
    *,
    chat_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    message_in: MessageCreate,
) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = create_message(
        session=session,
        chat=chat,
        sender_id=current_user.id,
        message_in=message_in,
    )
    chat_event_manager.broadcast_to_users(
        user_ids=chat.participants,
        event={
            "type": "message.created",
            "chat": serialize_chat(chat),
            "message": serialize_message(message),
        },
    )
    return message


@router.patch("/{message_id}", response_model=MessagePublic)
def update_message_route(
    *,
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    message_in: MessageUpdate,
) -> Any:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = get_message_by_id(
        session=session,
        chat=chat,
        user_id=current_user.id,
        message_id=message_id,
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return update_message(session=session, db_message=message, message_in=message_in)


@router.delete("/{message_id}", response_model=Message)
def delete_message_route(
    *,
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
) -> Message:
    chat = get_chat_by_id(session=session, chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    message = get_message_by_id(
        session=session,
        chat=chat,
        user_id=current_user.id,
        message_id=message_id,
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    delete_message(session=session, db_message=message)
    return Message(message="Message deleted successfully")
