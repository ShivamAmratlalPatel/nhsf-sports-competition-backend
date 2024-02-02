"""Endpoints for spectators"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.players.players_models import Player
from backend.players.players_schemas import (
    CardBase,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from backend.spectators.spectators_models import Spectator
from backend.spectators.spectators_schemas import SpectatorRead
from backend.sports.sports_models import Sport
from backend.teams.teams_commands.chapter_from_team import chapter_id_from_team
from backend.teams.teams_models import Team
from backend.users.users_commands.chapter_user import verify_chapter_user
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import convert_list_to_list, object_to_dict, generate_uuid

spectator_router = APIRouter()
current_user_instance = Depends(get_current_active_user)
db_session = Depends(get_db)


@spectator_router.get("/spectator/{spectator_id}", tags=["spectators"])
def get_spectator(spectator_id: UUID, db: Session = db_session):
    pass
    spectator = db.get(Spectator, spectator_id)
    if spectator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spectator not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(
            SpectatorRead(
                id=spectator.id,
                name=spectator.name,
                email=spectator.email,
            ),
            format_date=True,
        ),
    )
