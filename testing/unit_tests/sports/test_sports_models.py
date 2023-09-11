"""Test cases for sports models."""
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_chapter, fake_sport, fake_team


class TestSport:
    """Sport model test cases."""

    def test_create_sport(self: "TestSport", session: Session) -> None:
        """Test creating a sport instance."""
        sport_data = fake_sport()
        sport = Sport(**sport_data)
        session.add(sport)
        session.commit()

        assert sport.id is not None
        assert sport.name == sport_data["name"]
        assert sport.created_date is not None
        assert sport.is_deleted is False

    def test_soft_delete_sport(self: "TestSport", session: Session) -> None:
        """Test soft deleting a sport."""
        sport_data = fake_sport()

        sport = Sport(**sport_data)
        session.add(sport)
        session.commit()

        sport.is_deleted = True
        session.commit()

        deleted_sport = session.get(Sport, sport.id)
        assert deleted_sport.is_deleted is True

    def test_teams_relationship(self: "TestSport", session: Session) -> None:
        """Test teams relationship."""
        chapter_data = fake_chapter()
        chapter = Chapter(**chapter_data)
        session.add(chapter)
        session.commit()

        assert chapter.teams == []

        sport_data = fake_sport()

        sport = Sport(**sport_data)
        session.add(sport)
        session.commit()

        assert sport.teams == []

        team_data = fake_team(chapter_id=chapter.id, sport_id=sport.id)
        team = Team(**team_data)

        session.add(team)

        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        assert sport.teams == [team]
