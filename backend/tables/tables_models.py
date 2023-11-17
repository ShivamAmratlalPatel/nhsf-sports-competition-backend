"""Table Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class LeagueTable(Base):
    """LeagueTable model."""

    __tablename__ = "league_tables"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    team_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    team = relationship("Team")
    sport_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
    )
    won = Column(Integer, default=0, server_default="0")
    drawn = Column(Integer, default=0, server_default="0")
    lost = Column(Integer, default=0, server_default="0")
    scores_for = Column(
        pg.NUMERIC(precision=12, scale=2),
        default=0,
        server_default="0",
    )
    scores_against = Column(
        pg.NUMERIC(precision=12, scale=2),
        default=0,
        server_default="0",
    )
    played = Column(Integer, default=0, server_default="0")
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone("Europe/London", func.current_timestamp()),
    )
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone("Europe/London", func.current_timestamp()),
    )

    @property
    def points(self: "LeagueTable") -> int:
        """Calculate the points for the team."""
        return self.won * 3 + self.drawn

    @property
    def points_per_game(self: "LeagueTable") -> float:
        """Calculate the points per game for the team."""
        try:
            return float(self.points) / float(self.played)
        except ZeroDivisionError:
            return 0

    @property
    def scores_for_per_game(self: "LeagueTable") -> float:
        """Calculate the scores for per game for the team."""
        try:
            return float(self.scores_for) / float(self.played)
        except ZeroDivisionError:
            return 0

    @property
    def scores_against_per_game(self: "LeagueTable") -> float:
        """Calculate the scores against per game for the team."""
        try:
            return float(self.scores_against) / float(self.played)
        except ZeroDivisionError:
            return 0

    @property
    def score_difference(self: "LeagueTable") -> float:
        """Calculate the score difference for the team."""
        return self.scores_for - self.scores_against

    @property
    def score_difference_per_game(self: "LeagueTable") -> float:
        """Calculate the score difference per game for the team."""
        try:
            return float(self.score_difference) / float(self.played)
        except ZeroDivisionError:
            return 0

    @property
    def team_name(self: "LeagueTable") -> str:
        """Get the team name."""
        return self.team.name
