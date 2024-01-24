"""Sports Database Models"""
from sqlalchemy import Boolean, Column, DateTime, String, func, Float
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Sport(Base):
    """Sport database model."""

    __tablename__ = "sports"
    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
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
    quarter_finals = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    semi_finals = Column(Boolean, nullable=False, default=False, server_default="false")
    start_time = Column(DateTime(timezone=True))
    minutes_per_game = Column(Float)
    teams = relationship("Team", back_populates="sport")
    matches = relationship("Match", back_populates="sport")
