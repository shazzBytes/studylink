import uuid
from datetime import datetime, timezone

from sqlalchemy import String, cast
from sqlmodel import Session, func, select

from app.models.chat import Chat, ChatType
from app.models.users import User
from app.schemas.chat import CreateChat, UpdateChat


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


def participant_membership_filter(user_id: uuid.UUID):
    return cast(Chat.participants, String).like(f'%"{user_id}"%')


def serialize_datetime(value: datetime) -> str:
    return value.isoformat()


def deserialize_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def ensure_member_states(chat: Chat) -> dict[str, list[dict[str, str | None]]]:
    if chat.member_states:
        return chat.member_states

    joined_at = serialize_datetime(chat.created_at or get_datetime_utc())
    chat.member_states = {
        participant_id: [{"start": joined_at, "end": None}]
        for participant_id in chat.participants
    }
    return chat.member_states


def is_chat_active_for_user(chat: Chat, user_id: uuid.UUID) -> bool:
    member_states = ensure_member_states(chat)
    windows = member_states.get(str(user_id), [])
    return bool(windows and windows[-1].get("end") is None)


def get_visible_windows(chat: Chat, user_id: uuid.UUID) -> list[tuple[datetime, datetime | None]]:
    member_states = ensure_member_states(chat)
    visible_windows: list[tuple[datetime, datetime | None]] = []

    for window in member_states.get(str(user_id), []):
        start = deserialize_datetime(window.get("start"))
        if not start:
            continue
        visible_windows.append((start, deserialize_datetime(window.get("end"))))

    return visible_windows


def normalize_chat_participants(
    *,
    session: Session,
    participant_ids: list[str],
    minimum_participants: int = 1,
) -> list[str]:
    normalized_ids: list[uuid.UUID] = []
    invalid_ids: list[str] = []

    for participant_id in participant_ids:
        try:
            parsed_id = uuid.UUID(str(participant_id))
        except (TypeError, ValueError):
            invalid_ids.append(str(participant_id))
            continue
        if parsed_id not in normalized_ids:
            normalized_ids.append(parsed_id)

    if len(normalized_ids) < minimum_participants:
        raise ValueError("A conversation must include at least one other participant")

    users = session.exec(
        select(User).where(User.id.in_(normalized_ids)).where(User.is_active == True)  # noqa: E712
    ).all()
    valid_user_ids = {user.id for user in users}

    missing_ids = [str(participant_id) for participant_id in normalized_ids if participant_id not in valid_user_ids]
    if invalid_ids or missing_ids:
        raise ValueError("One or more selected participants are invalid")

    return [str(participant_id) for participant_id in normalized_ids]


def derive_chat_type(participants: list[str]) -> ChatType:
    return ChatType.dm if len(participants) == 2 else ChatType.group


def list_chat_contacts(
    *, session: Session, current_user_id: uuid.UUID, q: str | None = None, limit: int = 20
) -> list[User]:
    statement = (
        select(User)
        .where(User.id != current_user_id)
        .where(User.is_active == True)  # noqa: E712
        .order_by(User.full_name, User.email)
        .limit(limit)
    )

    if q:
        like_query = f"%{q.strip()}%"
        statement = statement.where(
            (User.full_name.ilike(like_query)) | (User.email.ilike(like_query))
        )

    return list(session.exec(statement).all())


def create_chat(*, session: Session, user_id: uuid.UUID, chat_in: CreateChat) -> Chat:
    """Create a new chat record."""
    created_at = get_datetime_utc()
    participants = normalize_chat_participants(
        session=session,
        participant_ids=[str(user_id), *chat_in.participants],
        minimum_participants=2,
    )
    member_states = {
        participant_id: [{"start": serialize_datetime(created_at), "end": None}]
        for participant_id in participants
    }
    db_obj = Chat(
        user_id=user_id,
        chat_type=derive_chat_type(participants),
        title=chat_in.title,
        participants=participants,
        member_states=member_states,
        created_at=created_at,
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
        .where(participant_membership_filter(user_id))
        .where(Chat.is_deleted == False)  # noqa: E712
    )
    chat = session.exec(statement).first()
    if not chat:
        return None
    if not is_chat_active_for_user(chat, user_id):
        return None
    return chat


def list_chats_for_user(
    *, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 50
) -> list[Chat]:
    """List chats where the current user is a participant."""
    statement = (
        select(Chat)
        .where(participant_membership_filter(user_id))
        .where(Chat.is_deleted == False)  # noqa: E712
        .order_by(Chat.updated_at.desc(), Chat.created_at.desc())
    )
    chats = list(session.exec(statement).all())
    active_chats = [chat for chat in chats if is_chat_active_for_user(chat, user_id)]
    return active_chats[skip : skip + limit]


def count_chats_for_user(*, session: Session, user_id: uuid.UUID) -> int:
    statement = (
        select(Chat)
        .where(participant_membership_filter(user_id))
        .where(Chat.is_deleted == False)  # noqa: E712
    )
    chats = list(session.exec(statement).all())
    return sum(1 for chat in chats if is_chat_active_for_user(chat, user_id))


def update_chat(
    *, session: Session, db_chat: Chat, chat_in: UpdateChat, actor_id: uuid.UUID
) -> Chat:
    """Update fields on an existing chat."""
    update_data = chat_in.model_dump(exclude_unset=True)
    if "participants" in update_data:
        participants = normalize_chat_participants(
            session=session,
            participant_ids=[str(actor_id), *update_data["participants"]],
        )
        update_data["participants"] = participants
        member_states = ensure_member_states(db_chat)
        active_participants = set(participants)
        now = serialize_datetime(get_datetime_utc())

        for participant_id in participants:
            windows = member_states.setdefault(participant_id, [])
            if not windows or windows[-1].get("end") is not None:
                windows.append({"start": now, "end": None})

        for participant_id, windows in member_states.items():
            if participant_id in active_participants:
                continue
            if windows and windows[-1].get("end") is None:
                windows[-1]["end"] = now

        update_data["member_states"] = member_states
        update_data["chat_type"] = derive_chat_type(participants)
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


def leave_chat(*, session: Session, db_chat: Chat, user_id: uuid.UUID) -> Chat:
    member_states = ensure_member_states(db_chat)
    user_windows = member_states.get(str(user_id), [])
    if not user_windows or user_windows[-1].get("end") is not None:
        raise ValueError("You are no longer an active participant in this chat")

    now = serialize_datetime(get_datetime_utc())
    user_windows[-1]["end"] = now
    db_chat.participants = [
        participant_id
        for participant_id in db_chat.participants
        if participant_id != str(user_id)
    ]
    db_chat.member_states = member_states
    db_chat.updated_at = deserialize_datetime(now)
    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)
    return db_chat


def report_chat(*, session: Session, db_chat: Chat, user_id: uuid.UUID) -> Chat:
    if str(user_id) not in db_chat.reported_by:
        db_chat.reported_by = [*db_chat.reported_by, str(user_id)]
    db_chat.updated_at = get_datetime_utc()
    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)
    return db_chat
