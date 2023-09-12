"""Log the score of a match."""
from uuid import UUID

from sqlalchemy.orm import Session

from backend.matches.matches_models import Match


def log_score(
    match_id: UUID,
    home_score: float,
    away_score: float,
    db: Session,
) -> None:
    """Log the score of a match."""
    match = db.get(Match, match_id)
    match.home_score = home_score
    match.away_score = away_score
    db.add(match)
    db.commit()
