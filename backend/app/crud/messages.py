import uuid
from datetime import datetime
from sqlmodel import Session, select, func, or_, and_
from fastapi import HTTPException

from app.models.chats import (
    Room,
    RoomMember,
    RoomAdmin,
    Message,
    MessageReaction,
    MessageAttachment,
    ConversationType,
    MemberStatus,
    MessageStatus,
)
from app.schemas.chat import (
    RoomCreate,
    RoomUpdate,
    RoomMemberCreate,
    RoomMemberUpdate,
    RoomAdminCreate,
    MessageCreate,
    MessageUpdate,
    MessageReactionCreate,
    MessageAttachmentCreate,
)


# ============ Helper Functions ============

def is_room_admin(*, session: Session, room_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Check if user is an admin of the room"""
    statement = select(RoomAdmin).where(
        RoomAdmin.room_id == room_id,
        RoomAdmin.user_id == user_id
    )
    admin = session.exec(statement).first()
    return admin is not None


def is_room_member(*, session: Session, room_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Check if user is a member of the room"""
    statement = select(RoomMember).where(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id,
        RoomMember.status == MemberStatus.ACTIVE
    )
    member = session.exec(statement).first()
    return member is not None


def is_room_creator(*, session: Session, room_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Check if user is the creator of the room"""
    statement = select(Room).where(Room.id == room_id, Room.created_by == user_id)
    room = session.exec(statement).first()
    return room is not None


# ============ Room CRUD ============

def create_room(*, session: Session, room_in: RoomCreate, created_by: uuid.UUID) -> Room:
    """Create a new room"""
    room = Room(
        **room_in.model_dump(),
        created_by=created_by,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    
    # Add creator as member
    creator_member = RoomMember(room_id=room.id, user_id=created_by)
    session.add(creator_member)
    
    # Add creator as admin
    creator_admin = RoomAdmin(room_id=room.id, user_id=created_by, assigned_by=created_by)
    session.add(creator_admin)
    
    session.commit()
    session.refresh(room)
    return room


def get_room_by_id(*, session: Session, room_id: uuid.UUID) -> Room | None:
    """Get room by ID"""
    statement = select(Room).where(Room.id == room_id, Room.is_archived == False)
    return session.exec(statement).first()


def get_user_rooms(
    *,
    session: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Room]:
    """Get all rooms for a user"""
    statement = (
        select(Room)
        .join(RoomMember, Room.id)
        .where(
            Room.id == RoomMember.room_id
            RoomMember.user_id == user_id,
            RoomMember.status == MemberStatus.ACTIVE,
            Room.is_archived == False
        )
        .order_by(Room.last_message_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def update_room(
    *,
    session: Session,
    room: Room,
    room_in: RoomUpdate,
    user_id: uuid.UUID,
) -> Room:
    """Update room - only admins can update"""
    if not is_room_admin(session=session, room_id=room.id, user_id=user_id):
        raise HTTPException(status_code=403, detail="Only admins can update room details")
    
    update_data = room_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)
    
    room.updated_at = datetime.utcnow()
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


def delete_room(*, session: Session, room: Room, user_id: uuid.UUID) -> None:
    """Delete room - only creator or admin can delete"""
    if not (is_room_admin(session=session, room_id=room.id, user_id=user_id) or
            is_room_creator(session=session, room_id=room.id, user_id=user_id)):
        raise HTTPException(status_code=403, detail="Only admins or creator can delete the room")
    
    room.is_archived = True
    room.updated_at = datetime.utcnow()
    session.add(room)
    session.commit()


# ============ Room Member CRUD ============

def add_room_member(
    *,
    session: Session,
    member_in: RoomMemberCreate,
    added_by: uuid.UUID,
) -> RoomMember:
    """Add member to room - only admins can add members"""
    if not is_room_admin(session=session, room_id=member_in.room_id, user_id=added_by):
        raise HTTPException(status_code=403, detail="Only admins can add members")
    
    # Check if user is already a member
    existing = session.exec(
        select(RoomMember).where(
            RoomMember.room_id == member_in.room_id,
            RoomMember.user_id == member_in.user_id
        )
    ).first()
    
    if existing:
        if existing.status == MemberStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="User is already a member")
        # Reactivate if left/removed
        existing.status = MemberStatus.ACTIVE
        existing.joined_at = datetime.utcnow()
        existing.left_at = None
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    
    member = RoomMember(**member_in.model_dump())
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def get_room_members(
    *,
    session: Session,
    room_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[RoomMember]:
    """Get all active members of a room"""
    statement = (
        select(RoomMember)
        .where(
            RoomMember.room_id == room_id,
            RoomMember.status == MemberStatus.ACTIVE
        )
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def update_room_member(
    *,
    session: Session,
    member: RoomMember,
    member_in: RoomMemberUpdate,
) -> RoomMember:
    """Update room member"""
    update_data = member_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)
    
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def remove_room_member(
    *,
    session: Session,
    room_id: uuid.UUID,
    user_id: uuid.UUID,
    removed_by: uuid.UUID,
) -> None:
    """Remove member from room - only admins can remove members"""
    if not is_room_admin(session=session, room_id=room_id, user_id=removed_by):
        raise HTTPException(status_code=403, detail="Only admins can remove members")
    
    statement = select(RoomMember).where(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    )
    member = session.exec(statement).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.status = MemberStatus.REMOVED
    member.left_at = datetime.utcnow()
    session.add(member)
    session.commit()


def leave_room(*, session: Session, room_id: uuid.UUID, user_id: uuid.UUID) -> None:
    """User leaves room voluntarily"""
    statement = select(RoomMember).where(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    )
    member = session.exec(statement).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.status = MemberStatus.LEFT
    member.left_at = datetime.utcnow()
    session.add(member)
    session.commit()


# ============ Room Admin CRUD ============

def add_room_admin(
    *,
    session: Session,
    admin_in: RoomAdminCreate,
    assigned_by: uuid.UUID,
) -> RoomAdmin:
    """Add admin to room - only existing admins can add new admins"""
    if not is_room_admin(session=session, room_id=admin_in.room_id, user_id=assigned_by):
        raise HTTPException(status_code=403, detail="Only admins can assign new admins")
    
    # Check if user is a member
    if not is_room_member(session=session, room_id=admin_in.room_id, user_id=admin_in.user_id):
        raise HTTPException(status_code=400, detail="User must be a member first")
    
    # Check if already admin
    existing = session.exec(
        select(RoomAdmin).where(
            RoomAdmin.room_id == admin_in.room_id,
            RoomAdmin.user_id == admin_in.user_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    admin = RoomAdmin(**admin_in.model_dump(), assigned_by=assigned_by)
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


def remove_room_admin(
    *,
    session: Session,
    room_id: uuid.UUID,
    user_id: uuid.UUID,
    removed_by: uuid.UUID,
) -> None:
    """Remove admin from room - only admins or creator can remove admins"""
    if not (is_room_admin(session=session, room_id=room_id, user_id=removed_by) or
            is_room_creator(session=session, room_id=room_id, user_id=removed_by)):
        raise HTTPException(status_code=403, detail="Only admins or creator can remove admins")
    
    # Can't remove the creator
    if is_room_creator(session=session, room_id=room_id, user_id=user_id):
        raise HTTPException(status_code=400, detail="Cannot remove creator as admin")
    
    statement = select(RoomAdmin).where(
        RoomAdmin.room_id == room_id,
        RoomAdmin.user_id == user_id
    )
    admin = session.exec(statement).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    session.delete(admin)
    session.commit()


def get_room_admins(*, session: Session, room_id: uuid.UUID) -> list[RoomAdmin]:
    """Get all admins of a room"""
    statement = select(RoomAdmin).where(RoomAdmin.room_id == room_id)
    return list(session.exec(statement).all())


# ============ Message CRUD ============

def create_message(
    *,
    session: Session,
    message_in: MessageCreate,
    sender_id: uuid.UUID,
) -> Message:
    """Create a new message"""
    # Check if user is a member
    if not is_room_member(session=session, room_id=message_in.room_id, user_id=sender_id):
        raise HTTPException(status_code=403, detail="You must be a member to send messages")
    
    message = Message(**message_in.model_dump(), sender_id=sender_id)
    session.add(message)
    
    # Update room's last_message_at
    room = session.get(Room, message_in.room_id)
    if room:
        room.last_message_at = datetime.utcnow()
        session.add(room)
    
    session.commit()
    session.refresh(message)
    return message


def get_message_by_id(*, session: Session, message_id: uuid.UUID) -> Message | None:
    """Get message by ID"""
    statement = select(Message).where(
        Message.id == message_id,
        Message.is_deleted == False
    )
    return session.exec(statement).first()


def get_room_messages(
    *,
    session: Session,
    room_id: uuid.UUID,
    skip: int = 0,
    limit: int = 50,
) -> list[Message]:
    """Get messages for a room"""
    statement = (
        select(Message)
        .where(Message.room_id == room_id, Message.is_deleted == False)
        .order_by(Message.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def update_message(
    *,
    session: Session,
    message: Message,
    message_in: MessageUpdate,
    user_id: uuid.UUID,
) -> Message:
    """Update message - only sender can update"""
    if message.sender_id != user_id:
        raise HTTPException(status_code=403, detail="Only the sender can edit the message")
    
    message.content = message_in.content
    message.is_edited = True
    message.updated_at = datetime.utcnow()
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def delete_message(
    *,
    session: Session,
    message: Message,
    user_id: uuid.UUID,
) -> None:
    """Delete message - sender or admin can delete"""
    if message.sender_id != user_id and not is_room_admin(
        session=session, room_id=message.room_id, user_id=user_id
    ):
        raise HTTPException(status_code=403, detail="Only the sender or admin can delete the message")
    
    message.is_deleted = True
    message.status = MessageStatus.DELETED
    message.updated_at = datetime.utcnow()
    session.add(message)
    session.commit()


# ============ Message Reaction CRUD ============

def add_message_reaction(
    *,
    session: Session,
    reaction_in: MessageReactionCreate,
    user_id: uuid.UUID,
) -> MessageReaction:
    """Add reaction to message"""
    # Check if already reacted with same emoji
    existing = session.exec(
        select(MessageReaction).where(
            MessageReaction.message_id == reaction_in.message_id,
            MessageReaction.user_id == user_id,
            MessageReaction.emoji == reaction_in.emoji
        )
    ).first()
    
    if existing:
        return existing
    
    reaction = MessageReaction(**reaction_in.model_dump(), user_id=user_id)
    session.add(reaction)
    session.commit()
    session.refresh(reaction)
    return reaction


def remove_message_reaction(
    *,
    session: Session,
    message_id: uuid.UUID,
    emoji: str,
    user_id: uuid.UUID,
) -> None:
    """Remove reaction from message"""
    statement = select(MessageReaction).where(
        MessageReaction.message_id == message_id,
        MessageReaction.user_id == user_id,
        MessageReaction.emoji == emoji
    )
    reaction = session.exec(statement).first()
    
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    
    session.delete(reaction)
    session.commit()


def get_message_reactions(
    *,
    session: Session,
    message_id: uuid.UUID,
) -> list[MessageReaction]:
    """Get all reactions for a message"""
    statement = select(MessageReaction).where(MessageReaction.message_id == message_id)
    return list(session.exec(statement).all())


# ============ Message Attachment CRUD ============

def add_message_attachment(
    *,
    session: Session,
    attachment_in: MessageAttachmentCreate,
) -> MessageAttachment:
    """Add attachment to message"""
    attachment = MessageAttachment(**attachment_in.model_dump())
    session.add(attachment)
    session.commit()
    session.refresh(attachment)
    return attachment


def get_message_attachments(
    *,
    session: Session,
    message_id: uuid.UUID,
) -> list[MessageAttachment]:
    """Get all attachments for a message"""
    statement = select(MessageAttachment).where(MessageAttachment.message_id == message_id)
    return list(session.exec(statement).all())