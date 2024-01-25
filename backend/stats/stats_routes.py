"""Endpoints for stats"""
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.players.players_models import Player
from backend.stats.stats_schemas import Stat
from backend.teams.teams_models import Team
from backend.utils import convert_list_to_list

stats_router = APIRouter()

db_session = Depends(get_db)


@stats_router.get("/stats")
def get_stats(chapter_id: UUID | None = None, db: Session = db_session) -> JSONResponse:
    """Get stats"""
    if chapter_id:
        number_of_teams = (
            db.query(Team)
            .filter(Team.chapter_id == chapter_id)
            .filter(Team.is_deleted.is_(False))
            .count()
        )
        number_of_players = (
            db.query(Player)
            .filter(Team.chapter_id == chapter_id)
            .filter(Player.is_deleted.is_(False))
            .filter(Team.is_deleted.is_(False))
            .count()
        )
    else:
        number_of_teams = db.query(Team).filter(Team.is_deleted.is_(False)).count()
        number_of_players = (
            db.query(Player)
            .filter(Player.is_deleted.is_(False))
            .filter(Team.is_deleted.is_(False))
            .count()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=convert_list_to_list(
            [
                Stat(
                    text="Teams",
                    count=number_of_teams,
                    icon="ri:user-line",
                    color="bg-indigo-500",
                ),
                Stat(
                    text="Players",
                    count=number_of_players,
                    icon="ri:book-2-line",
                    color="bg-blue-500",
                ),
                Stat(
                    text="Matches",
                    count=1,
                    icon="ri:message-line",
                    color="bg-orange-500",
                ),
                Stat(
                    text="Sports",
                    count=1,
                    icon="ri:line-chart-line",
                    color="bg-emerald-500",
                ),
            ],
            format_date=True,
        ),
    )
