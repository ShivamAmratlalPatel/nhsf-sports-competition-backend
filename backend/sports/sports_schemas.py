"""Sports Schemas"""

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, BaseModel

from backend.utils import generate_uuid, datetime_now
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
