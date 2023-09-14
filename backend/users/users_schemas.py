"""User schemas"""
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """User base."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    user_type_name: str | None = None


class UserInDB(UserBase):
    """User in database."""

    hashed_password: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class Token(BaseModel):
    """Token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    username: str | None = None


class UserCreate(BaseModel):
    """User create."""

    username: str
    email: EmailStr
    password: str
    full_name: str
