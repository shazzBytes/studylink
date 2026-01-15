# User CRUD operations
from app.crud.users import (
    authenticate,
    create_user,
    get_user_by_email,
    update_user,
)

# Item CRUD operations
from app.crud.items import create_item

# Publication CRUD operations
from app.crud.publication import (
    create_publication,
    delete_publication,
    get_publication_by_id,
    get_publications_by_researcher,
    update_publication,
)
from app.crud.researcher import (
    get_researcher_by_id,
)
__all__ = [
    # User operations
    "authenticate",
    "create_user",
    "get_user_by_email",
    "update_user",
    # Item operations
    "create_item",
    # Publication operations
    "create_publication",
    "delete_publication",
    "get_publication_by_id",
    "get_publications_by_researcher",
    "update_publication",
]
