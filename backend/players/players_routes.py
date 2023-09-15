"""Ednpoints for players"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerCreate, PlayerRead
from backend.teams.teams_commands.chapter_from_team import chapter_id_from_team
from backend.users.users_commands.chapter_user import verify_chapter_user
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from typing import TYPE_CHECKING

from backend.utils import object_to_dict

if TYPE_CHECKING:
    from uuid import UUID

players_router = APIRouter()
current_user_instance = Depends(get_current_active_user)
db_session = Depends(get_db)


@players_router.post(
    "/player",
    tags=["players"],
    description="Create player.",
    responses={
        status.HTTP_201_CREATED: {
            "model": PlayerRead,
            "description": "Player created successfully",
        },
    },
)
def create_player(
    player_create: PlayerCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a player."""
    try:
        chapter_id: UUID = chapter_id_from_team(db, player_create.team_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if current_user.user_type_name == "chapter":
        try:
            verify_chapter_user(current_user.chapter_id, chapter_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not part of chapter",
            )

    player = Player(
        name=player_create.name,
        team_id=player_create.team_id,
    )

    db.add(player)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
    )
