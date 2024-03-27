"""Schemas for the stages module."""

from testing.fixtures.database import session, session_factory  # noqa: F401
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid


class StagesEnum(str, Enum):
    """Enum for the stages of the tournament."""

    group_stage = 0
    quarter_final = 1
    semi_final = 2
    final = 3
    __slots__ = ()


class StageBase(BaseModel):
    """Stage base schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Group Stage"},
        },
    )


class StageCreate(StageBase):
    """Stage create schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **StageBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class StageUpdate(BaseModel):
    """Stage update schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "example": {"name": "Group Stage"},
            },
        },
    )


class StageRead(StageBase):
    """Stage read schema."""

    id: int
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **StageBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "last_modified_date": datetime_now(),
                "is_deleted": False,
            },
        },
    )
