"""Functions to update the knockout stage of a sport."""
from uuid import UUID

from backend.matches.matches_models import Match
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from backend.utils import generate_uuid


def is_match_played(match: Match) -> bool:
    """Check if a match has been played."""
    return match.home_score is not None


def find_winner(match: Match) -> UUID:
    """Find the winner of a match."""
    if match.home_score > match.away_score:
        return match.home_team_id
    elif match.away_score > match.home_score:
        return match.away_team_id
    elif match.home_penalties > match.away_penalties:
        return match.home_team_id
    elif match.away_penalties > match.home_penalties:
        return match.away_team_id
    else:
        msg = f"Match {match.id} has no winner."
        raise HTTPException(status_code=500, detail=msg)


def update_knockout_for_match(match: Match, db: Session) -> None:
    """Update the knockout stage for a match."""
    if match.stage_id == 1 or match.stage_id == 3:
        other_match = (
            db.query(Match)
            .filter(Match.stage_id == match.stage_id + 1)
            .filter(Match.sport_id == match.sport_id)
            .filter(Match.is_deleted.is_(False))
            .first()
        )
        if is_match_played(other_match):
            semi_final_stage = 5 if match.stage_id == 1 else 6
            semi_final = (
                db.query(Match)
                .filter(Match.stage_id == semi_final_stage)
                .filter(Match.sport_id == match.sport_id)
                .filter(Match.is_deleted.is_(False))
                .first()
            )

            semi_final_1_home_team_id = find_winner(match)
            semi_final_1_away_team_id = find_winner(other_match)

            if semi_final:
                semi_final.is_deleted = True
            else:
                semi_final = Match(
                    id=generate_uuid(),
                    sport_id=match.sport_id,
                    stage_id=semi_final_stage,
                    home_team_id=semi_final_1_home_team_id,
                    away_team_id=semi_final_1_away_team_id,
                )
            db.add(semi_final)
            db.commit()
    elif match.stage_id == 5 or match.stage_id == 6:
        other_semi_final_id = 5 if match.stage_id == 6 else 6
        other_match = (
            db.query(Match)
            .filter(Match.stage_id == other_semi_final_id)
            .filter(Match.sport_id == match.sport_id)
            .filter(Match.is_deleted.is_(False))
            .first()
        )

        if is_match_played(other_match):
            final = (
                db.query(Match)
                .filter(Match.stage_id == 7)
                .filter(Match.sport_id == match.sport_id)
                .filter(Match.is_deleted.is_(False))
                .first()
            )

            final_home_team_id = find_winner(match)
            final_away_team_id = find_winner(other_match)

            if final:
                final.is_deleted = True
            else:
                final = Match(
                    id=generate_uuid(),
                    sport_id=match.sport_id,
                    stage_id=7,
                    home_team_id=final_home_team_id,
                    away_team_id=final_away_team_id,
                )
            db.add(final)
            db.commit()
