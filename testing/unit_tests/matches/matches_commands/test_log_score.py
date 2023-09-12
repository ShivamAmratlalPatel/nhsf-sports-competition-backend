"""Test the log_score function."""
import pytest
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.matches.matches_models import Match
from backend.matches.mathes_commands.log_score import log_score
from backend.pitches.pitches_models import Pitch
from backend.sports.sports_models import Sport
from backend.stages.stages_schemas import StagesEnum
from backend.teams.teams_models import Team
from backend.utils import generate_uuid
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import (
    fake_chapter,
    fake_match,
    fake_pitch,
    fake_sport,
    fake_team,
)


@pytest.fixture()
def match_data(session: Session) -> dict:
    """Return a dictionary of match data."""
    home_chapter = Chapter(**fake_chapter())
    away_chapter = Chapter(**fake_chapter())
    home_chapter.id = generate_uuid()
    away_chapter.id = generate_uuid()
    sport = Sport(**fake_sport())
    sport.id = generate_uuid()
    home_team = Team(**fake_team(chapter_id=home_chapter.id, sport_id=sport.id))
    away_team = Team(**fake_team(chapter_id=away_chapter.id, sport_id=sport.id))
    away_team.id = generate_uuid()
    pitch = Pitch(**fake_pitch())
    pitch.id = generate_uuid()
    session.add(home_chapter)
    session.add(away_chapter)
    session.add(home_team)
    session.add(away_team)
    session.add(sport)
    session.add(pitch)
    session.commit()

    return fake_match(
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        sport_id=sport.id,
        pitch_id=pitch.id,
        stage=StagesEnum.quarter_final,
    )


class TestLogScore:
    """Test the log_score function."""

    def test_log_score(
        self: "TestLogScore",
        session: Session,
        match_data: dict,
    ) -> None:
        """Test that the score of a match can be logged."""
        match = Match(**match_data)
        session.add(match)
        session.commit()

        log_score(match.id, 1, 2, session)

        match = session.get(Match, match.id)

        assert match.home_score == 1
        assert match.away_score == 2  # noqa: PLR2004
