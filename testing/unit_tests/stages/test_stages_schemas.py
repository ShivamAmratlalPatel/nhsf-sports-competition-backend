"""Tests for stage schemas"""
import pytest
from sqlalchemy.orm import Session

from backend.stages.stages_models import Stage
from backend.stages.stages_schemas import StagesEnum
from testing.fixtures.database import session, session_factory  # noqa: F401


class TestStagesEnum:
    """Test cases for the StagesEnum enum."""

    def test_enum_values(self: "TestStagesEnum") -> None:
        """Test that the enum values are correct."""
        assert StagesEnum.group_stage.value == "0"
        assert StagesEnum.quarter_final.value == "1"
        assert StagesEnum.semi_final.value == "2"
        assert StagesEnum.final.value == "3"

    def test_enum_equality(self: "TestStagesEnum") -> None:
        """Test that the enum values are equal."""
        assert StagesEnum.group_stage == StagesEnum.group_stage
        assert StagesEnum.quarter_final == StagesEnum.quarter_final
        assert StagesEnum.semi_final == StagesEnum.semi_final
        assert StagesEnum.final == StagesEnum.final

    def test_enum_inequality(self: "TestStagesEnum") -> None:
        """Test that the enum values are not equal."""
        assert StagesEnum.group_stage != StagesEnum.quarter_final
        assert StagesEnum.quarter_final != StagesEnum.semi_final
        assert StagesEnum.semi_final != StagesEnum.final
        assert StagesEnum.final != StagesEnum.group_stage

    def test_invalid_enum_value(self: "TestStagesEnum") -> None:
        """Test that an invalid enum value raises a ValueError."""
        with pytest.raises(ValueError, match="a"):
            StagesEnum("Invalid Stage")


class TestStages:
    """Test cases for the stages module."""

    def test_stages(self: "TestStages", session: Session) -> None:
        """Test that the stages are created."""
        stages = session.query(Stage).order_by(Stage.id).all()
        assert len(stages) == 4  # noqa: PLR2004
