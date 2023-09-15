"""Routes for users."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.helpers import get_db
from backend.users.users_commands.authenticate_user import authenticate_user
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_commands.password_token_commands import get_password_hash
from backend.users.users_commands.tokens import create_access_token
from backend.users.users_models import User, UserType
from backend.users.users_schemas import UserBase, UserCreate

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)
form_instace = Depends()

users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.post("/token", tags=["users"])
def login_for_access_token(
    db: Session = db_session,
    form_data: OAuth2PasswordRequestForm = form_instace,
) -> dict[str, str]:
    """Login for access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_type": user.user_type_name},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post(
    "/users",
    tags=["users"],
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
        },
    },
)
def post_user(user_create: UserCreate, db: Session = db_session) -> JSONResponse:
    """Create user."""
    admin_user_id = db.query(UserType).filter(UserType.name == "admin").first().id
    user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
        user_type_id=admin_user_id,
        is_deleted=True,
    )
    db.add(user)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully"},
    )


@users_router.get("/users/me", tags=["users"])
def get_me(
    current_user: UserBase = current_user_instance,
) -> UserBase:
    """Get current user."""
    return current_user
