from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TableRead(BaseModel):
    id: UUID
    team_name: str
    points: float
    score_difference: float
    played: int
    points_per_game: float
    score_difference_per_game: float

    model_config = ConfigDict(
        from_attributes=True,
    )
