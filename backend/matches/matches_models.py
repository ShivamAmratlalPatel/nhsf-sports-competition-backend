"""Matches Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Match(Base):
    """Match database model."""

    __tablename__ = "matches"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    home_team_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    away_team_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    sport_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
    )
    pitch_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("pitches.id", ondelete="CASCADE"),
        nullable=False,
    )
    stage_id = Column(
        Integer,
        ForeignKey("stages.id", ondelete="CASCADE"),
        nullable=False,
    )
    home_score = Column(pg.NUMERIC(precision=12, scale=2))
    away_score = Column(pg.NUMERIC(precision=12, scale=2))
    home_penalties = Column(pg.NUMERIC(precision=12, scale=2))
    away_penalties = Column(pg.NUMERIC(precision=12, scale=2))
    time = Column(DateTime(timezone=True))
    sport = relationship("Sport", back_populates="matches")
    pitch = relationship("Pitch", back_populates="matches")
