"""Endpoints for tables"""
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.tables.tables_commands.update_table import (
    update_table_for_match,
    update_table_for_team,
)
from backend.tables.tables_models import LeagueTable
from backend.tables.tables_schemas import TableRead
from backend.teams.teams_models import Team
from backend.utils import object_to_dict

tables_router = APIRouter()

db_session = Depends(get_db)


@tables_router.get("/table/{sport_id}", tags=["table"])
def get_table_for_sport(sport_id: UUID, db: Session = db_session) -> JSONResponse:
    """Get table for sport"""
    table_rows: list[LeagueTable] = (
        db.query(LeagueTable)
        .filter(LeagueTable.sport_id == sport_id)
        .filter(LeagueTable.is_deleted.is_(False))
        .all()
    )

    if not table_rows or table_rows == []:
        return JSONResponse(status_code=200, content=[])

    # Sort by points_per_game, then score_difference_per_game, then scores_for_per_game
    table_rows.sort(
        key=lambda x: (
            x.points,
            x.score_difference,
            x.scores_for,
        ),
        reverse=True,
    )

    max_groups = max([i.team.group for i in table_rows])

    output = []
    for i in range(max_groups + 1):
        output.append(
            [
                object_to_dict(TableRead.model_validate(table_row))
                for table_row in table_rows
                if table_row.team.group == i
            ],
        )

    return JSONResponse(status_code=200, content=output)


@tables_router.put("/table/{sport_id}", tags=["table"])
def update_table_for_sport(sport_id: UUID, db: Session = db_session) -> JSONResponse:
    """Update table for sport"""
    matches: list[Match] = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.is_deleted.is_(False))
        .filter(Match.home_score.isnot(None))
        .all()
    )

    for match in matches:
        update_table_for_match(match, db)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": True})


@tables_router.get("/table_update", tags=["table"])
def update_all_tables(db: Session = db_session) -> JSONResponse:
    teams: list[Team] = db.query(Team).filter(Team.is_deleted.is_(False)).all()

    for team in teams:
        update_table_for_team(team.id, db)

    return JSONResponse(status_code=200, content="Updated tables for all teams")
