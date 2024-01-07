"""Teams Schemas"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_name


class TeamBase(BaseModel):
    """Team base schema."""

    name: str
    internal_name: str
    chapter_id: UUID
    sport_id: UUID
    group: int | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "internal_name": fake_name(),
                "chapter_id": generate_uuid(),
                "sport_id": generate_uuid(),
                "group": 0,
            },
        },
    )


class TeamCreate(TeamBase):
    """Team create schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **TeamBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class TeamUpdate(BaseModel):
    """Team update schema."""

    name: str
    internal_name: str
    chapter_id: UUID
    sport_id: UUID
    group: int | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "internal_name": fake_name(),
                "chapter_id": generate_uuid(),
                "sport_id": generate_uuid(),
                "group": 0,
            },
        },
    )


class TeamRead(TeamBase):
    """Team read schema."""

    id: UUID
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **TeamBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "last_modified_date": datetime_now(),
                "is_deleted": False,
            },
        },
    )
