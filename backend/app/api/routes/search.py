from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_db
from app.crud.project_search import search_projects
from app.crud.publication_search import search_publications
from app.crud.research_search import search_researchers
from app.models.project import Project
from app.models.publication import Publication
from app.models.researcher import ResearcherInfo

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get(
    "/researchers",
    response_model=list[ResearcherInfo],
)
def search_researchers_route(
    *,
    session: Session = Depends(get_db),
    q: str | None = None,
    institute: str | None = None,
    qualification: str | None = None,
    domain: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return search_researchers(
        session=session,
        q=q,
        institute=institute,
        qualification=qualification,
        domain=domain,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/publications",
    response_model=list[Publication],
)
def search_publications_route(
    *,
    session: Session = Depends(get_db),
    q: str | None = None,
    domain: str | None = None,
    keyword: str | None = None,
    publisher: str | None = None,
    year: int | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return search_publications(
        session=session,
        q=q,
        domain=domain,
        keyword=keyword,
        publisher=publisher,
        year=year,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/projects",
    response_model=list[Project],
)
def search_projects_route(
    *,
    session: Session = Depends(get_db),
    q: str | None = None,
    domain: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return search_projects(
        session=session,
        q=q,
        domain=domain,
        skip=skip,
        limit=limit,
    )
