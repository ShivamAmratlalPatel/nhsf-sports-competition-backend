"""Schemas for the stages module."""
from enum import Enum

from testing.fixtures.database import session, session_factory  # noqa: F401


class StagesEnum(str, Enum):
    """Enum for the stages of the tournament."""

    group_stage = 0
    quarter_final = 1
    semi_final = 2
    final = 3
