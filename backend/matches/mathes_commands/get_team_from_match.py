from backend.matches.matches_models import Match
from sqlalchemy.orm import Session

from backend.teams.teams_models import Team


def get_home_team_from_match(db: Session, match: Match) -> Team:
    return db.query(Team).filter(Team.id == match.home_team_id).first()


def get_away_team_from_match(db: Session, match: Match) -> Team:
    return db.query(Team).filter(Team.id == match.away_team_id).first()
