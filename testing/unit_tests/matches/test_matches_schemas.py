"""Test match schemas"""
from backend.matches.matches_schemas import (
    MatchBase,
    MatchCreate,
    MatchRead,
    MatchUpdate,
)
from backend.utils import datetime_now, generate_uuid


class TestMatchBase:
    """Test cases for the match base schema."""

    def test_valid_match_base(self: "TestMatchBase") -> None:
        """Test that the match base schema is valid."""
        data = {
            "home_team_id": generate_uuid(),
            "away_team_id": generate_uuid(),
            "sport_id": generate_uuid(),
            "pitch_id": generate_uuid(),
            "stage_id": 0,
            "home_score": 0.0,
            "away_score": 0.0,
            "home_penalties": 0.0,
            "away_penalties": 0.0,
            "time": None,
        }
        match = MatchBase(**data)
        assert match.model_dump() == data


class TestMatchCreate:
    """Test cases for the match create schema."""

    def test_valid_match_create(self: "TestMatchCreate") -> None:
        """Test that the match create schema is valid."""
        data = {
            "home_team_id": generate_uuid(),
            "away_team_id": generate_uuid(),
            "sport_id": generate_uuid(),
            "pitch_id": generate_uuid(),
            "stage_id": 0,
            "home_score": 0.0,
            "away_score": 0.0,
            "home_penalties": 0.0,
            "away_penalties": 0.0,
            "time": None,
        }
        match = MatchCreate(**data)
        assert match.model_dump() == data


class TestMatchUpdate:
    """Test cases for the match update schema."""

    def test_valid_match_update(self: "TestMatchUpdate") -> None:
        """Test that the match update schema is valid."""
        data = {
            "home_team_id": generate_uuid(),
            "away_team_id": generate_uuid(),
            "sport_id": generate_uuid(),
            "pitch_id": generate_uuid(),
            "stage_id": 0,
            "home_score": 0.0,
            "away_score": 0.0,
            "home_penalties": 0.0,
            "away_penalties": 0.0,
            "time": None,
        }
        match = MatchUpdate(**data)
        assert match.model_dump() == data


class TestMatchRead:
    """Test cases for the match read schema."""

    def test_valid_match_read(self: "TestMatchRead") -> None:
        """Test that the match read schema is valid."""
        data = {
            "id": generate_uuid(),
            "created_date": datetime_now(),
            "last_modified_date": datetime_now(),
            "is_deleted": False,
            "home_team_id": generate_uuid(),
            "away_team_id": generate_uuid(),
            "sport_id": generate_uuid(),
            "pitch": None,
            "pitch_id": generate_uuid(),
            "stage_id": 0,
            "home_score": 0.0,
            "away_score": 0.0,
            "home_penalties": 0.0,
            "away_penalties": 0.0,
            "time": None,
        }
        match = MatchRead(**data)
        assert match.model_dump() == data
