"""Sports Schemas"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_sport_name


class SportBase(BaseModel):
    """Sport base schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": fake_sport_name()},
        },
    )


class SportCreate(SportBase):
    """Sport create schema."""

    start_time: datetime
    minutes_per_game: int
    number_of_players: int
    number_of_subs: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **SportBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class SportUpdate(BaseModel):
    """Sport update schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_sport_name(),
            },
        },
    )


class SportRead(SportBase):
    """Sport read schema."""

    id: UUID
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool
    start_time: datetime | None = None
    minutes_per_game: int | None = None
    number_of_players: int | None = None
    number_of_subs: int | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **SportBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "last_modified_date": datetime_now(),
                "is_deleted": False,
            },
        },
    )


class SportNameEnum(Enum):
    """Sport Name Enum"""

    football = "Football"
    badminton = "Badminton"
    netball = "Netball"
    cricket = "Cricket"
    kho = "Kho"
    kabaddiw = "KabaddiW"
    kabaddim = "KabaddiM"
