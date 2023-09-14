"""Authenticate user command."""
from sqlalchemy.orm import Session

from backend.users.users_commands.get_users import get_user
from backend.users.users_commands.password_token_commands import verify_password
from backend.users.users_schemas import UserInDB


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    """Authenticate user."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
