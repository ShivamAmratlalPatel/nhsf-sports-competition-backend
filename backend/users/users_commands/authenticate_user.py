"""Authenticate user command."""
from sqlalchemy.orm import Session

from backend.users.users_commands.get_users import get_user_by_username
from backend.users.users_commands.password_token_commands import verify_password
from backend.users.users_models import User


def authenticate_user(db: Session, username: str, password: str) -> User | bool:
    """Authenticate user."""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if user.is_deleted:
        return False
    return user
