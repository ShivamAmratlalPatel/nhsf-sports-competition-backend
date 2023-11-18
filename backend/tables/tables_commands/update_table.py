"""Update the table for a team or match."""
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from backend.matches.matches_models import Match
from backend.tables.tables_models import LeagueTable
from backend.teams.teams_models import Team
from backend.utils import generate_uuid


def update_table_for_team(team_id: UUID, db: Session) -> None:
    """Update the table for a team."""
    team: Team | None = db.get(Team, team_id)

    if team is None:
        msg = f"Team with id {team_id} does not exist."
        raise ValueError(msg)

    played = (
        db.query(Match)
        .filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
        .filter(Match.home_score.is_not(None))
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

    lost = (
        db.query(Match)
        .filter(
            or_(
                and_(
                    Match.home_team_id == team_id,
                    or_(
                        Match.home_score < Match.away_score,
                        and_(
                            Match.home_score == Match.away_score,
                            Match.home_penalties < Match.away_penalties,
                        ),
                    ),
                ),
                and_(
                    Match.away_team_id == team_id,
                    or_(
                        Match.away_score < Match.home_score,
                        and_(
                            Match.away_score == Match.home_score,
                            Match.away_penalties < Match.home_penalties,
                        ),
                    ),
                ),
            ),
        )
        .count()
    )

    drawn = played - won - lost

    scores_for = sum(
        [
            float(row[0])
            for row in db.query(Match.home_score)
            .filter(Match.home_team_id == team_id)
            .all()
            if row[0] is not None
        ],
    ) + sum(
        [
            float(row[0])
            for row in db.query(Match.away_score)
            .filter(Match.away_team_id == team_id)
            .all()
            if row[0] is not None
        ],
    )

    scores_against = sum(
        [
            float(row[0])
            for row in db.query(Match.home_score)
            .filter(Match.away_team_id == team_id)
            .all()
            if row[0] is not None
        ],
    ) + sum(
        [
            float(row[0])
            for row in db.query(Match.away_score)
            .filter(Match.home_team_id == team_id)
            .all()
            if row[0] is not None
        ],
    )

    table_entry: LeagueTable | None = (
        db.query(LeagueTable).filter(LeagueTable.team_id == team_id).first()
    )

    if table_entry:
        table_entry.played = played
        table_entry.won = won
        table_entry.drawn = drawn
        table_entry.lost = lost
        table_entry.scores_for = scores_for
        table_entry.scores_against = scores_against
    else:
        table_entry = LeagueTable(
            team_id=team_id,
            sport_id=team.sport_id,
            played=played,
            won=won,
            drawn=drawn,
            lost=lost,
            scores_for=scores_for,
            scores_against=scores_against,
        )
        table_entry.id = generate_uuid()

    db.add(table_entry)
    db.commit()


def update_table_for_match(match: Match, db: Session) -> None:
    """Update the table for a match."""
    update_table_for_team(match.home_team_id, db)
    update_table_for_team(match.away_team_id, db)
