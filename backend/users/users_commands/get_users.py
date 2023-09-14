"""Get user commands."""
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from backend.config import ALGORITHM, SECRET_KEY
from backend.helpers import get_db
from backend.users.users_models import User
from backend.users.users_schemas import TokenData, UserBase, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

oauth2_scheme_depends = Depends(oauth2_scheme)
db_session = Depends(get_db)


def get_current_user(
    db: Session = db_session,
    token: str = oauth2_scheme_depends,
) -> UserBase:
    """Get current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    user: UserInDB | None = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserBase(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
        user_type_name=user.user_type_name,
    )


current_user_depends = Depends(get_current_user)


def get_current_active_user(
    current_user: UserBase = current_user_depends,
) -> UserBase:
    """Get current active user."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


def get_user(db: Session, username: str) -> UserInDB | None:
    """Get user."""
    user = db.query(User).filter(User.username == username).first()

    if user is not None:
        return UserInDB(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.is_deleted,
            hashed_password=user.hashed_password,
            user_type_name=user.user_type_name,
        )
    return None
