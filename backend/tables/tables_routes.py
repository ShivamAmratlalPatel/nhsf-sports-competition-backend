"""Ednpoints for tables"""
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.tables.tables_models import LeagueTable
from backend.tables.tables_schemas import TableRead
from backend.utils import object_to_dict

tables_router = APIRouter()

db_session = Depends(get_db)


@tables_router.get("/table/{sport_id}")
def get_table_for_sport(sport_id: UUID, db: Session = db_session) -> JSONResponse:
    """Get table for sport"""
    table_rows: list[LeagueTable] = (
        db.query(LeagueTable)
        .filter(LeagueTable.sport_id == sport_id)
        .filter(LeagueTable.is_deleted.is_(False))
        .all()
    )

    # Sort by points_per_game, then score_difference_per_game, then scores_for_per_game
    table_rows.sort(
        key=lambda x: (
            x.points_per_game,
            x.score_difference_per_game,
            x.scores_for_per_game,
        ),
        reverse=True,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(TableRead.model_validate(table_row))
            for table_row in table_rows
        ],
    )
