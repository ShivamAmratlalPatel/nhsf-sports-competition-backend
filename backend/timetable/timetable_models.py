"""Matches Database Models"""
from sqlalchemy import Column, Integer, String

from backend.database import Base
from backend.stages.stages_models import Stage  # noqa: F401


class Timetable(Base):
    """Timetable database model."""

    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    time_activity = Column(String, nullable=False)
    activity_name = Column(String, nullable=False)
