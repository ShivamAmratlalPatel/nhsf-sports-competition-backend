"""Database module."""
import logging
import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from backend.config import DATABASE_URL


def session_local_factory(database_url: str | None = None) -> sessionmaker:
    """
    Create a session factory.

    Args:
        database_url: database url

    Returns:
        sessionmaker: session factory

    """
    if database_url is None:
        database_url = DATABASE_URL
    engine: Engine = create_engine(database_url, poolclass=NullPool)

    session_factory: sessionmaker = sessionmaker(
        bind=engine,
        future=True,
        expire_on_commit=False,
    )

    if "DEBUG_SQL" in os.environ:  # pragma: no cover
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

    return session_factory


Base = declarative_base()
