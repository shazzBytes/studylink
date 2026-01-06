import uuid
from sqlmodel import Session, select
from app.models.chats import Room, RoomMembers, ConversationType

def create_direct_message_chat(*, session: Session, created_by: uuid.UUID) -> Room:
    chat = Room(type=ConversationType.DIRECT, created_by=created_by)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat