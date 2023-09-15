from uuid import UUID

from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.teams.teams_models import Team


def chapter_id_from_team(db: Session, team_id: UUID) -> UUID:
    """Get the chapter ID from the team ID."""
    team: Team | None = db.get(Team, team_id)
    if team is None:
        msg = "Team not found"
        raise ValueError(msg)
    return team.chapter_id


def chapter_from_team(db: Session, team_id: UUID) -> Chapter:
    """Get the chapter from the team ID."""
    chapter_id: UUID = chapter_id_from_team(db, team_id)
    chapter: Chapter | None = db.get(Chapter, chapter_id)
    if chapter is None:
        msg = "Chapter not found"
        raise ValueError(msg)
    return chapter
