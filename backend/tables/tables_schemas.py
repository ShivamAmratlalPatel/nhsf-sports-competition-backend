"""Pydantic schemas for the tables module."""
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TableRead(BaseModel):
    """Table read schema."""

    id: UUID
    team_name: str
    won: int
    drawn: int
    lost: int
    played: int
    points_per_game: float
    score_difference_per_game: float

    model_config = ConfigDict(
        from_attributes=True,
    )
