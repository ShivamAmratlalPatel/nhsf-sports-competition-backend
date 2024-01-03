"""Ednpoints for players"""

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerCreate, PlayerRead
from backend.teams.teams_commands.chapter_from_team import chapter_id_from_team
from backend.users.users_commands.chapter_user import verify_chapter_user
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        ) from e

    if current_user.user_type_name == "chapter":
        try:
            verify_chapter_user(current_user.chapter_id, chapter_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not part of chapter",
            ) from e

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


@players_router.get(
    "/player/{player_id}",
    tags=["players"],
    description="Get player by id.",
    responses={
        status.HTTP_200_OK: {
            "model": PlayerRead,
            "description": "Player retrieved successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Player not found",
        },
    },
)
def get_player(
    player_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get player by id."""
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
    )


@players_router.get(
    "/players/{match_id}/home",
    tags=["players"],
    description="Get all players.",
    responses={
        status.HTTP_200_OK: {
            "model": PlayerRead,
            "description": "Players retrieved successfully",
        },
    },
)
def get_home_players(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get all players."""
    match: Match = db.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )

    players: list[Player] = (
        db.query(Player)
        .filter(Player.team_id == match.home_team_id)
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    if not players:
        players = []

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(PlayerRead.model_validate(player), format_date=True)
            for player in players
        ],
    )


@players_router.get(
    "/players/{match_id}/away",
    tags=["players"],
    description="Get all players.",
    responses={
        status.HTTP_200_OK: {
            "model": PlayerRead,
            "description": "Players retrieved successfully",
        },
    },
)
def get_away_players(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get all players."""
    match: Match = db.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )

    players: list[Player] = (
        db.query(Player)
        .filter(Player.team_id == match.away_team_id)
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    if not players:
        players = []

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(PlayerRead.model_validate(player), format_date=True)
            for player in players
        ],
    )


@players_router.get(
    "/players/{match_id}",
    tags=["players"],
    description="Get match players.",
    responses={
        status.HTTP_200_OK: {
            "model": PlayerRead,
            "description": "Players retrieved successfully",
        },
    },
)
def get_match_players(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get match players."""
    match: Match = db.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )

    home_players: list[Player] = (
        db.query(Player)
        .filter(Player.team_id == match.home_team_id)
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    if not home_players:
        home_players = []

    away_players: list[Player] = (
        db.query(Player)
        .filter(Player.team_id == match.away_team_id)
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    if not away_players:
        away_players = []

    number_of_home_players = len(home_players)
    number_of_away_players = len(away_players)

    if number_of_home_players > number_of_away_players:
        away_players.extend([None] * (number_of_home_players - number_of_away_players))
    elif number_of_away_players > number_of_home_players:
        home_players.extend([None] * (number_of_away_players - number_of_home_players))

    players = []
    for i in range(len(home_players)):
        players.append(
            {
                "home": object_to_dict(PlayerRead.model_validate(home_players[i]))
                if home_players[i]
                else None,
                "away": object_to_dict(PlayerRead.model_validate(away_players[i]))
                if away_players[i]
                else None,
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=players,
    )
