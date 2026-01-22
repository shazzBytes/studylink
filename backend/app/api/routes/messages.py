import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select, func, Session, col

from app.api.deps import CurrentUser, SessionDep, get_current_user
from app.models.chats import Room, Message, RoomMember
from app.schemas.chat import (
    MessageCreate,
    MessagePublic,
    MessagesPublic,
    RoomPublic,
    RoomCreate,
    RoomMemberCreate,
)

router = APIRouter()


@router.post("/rooms", response_model=RoomPublic)
def create_room(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    room_in: RoomCreate,
) -> Room:
    """Create a new chat room."""
    room = Room(
        type=room_in.type,
        name=room_in.name,
        created_by=current_user.id,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    
    # Add creator as a member
    member = RoomMember(
        room_id=room.id,
        user_id=current_user.id,
    )
    session.add(member)
    session.commit()
    
    return room


@router.get("/rooms", response_model=list[RoomPublic])
def get_my_rooms(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, le=100),
) -> list[Room]:
    """Get all rooms where current user is a member."""
    statement = (
        select(Room)
        .join(RoomMember)
        .where(RoomMember.user_id == current_user.id)
        .where(Room.is_archived == False)
        .order_by(col(Room.last_message_at).desc())
        .offset(skip)
        .limit(limit)
    )
    rooms = session.exec(statement).all()
    return list(rooms)


@router.get("/rooms/{room_id}", response_model=RoomPublic)
def get_room(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    room_id: uuid.UUID,
) -> Room:
    """Get a specific room."""
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Verify user is a member
    membership = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id
        )
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    return room


@router.post("/rooms/{room_id}/members")
def add_room_member(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    room_id: uuid.UUID,
    user_id: uuid.UUID,
) -> dict:
    """Add a member to a room."""
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check if requester is a member (and has permission)
    requester_membership = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id
        )
    ).first()
    
    if not requester_membership:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if user is already a member
    existing = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == user_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")
    
    member = RoomMember(
        room_id=room_id,
        user_id=user_id,
    )
    session.add(member)
    session.commit()
    
    return {"message": "Member added successfully"}


@router.get("/rooms/{room_id}/messages", response_model=MessagesPublic)
def get_room_messages(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    room_id: uuid.UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, le=100),
) -> MessagesPublic:
    """Get messages from a room with pagination."""
    # Verify user is a member
    membership = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id
        )
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    # Get total count
    count_statement = select(func.count()).select_from(Message).where(Message.room_id == room_id)
    total_count = session.exec(count_statement).one()
    
    # Get messages ordered by timestamp descending (most recent first)
    statement = (
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(col(Message.created_at).desc())
        .offset(skip)
        .limit(limit)
    )
    messages = session.exec(statement).all()
    
    # Reverse to get chronological order for display
    messages_list = list(reversed(list(messages)))
    
    return MessagesPublic(data=messages_list, count=total_count)


@router.post("/rooms/{room_id}/messages", response_model=MessagePublic)
def send_message(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    room_id: uuid.UUID,
    content: str,
) -> Message:
    """Send a message to a room (HTTP endpoint, use WebSocket for real-time)."""
    # Verify user is a member
    membership = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == current_user.id
        )
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    message = Message(
        room_id=room_id,
        sender_id=current_user.id,
        content=content,
    )
    session.add(message)
    
    # Update room's last message timestamp
    room = session.get(Room, room_id)
    if room:
        room.last_message_at = message.created_at
        session.add(room)
    
    session.commit()
    session.refresh(message)
    
    return message


@router.delete("/messages/{message_id}")
def delete_message(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    message_id: uuid.UUID,
) -> dict:
    """Delete a message (only by sender)."""
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")
    
    session.delete(message)
    session.commit()
    
    return {"message": "Message deleted successfully"}
