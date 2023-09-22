"""Configuration for the backend application."""
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", ""))
ALGORITHM = os.environ.get("ALGORITHM", "")
BACKEND_ENDPOINT = os.environ.get("BACKEND_ENDPOINT", "")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "")
LOGLEVEL = os.environ.get("LOGLEVEL", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
UVICORN_RELOAD = os.environ.get("UVICORN_RELOAD", "")
SQLALCHEMY_WARN_20 = os.environ.get("SQLALCHEMY_WARN_20", "")

DB_USER = os.environ.get("DB_USER", "")
DB_PASS = os.environ.get("DB_PASS", "")
DB_HOST = os.environ.get("DB_HOST", "")
DB_PORT = os.environ.get("DB_PORT", "")
DB_NAME = os.environ.get("DB_NAME", "")
