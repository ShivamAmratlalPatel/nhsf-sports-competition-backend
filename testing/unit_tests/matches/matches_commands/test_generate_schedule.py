"""Test generate_schedule function."""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.matches.matches_models import Match
from backend.matches.mathes_commands.generate_schedule import (
    check_matches_have_not_been_generated,
)
from backend.pitches.pitches_models import Pitch
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.utils import generate_uuid
from testing.fixtures.database import session, session_factory  # noqa: F401


class TestCheckMatchesHaveNotBeenGenerated:
    """Test the check_matches_have_not_been_generated function."""

    def test_matches_generated(
        self: "TestCheckMatchesHaveNotBeenGenerated",
        session: Session,
    ) -> None:
        """Test that an error is raised if matches have already been generated."""
        # Arrange
        sport_id = generate_uuid()
        sport = Sport(id=sport_id, name="Football")
        session.add(sport)
        session.commit()

        chapter = Chapter(
            id=generate_uuid(),
            name="Chapter",
            zone="North",
            email="a@b.com",
        )
        session.add(chapter)
        session.commit()

        pitch = Pitch(
            id=generate_uuid(),
            name="Pitch",
        )

        session.add(pitch)
        session.commit()

        home_team = Team(
            id=generate_uuid(),
            sport_id=sport_id,
            name="Home Team",
            chapter_id=chapter.id,
        )
        away_team = Team(
            id=generate_uuid(),
            sport_id=sport_id,
            name="Away Team",
            chapter_id=chapter.id,
        )
        session.add(home_team)
        session.add(away_team)
        session.commit()

        match = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            pitch_id=pitch.id,
            stage_id=0,
        )
        session.add(match)
        session.commit()

        with pytest.raises(HTTPException):
            check_matches_have_not_been_generated(session, sport_id)

    def test_matches_not_generated(
        self: "TestCheckMatchesHaveNotBeenGenerated",
        session: Session,
    ) -> None:
        """Test that no error is raised if matches have not been generated."""
        # Arrange
        sport_id = generate_uuid()
        sport = Sport(id=sport_id, name="Football")
        session.add(sport)
        session.commit()

        chapter = Chapter(
            id=generate_uuid(),
            name="Chapter",
            zone="North",
            email="a@b.com",
        )
        session.add(chapter)
        session.commit()

        pitch = Pitch(
            id=generate_uuid(),
            name="Pitch",
        )

        session.add(pitch)
        session.commit()

        home_team = Team(
            id=generate_uuid(),
            sport_id=sport_id,
            name="Home Team",
            chapter_id=chapter.id,
        )
        away_team = Team(
            id=generate_uuid(),
            sport_id=sport_id,
            name="Away Team",
            chapter_id=chapter.id,
        )
        session.add(home_team)
        session.add(away_team)
        session.commit()

        match = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            pitch_id=pitch.id,
            stage_id=0,
        )
        session.add(match)
        session.commit()

        # Act
        check_matches_have_not_been_generated(session, generate_uuid())

        # Assert
        assert True
