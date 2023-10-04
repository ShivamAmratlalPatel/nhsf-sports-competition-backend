from fastapi import HTTPException
from starlette import status

from backend.users.users_schemas import UserBase


def check_admin(user: UserBase) -> None:
    if user.user_type_name == "admin":
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
