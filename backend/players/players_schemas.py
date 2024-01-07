"""Players schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_name


class PlayerBase(BaseModel):
    """Player base schema."""

    name: str
    team_id: UUID | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "team_id": generate_uuid(),
            },
        },
    )


class PlayerCreate(PlayerBase):
    """Player create schema."""


class PlayerUpdate(PlayerBase):
    """Player update schema."""


class PlayerRead(PlayerBase):
    """Player read schema."""

    id: UUID
    created_date: datetime
    is_deleted: bool
    last_modified_date: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **PlayerBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "is_deleted": False,
                "last_modified_date": datetime_now(),
            },
        },
    )
