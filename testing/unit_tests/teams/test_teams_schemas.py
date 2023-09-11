"""Test Team schemas."""
from datetime import datetime
from uuid import UUID

import pytz

from backend.teams.teams_schemas import TeamBase, TeamCreate, TeamRead, TeamUpdate


def test_valid_team_base_schema() -> None:
    """Test valid TeamBase schema."""
    data = {
        "name": "Football",
        "chapter_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    team_base = TeamBase(**data)
    assert team_base.name == data["name"]


def test_valid_team_create_schema() -> None:
    """Test valid TeamCreate schema."""
    data = {
        "name": "Football",
        "chapter_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    team_create = TeamCreate(**data)
    assert team_create.name == data["name"]


def test_valid_team_update_schema() -> None:
    """Test valid TeamUpdate schema."""
    data = {
        "name": "Football",
        "chapter_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "sport_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4f",
    }
    team_update = TeamUpdate(**data)
    assert team_update.name == data["name"]


def test_valid_team_read_schema() -> None:
    """Test valid TeamRead schema."""
    data = {
        "id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "name": "Football",
        "chapter_id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
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
    team_read = TeamRead(**data)
    assert team_read.id == UUID(data["id"])
    assert team_read.name == data["name"]
    assert team_read.created_date == data["created_date"]
    assert team_read.last_modified_date == data["last_modified_date"]
    assert team_read.is_deleted == data["is_deleted"]
