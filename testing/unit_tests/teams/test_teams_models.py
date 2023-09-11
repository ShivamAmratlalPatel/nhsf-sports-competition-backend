"""Test cases for teams models."""
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_chapter, fake_sport, fake_team


class TestTeam:
    """Team model test cases."""

    def test_create_team(self: "TestTeam", session: Session) -> None:
        """Test creating a team instance."""
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        team_data = fake_team(chapter_id=chapter.id, sport_id=sport.id)
        team = Team(**team_data)
        session.add(team)
        session.commit()

        assert team.id is not None
        assert team.name == team_data["name"]
        assert team.created_date is not None
        assert team.is_deleted is False

    def test_soft_delete_team(self: "TestTeam", session: Session) -> None:
        """Test soft deleting a team."""
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        team_data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        team = Team(**team_data)
        session.add(team)
        session.commit()

        team.is_deleted = True
        session.commit()

        deleted_team = session.get(Team, team.id)
        assert deleted_team.is_deleted is True

    def test_teams_relationship(self: "TestTeam", session: Session) -> None:
        """Test teams relationship."""
        chapter_data = fake_chapter()
        chapter = Chapter(**chapter_data)
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)

        session.commit()
        session.refresh(chapter)
        session.refresh(sport)

        team_data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        team = Team(**team_data)
        session.add(team)
        session.commit()

        assert team.sport == sport
        assert team.chapter == chapter
