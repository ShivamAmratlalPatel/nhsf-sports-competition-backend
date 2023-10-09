"""Update the table for a team or match."""
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from backend.matches.matches_models import Match


def update_table_for_team(team_id: UUID, db: Session) -> None:
    """Update the table for a team."""
    played = (
        db.query(Match)
        .filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
        .count()
    )
    won = (
        db.query(Match)
        .filter(
            or_(
                and_(
                    Match.home_team_id == team_id,
                    or_(
                        Match.home_score > Match.away_score,
                        and_(
                            Match.home_score == Match.away_score,
                            Match.home_penalties > Match.away_penalties,
                        ),
                    ),
                ),
                and_(
                    Match.away_team_id == team_id,
                    or_(
                        Match.away_score > Match.home_score,
                        and_(
                            Match.away_score == Match.home_score,
                            Match.away_penalties > Match.home_penalties,
                        ),
                    ),
                ),
            ),
        )
        .count()
    )

    drawn = (
        db.query(Match)
        .filter(
            and_(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
                Match.home_score == Match.away_score,
                Match.home_penalties == Match.away_penalties,
            ),
        )
        .count()
    )

    _lost = played - won - drawn


def update_table_for_match(match: Match, db: Session) -> None:  # noqa: ARG001
    """Update the table for a match."""
