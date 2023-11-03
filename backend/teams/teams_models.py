"""Teams Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func, Integer
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Team(Base):
    """Team database model."""

    __tablename__ = "teams"

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
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
    )
    sport_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
    )
    group = Column(Integer)
    chapter = relationship("Chapter", back_populates="teams")
    sport = relationship("Sport", back_populates="teams")
