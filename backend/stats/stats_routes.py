"""Endpoints for stats"""
from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.stats.stats_schemas import Stat
from backend.teams.teams_models import Team
from backend.teams.teams_routes import check_team_valid
from backend.teams.teams_schemas import TeamRead
from backend.utils import convert_list_to_list, object_to_dict
from fastapi import APIRouter, Depends, HTTPException

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


@stats_router.get("/invalid_teams")
def get_invalid_teams(db: Session = db_session) -> JSONResponse:
    teams: list[Team] = (
        db.query(Team)
        .filter(Team.is_deleted.is_(False))
        .order_by(Team.name, Team.sport_id)
        .all()
    )

    invalid_teams: list[Team] = []
    for team in teams:
        try:
            check_team_valid(team.id, db)
        except HTTPException:
            invalid_teams.append(team)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(TeamRead.model_validate(team)) for team in invalid_teams
        ],
    )


@stats_router.get("/team_numbers")
def get_team_numbers(db: Session = db_session):
    team_numbers = (
        db.query(Team.name, Team.internal_name, func.count(Player.id))
        .select_from(Team)
        .outerjoin(
            Player,
            (Player.morning_team_id == Team.id)
            | (Player.afternoon_team_id == Team.id) & Player.is_deleted.is_(False),
            full=True,
        )
        .filter(Team.is_deleted.is_(False))
        .group_by(Team.id)
        .order_by(Team.name, Team.internal_name)
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=convert_list_to_list(
            [
                {
                    "name": row[0],
                    "internal_name": row[1],
                    "number_of_players": row[2],
                }
                for row in team_numbers
            ],
            format_date=True,
        ),
    )
