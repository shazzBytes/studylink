import logging

from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine, init_db
from app.models.institution import Institution
from app.populate_sample_data import populate_sample_institution_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)

        if settings.ENVIRONMENT == "local":
            has_institution = session.exec(select(Institution.id)).first()
            if not has_institution:
                logger.info("No institutions found; populating local sample institution data.")
                populate_sample_institution_data(session)
            else:
                logger.info("Existing institutions found; skipping local sample institution seeding.")


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
