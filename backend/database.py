"""Database module."""
import logging
import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from backend.config import DB_HOST, DB_NAME, DB_CONN, DB_USER, ENVIRONMENT, DB_PASS, \
    DATABASE_URL
from google.cloud.sql.connector import Connector
import sqlalchemy

# initialize Connector object
def connect_tcp_socket() -> Engine:
    """Initialize a TCP connection pool for a Cloud SQL instance of Postgres."""
    connector = Connector()

    conn = connector.connect(
        DB_CONN,
        driver="pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )

    return create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        "postgresql+pg8000://",
        creator=conn,
    )


def session_local_factory(database_url: str | None = None) -> sessionmaker:
    """
    Create a session factory.

    Args:
        database_url: database url

    Returns:
        sessionmaker: session factory

    """

    if ENVIRONMENT == "local":
        if database_url is None:
            database_url = DATABASE_URL
        engine: Engine = create_engine(database_url, poolclass=NullPool)
    else:
        engine: Engine = connect_tcp_socket()
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
