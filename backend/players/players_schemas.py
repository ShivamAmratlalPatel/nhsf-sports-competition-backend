"""Players schemas."""
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_name


class CardType(Enum):
    """Card type enum."""

    YELLOW = "yellow"
    RED = "red"


class CardBase(BaseModel):
    type: CardType
    reason: str | None = None


class PlayerBase(BaseModel):
    """Player base schema."""

    name: str | None = None
    morning_team_id: UUID | None = None
    afternoon_team_id: UUID | None = None
    cards: list | None = []
    order_id: str | None = None
    ticket_id: str | None = None
    barcode: str | None = None
    checked_in: bool = False
    ticket_voided: bool = False
    emergency_contact_name: str | None = None
    emergency_contact_number: str | None = None
    emergency_contact_relation: str | None = None
    allergies_medical_conditions: str | None = None
    original_chapter: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "morning_team_id": generate_uuid(),
                "afternoon_team_id": generate_uuid(),
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
