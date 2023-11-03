"""Pitches Schemas"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from testing.helpers.fake_data import fake_name


class PitchBase(BaseModel):
    """Pitch base schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": fake_name()},
        },
    )


class PitchCreate(PitchBase):
    """Pitch create schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **PitchBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class PitchUpdate(BaseModel):
    """Pitch update schema."""

    name: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
            },
        },
    )


class PitchRead(PitchBase):
    """Pitch read schema."""

    id: UUID
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
