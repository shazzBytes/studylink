import uuid
from datetime import datetime, timezone

from sqlmodel import Session, func, select

from app.models.chat import Chat
from app.schemas.chat import CreateChat, UpdateChat


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


def create_chat(*, session: Session, user_id: uuid.UUID, chat_in: CreateChat) -> Chat:
    """Create a new chat record."""
    participants = list(dict.fromkeys([str(user_id), *chat_in.participants]))
    db_obj = Chat(
        user_id=user_id,
        title=chat_in.title,
        participants=participants,
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_chat_by_id(
    *, session: Session, chat_id: uuid.UUID, user_id: uuid.UUID
) -> Chat | None:
    """Return a chat by its ID or None if not found."""
    statement = (
        select(Chat)
        .where(Chat.id == chat_id)
        .where(Chat.user_id == user_id)
        .where(Chat.is_deleted == False)  # noqa: E712
    )
    return session.exec(statement).first()


def list_chats_for_user(
    *, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 50
) -> list[Chat]:
    """List chats belonging to a user with pagination."""
    statement = (
        select(Chat)
        .where(Chat.user_id == user_id)
        .where(Chat.is_deleted == False)  # noqa: E712
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_chats_for_user(*, session: Session, user_id: uuid.UUID) -> int:
    statement = (
        select(func.count())
        .select_from(Chat)
        .where(Chat.user_id == user_id)
        .where(Chat.is_deleted == False)  # noqa: E712
    )
    return int(session.exec(statement).one())


def update_chat(*, session: Session, db_chat: Chat, chat_in: UpdateChat) -> Chat:
    """Update fields on an existing chat."""
    update_data = chat_in.model_dump(exclude_unset=True)
    if "participants" in update_data:
        participants = list(
            dict.fromkeys([str(db_chat.user_id), *update_data["participants"]])
        )
        update_data["participants"] = participants
    update_data["updated_at"] = get_datetime_utc()
    db_chat.sqlmodel_update(update_data)
    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)
    return db_chat


def delete_chat(*, session: Session, db_chat: Chat) -> None:
    """Soft-delete a chat (mark as deleted)."""
    db_chat.is_deleted = True
    db_chat.updated_at = get_datetime_utc()
    session.add(db_chat)
    session.commit()
