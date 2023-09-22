"""Database module."""
import logging
import os
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy import engine as sqlalchemy_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from google.cloud.sql.connector import Connector, IPTypes

from backend.config import (
    ENVIRONMENT,
    DB_PASS,
    DB_NAME, DB_USER, DB_HOST, DB_PORT,
)

if TYPE_CHECKING:
    from sqlalchemy import Engine


def connect_tcp_socket() -> Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""

    pool = create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy_engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        ),
    )
    return pool


def session_local_factory(database_url: str | None = None) -> sessionmaker:
    """
    Create a session factory.

    Args:
        database_url: database url

    Returns:
        sessionmaker: session factory

    """
    if database_url is None:  # pragma: no cover
        database_url = os.environ["DATABASE_URL"]
    if ENVIRONMENT == "local":
        engine: Engine = create_engine(database_url, poolclass=NullPool)
    else:
        connector = Connector()
        engine = connect_tcp_socket(connector)
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
