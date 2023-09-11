"""Pitches Database Models"""
from sqlalchemy.orm import relationship

from backend.database import Base
from sqlalchemy import Column, func, String, DateTime, Boolean
from sqlalchemy.dialects import postgresql as pg

from backend.utils import generate_uuid, datetime_now


class Pitch(Base):
    """Pitch database model."""

    __tablename__ = "pitches"
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
        server_default=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    matches = relationship("Match", back_populates="pitch")
