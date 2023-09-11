"""Test Pitch schemas."""
from datetime import datetime
from uuid import UUID

import pytz

from backend.pitches.pitches_schemas import (
    PitchBase,
    PitchCreate,
    PitchRead,
    PitchUpdate,
)


def test_valid_pitch_base_schema() -> None:
    """Test valid PitchBase schema."""
    data = {
        "name": "Pitch 1",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    pitch_base = PitchBase(**data)
    assert pitch_base.name == data["name"]


def test_valid_pitch_create_schema() -> None:
    """Test valid PitchCreate schema."""
    data = {
        "name": "Pitch 1",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    pitch_create = PitchCreate(**data)
    assert pitch_create.name == data["name"]


def test_valid_pitch_update_schema() -> None:
    """Test valid PitchUpdate schema."""
    data = {
        "name": "Pitch 1",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    pitch_update = PitchUpdate(**data)
    assert pitch_update.name == data["name"]


def test_valid_pitch_read_schema() -> None:
    """Test valid PitchRead schema."""
    data = {
        "id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "name": "Pitch 1",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
        "created_date": datetime(2021, 1, 1, tzinfo=pytz.timezone("Europe/London")),
        "last_modified_date": datetime(
            2021,
            1,
            1,
            tzinfo=pytz.timezone("Europe/London"),
        ),
        "is_deleted": False,
    }
    pitch_read = PitchRead(**data)
    assert pitch_read.id == UUID(data["id"])
    assert pitch_read.name == data["name"]
    assert pitch_read.created_date == data["created_date"]
    assert pitch_read.last_modified_date == data["last_modified_date"]
    assert pitch_read.is_deleted == data["is_deleted"]
