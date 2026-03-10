from sqlmodel import Session

from app.crud.researcher import create_researcher
from app.models.researcher import ResearcherInfo
from app.schemas.researcher import CreateResearcherInfo
from tests.utils.utils import random_email, random_lower_string


def create_random_researcher(db: Session) -> ResearcherInfo:
    """Create a random researcher for testing"""
    email = random_email()
    full_name = f"{random_lower_string()} {random_lower_string()}"
    qualification = random_lower_string()
    institute = random_lower_string()

    researcher_in = CreateResearcherInfo(
        email=email,
        full_name=full_name,
        qualification=qualification,
        institute=institute,
        bio=random_lower_string(),
    )

    researcher = create_researcher(session=db, researcher_in=researcher_in)
    return researcher
