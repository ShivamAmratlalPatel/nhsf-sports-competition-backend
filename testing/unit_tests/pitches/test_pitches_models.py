"""Test cases for pitches models."""
from sqlalchemy.orm import Session

from backend.pitches.pitches_models import Pitch
from backend.sports.sports_models import Sport
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_pitch, fake_sport


class TestPitch:
    """Pitch model test cases."""

    def test_create_pitch(self: "TestPitch", session: Session) -> None:
        """Test creating a pitch instance."""
        sport_data = fake_sport()
        sport = Sport(**sport_data)
        session.add(sport)
        session.commit()
        session.refresh(sport)

        pitch_data = fake_pitch()
        pitch = Pitch(**pitch_data)
        session.add(pitch)
        session.commit()

        assert pitch.id is not None
        assert pitch.name == pitch_data["name"]
        assert pitch.created_date is not None
        assert pitch.is_deleted is False

    def test_soft_delete_pitch(self: "TestPitch", session: Session) -> None:
        """Test soft deleting a pitch."""
        sport_data = fake_sport()
        sport = Sport(**sport_data)
        session.add(sport)
        session.commit()
        session.refresh(sport)

        pitch_data = fake_pitch()

        pitch = Pitch(**pitch_data)
        session.add(pitch)
        session.commit()

        pitch.is_deleted = True
        session.commit()

        deleted_pitch = session.get(Pitch, pitch.id)
        assert deleted_pitch.is_deleted is True
