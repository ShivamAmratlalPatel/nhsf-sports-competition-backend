"""Test Sport schemas."""
from datetime import datetime
from uuid import UUID

import pytz

from backend.sports.sports_schemas import SportBase, SportCreate, SportRead, SportUpdate


def test_valid_sport_base_schema() -> None:
    """Test valid SportBase schema."""
    data = {
        "name": "Football",
    }
    sport_base = SportBase(**data)
    assert sport_base.name == data["name"]


def test_valid_sport_create_schema() -> None:
    """Test valid SportCreate schema."""
    data = {
        "name": "Football",
    }
    sport_create = SportCreate(**data)
    assert sport_create.name == data["name"]


def test_valid_sport_update_schema() -> None:
    """Test valid SportUpdate schema."""
    data = {
        "name": "Football",
    }
    sport_update = SportUpdate(**data)
    assert sport_update.name == data["name"]


def test_valid_sport_read_schema() -> None:
    """Test valid SportRead schema."""
    data = {
        "id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "name": "Football",
        "created_date": datetime(2021, 1, 1, tzinfo=pytz.timezone("Europe/London")),
        "last_modified_date": datetime(
            2021,
            1,
            1,
            tzinfo=pytz.timezone("Europe/London"),
        ),
        "is_deleted": False,
    }
    sport_read = SportRead(**data)
    assert sport_read.id == UUID(data["id"])
    assert sport_read.name == data["name"]
    assert sport_read.created_date == data["created_date"]
    assert sport_read.last_modified_date == data["last_modified_date"]
    assert sport_read.is_deleted == data["is_deleted"]
