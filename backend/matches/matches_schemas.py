"""Matches Schemas"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_penalties, fake_score


class MatchBase(BaseModel):
    """Match base schema."""

    home_team_id: UUID
    away_team_id: UUID
    sport_id: UUID
    pitch_id: UUID | None = None
    stage_id: int
    home_score: float | None = None
    away_score: float | None = None
    home_penalties: float | None = None
    away_penalties: float | None = None
    time: datetime | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "home_team_id": generate_uuid(),
                "away_team_id": generate_uuid(),
                "sport_id": generate_uuid(),
                "pitch_id": generate_uuid(),
                "stage_id": generate_uuid(),
                "home_score": 0,
                "away_score": 0,
                "home_penalties": 0,
                "away_penalties": 0,
                "time": datetime_now(),
            },
        },
    )


class MatchCreate(MatchBase):
    """Match create schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **MatchBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class MatchUpdate(MatchBase):
    """Match update schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **MatchBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class MatchRead(MatchBase):
    """Match read schema."""

    id: UUID
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool
    pitch: Any | None = None
    group: int | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **MatchBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "last_modified_date": datetime_now(),
                "is_deleted": False,
            },
        },
    )


class KnockoutRead(BaseModel):
    """Match read schema."""

    id: UUID | None = None
    stage: Any
    home_team: str
    away_team: str
    home_team_score: float | None = None
    away_team_score: float | None = None
    home_team_penalties: float | None = None
    away_team_penalties: float | None = None
    pitch: Any | None = None
    model_config = ConfigDict(
        from_attributes=True,
    )


class ScoreDetails(BaseModel):
    """Score details schema."""

    home_score: float | None = None
    away_score: float | None = None
    home_penalties: float | None = None
    away_penalties: float | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "home_score": fake_score(),
                "away_score": fake_score(),
                "home_penalties": fake_penalties(),
                "away_penalties": fake_penalties(),
            },
        },
    )

    @model_validator(mode="after")
    def validate_score_details(self: "ScoreDetails") -> "ScoreDetails":
        """Validate score details."""
        home_score = self.home_score
        away_score = self.away_score
        home_penalties = self.home_penalties
        away_penalties = self.away_penalties

        if (
            home_score is None
            and away_score is None
            and home_penalties is None
            and away_penalties is None
        ):
            msg = "Either score or penalties must be provided"
            raise ValueError(msg)

        return self


class KnockoutSave(BaseModel):
    teams: list[UUID]
