from sqlmodel import SQLModel



from app.models.users import (
    UserBase,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UpdatePassword,
    User,
    UserPublic,
    UsersPublic,
)

from app.models.items import (
    ItemBase,
    ItemCreate,
    ItemUpdate,
    Item,
    ItemPublic,
    ItemsPublic,
)

# Import auth-related models from auth.py
from app.models.auth import (
    Message,
    Token,
    TokenPayload,
    NewPassword,
)

# Import researcher models
from app.models.researcher import ResearcherInfo

# Import publication models
from app.models.publication import Publication, PublicationRole

# Import collaboration models
from app.models.collaborator import ResearcherCollaborator
from app.models.publication_member import PublicationMember

__all__ = [
    # SQLModel
    "SQLModel",
    # User models
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
]