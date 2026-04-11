from sqlmodel import SQLModel

# Import auth-related models from auth.py
from app.models.auth import (
    Message,
    NewPassword,
    Token,
    TokenPayload,
)
from app.models.items import (
    Item,
    ItemBase,
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
)
from app.models.users import (
    AccountType,
    UpdatePassword,
    User,
    UserBase,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

from .project import Project
from .project_member import ProjectMember

__all__ = ["Project", "ProjectMember"]

# Import researcher models
from app.models.chat import Chat

# Import collaboration models
from app.models.collaborator import ResearcherCollaborator
from app.models.message import Message as ChatMessage

# Import publication models
from app.models.publication import Publication, PublicationRole
from app.models.publication_member import PublicationMember
from app.models.researcher import ResearcherInfo

__all__ = [
    # SQLModel
    "SQLModel",
    # User models
    "AccountType",
    "UserBase",
    "UserCreate",
    "UserRegister",
    "UserUpdate",
    "UserUpdateMe",
    "UpdatePassword",
    "User",
    "UserPublic",
    "UsersPublic",
    # Item models
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "Item",
    "ItemPublic",
    "ItemsPublic",
    # Auth models
    "Message",
    "Token",
    "TokenPayload",
    "NewPassword",
    # Researcher models
    "ResearcherInfo",
    # Publication models
    "Publication",
    "PublicationRole",
    # Collaboration models
    "ResearcherCollaborator",
    "PublicationMember",
    # Chat models
    "Chat",
    "ChatMessage",
]
