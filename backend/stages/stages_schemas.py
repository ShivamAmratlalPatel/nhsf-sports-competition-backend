"""Schemas for the stages module."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid
from testing.fixtures.database import session, session_factory  # noqa: F401


class StagesEnum(str, Enum):
    """Enum for the stages of the tournament."""

    group_stage = 0
    round_of_16_1 = 1
    round_of_16_2 = 2
    round_of_16_3 = 3
    round_of_16_4 = 4
    round_of_16_5 = 5
    round_of_16_6 = 6
    round_of_16_7 = 7
    round_of_16_8 = 8
    round_of_16_9 = 9
    round_of_16_10 = 10
    round_of_16_11 = 11
    round_of_16_12 = 12
    round_of_16_13 = 13
    round_of_16_14 = 14
    round_of_16_15 = 15
    round_of_16_16 = 16
    quarter_final_1 = 17
    quarter_final_2 = 18
    quarter_final_3 = 19
    quarter_final_4 = 20
    semi_final_1 = 21
    semi_final_2 = 22
    final = 23
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
