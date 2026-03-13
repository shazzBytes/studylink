
from sqlmodel import SQLModel


class CreatePublication(SQLModel):
    title: str
    publisher: str
    year: int | None = None

    description: str | None = None

    domains: list[str] = []


class UpdatePublication(SQLModel):
    title: str | None = None
    publisher: str | None = None
    year: int | None = None

    description: str | None = None

    domains: list[str] | None = None
