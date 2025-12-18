# Publication schemas
from app.schemas.publications import (
    CreatePublication,
    UpdatePublication,
)

# Researcher schemas
from app.schemas.researcher import (
    CreateResearcherInfo,
    UpdateResearcherInfo,
)

__all__ = [
    # Publication schemas
    "CreatePublication",
    "UpdatePublication",
    # Researcher schemas
    "CreateResearcherInfo",
    "UpdateResearcherInfo",
]
