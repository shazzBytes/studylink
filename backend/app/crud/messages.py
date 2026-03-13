import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.crud.chats import get_visible_windows
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


def create_message(
    *,
    session: Session,
    chat: Chat,
    sender_id: uuid.UUID,
    message_in: MessageCreate,
) -> Message:
    db_obj = Message(
        chat_id=chat.id,
        sender_id=sender_id,
        content=message_in.content,
        attachments=message_in.attachments,
    )
    session.add(db_obj)

    # Keep chat preview fields in sync with latest message.
    chat.last_message = message_in.content
    chat.updated_at = get_datetime_utc()
    session.add(chat)

    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_message_by_id(
    *, session: Session, chat: Chat, user_id: uuid.UUID, message_id: uuid.UUID
) -> Message | None:
    statement = (
        select(Message)
        .where(Message.id == message_id)
        .where(Message.chat_id == chat.id)
        .where(Message.is_deleted == False)  # noqa: E712
    )
    message = session.exec(statement).first()
    if not message:
        return None
    return message if message_visible_to_user(chat=chat, user_id=user_id, message=message) else None


def message_visible_to_user(*, chat: Chat, user_id: uuid.UUID, message: Message) -> bool:
    for start, end in get_visible_windows(chat, user_id):
        if message.created_at is None:
            return True
        if message.created_at >= start and (end is None or message.created_at <= end):
            return True
    return False


def list_messages_for_chat(
    *,
    session: Session,
    chat: Chat,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 50,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.chat_id == chat.id)
        .where(Message.is_deleted == False)  # noqa: E712
        .order_by(Message.created_at)
    )
    messages = [
        message
        for message in session.exec(statement).all()
        if message_visible_to_user(chat=chat, user_id=user_id, message=message)
    ]
    return messages[skip : skip + limit]


def count_messages_for_chat(*, session: Session, chat: Chat, user_id: uuid.UUID) -> int:
    statement = (
        select(Message)
        .where(Message.chat_id == chat.id)
        .where(Message.is_deleted == False)  # noqa: E712
    )
    return sum(
        1
        for message in session.exec(statement).all()
        if message_visible_to_user(chat=chat, user_id=user_id, message=message)
    )


def update_message(
    *, session: Session, db_message: Message, message_in: MessageUpdate
) -> Message:
    update_data = message_in.model_dump(exclude_unset=True)
    update_data["updated_at"] = get_datetime_utc()
    db_message.sqlmodel_update(update_data)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def delete_message(*, session: Session, db_message: Message) -> None:
    db_message.is_deleted = True
    db_message.updated_at = get_datetime_utc()
    session.add(db_message)
    session.commit()
