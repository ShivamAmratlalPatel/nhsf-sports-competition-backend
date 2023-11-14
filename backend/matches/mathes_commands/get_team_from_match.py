"""Get the home and away team from a match."""
from backend.matches.matches_models import Match
from sqlalchemy.orm import Session

from backend.teams.teams_models import Team


def get_home_team_from_match(db: Session, match: Match) -> Team:
    """Get the home team from a match."""
    return db.get(Team, match.home_team_id)


def get_away_team_from_match(db: Session, match: Match) -> Team:
    """Get the away team from a match."""
    return db.get(Team, match.away_team_id)
