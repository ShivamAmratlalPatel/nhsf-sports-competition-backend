"""Ednpoints for teams"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Row, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.teams.teams_schemas import (
    TeamCreate,
    TeamRead,
    TeamUpdate,
    TeamCreateAdmin,
)
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict, generate_uuid

teams_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@teams_router.post(
    "/team",
    tags=["teams"],
    description="Create team.",
    responses={
        status.HTTP_201_CREATED: {
            "model": TeamRead,
            "description": "Successful response: team created",
            "title": "Team details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Team already exists",
            "title": "Team already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Team already exists"},
                },
            },
        },
    },
)
def create_team(
    team_details: TeamCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a team."""
    check_admin(current_user)
    team = Team(**team_details.model_dump())
    db.add(team)
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team already exists",
        ) from e
    db.refresh(team)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.post(
    "/team/admin",
    tags=["teams"],
    description="Create team.",
    responses={
        status.HTTP_201_CREATED: {
            "model": TeamRead,
            "description": "Successful response: team created",
            "title": "Team details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Team already exists",
            "title": "Team already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Team already exists"},
                },
            },
        },
    },
)
def create_team_admin(
    team_details: TeamCreateAdmin,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a team."""
    check_admin(current_user)

    existing_sport_teams: list[Team] | None = (
        db.query(Team)
        .filter(Team.sport_id == team_details.sport_id)
        .filter(Team.chapter_id == team_details.chapter_id)
        .filter(Team.is_deleted.is_(False))
        .all()
    )

    chapter = db.get(Chapter, team_details.chapter_id)
    sport = db.get(Sport, team_details.sport_id)

    new_team = Team(
        id=generate_uuid(),
        name=chapter.name,
        internal_name=sport.name,
        sport_id=team_details.sport_id,
        chapter_id=team_details.chapter_id,
    )

    if existing_sport_teams:
        for team in existing_sport_teams:
            if team.name == chapter.name:
                team.name = f"{team.name} A"
                new_team.name = f"{new_team.name} B"
            elif team.name == f"{chapter.name} A":
                new_team.name = f"{new_team.name} B"
            elif team.name == f"{chapter.name} B":
                new_team.name = f"{new_team.name} C"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Too many teams",
                )
            db.add(team)
    db.add(new_team)

    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(TeamRead.model_validate(new_team)),
    )


@teams_router.get(
    "/team/{team_id}",
    tags=["teams"],
    description="Get team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team found",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def get_team(
    team_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.get(
    "/teams",
    tags=["teams"],
    description="Get teams.",
    responses={
        status.HTTP_200_OK: {
            "model": list[TeamRead],
            "description": "Successful response: teams found",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Teams not found",
            "title": "Teams not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Teams not found"},
                },
            },
        },
    },
)
def get_teams(
    chapter_id: UUID | None = None,
    sport_id: UUID | None = None,
    sort_by_group: bool = False,
    db: Session = db_session,
) -> JSONResponse:
    """Get all teams."""
    if sort_by_group:
        max_group: Row | None = (
            db.query(Team.group)
            .filter(Team.group.is_not(None))
            .filter(Team.is_deleted.is_(False))
            .order_by(Team.group.desc())
            .first()
        )
        if max_group is None:
            if chapter_id:
                teams = (
                    db.query(Team)
                    .filter(Team.chapter_id == chapter_id)
                    .filter(Team.is_deleted.is_(False))
                    .all()
                )
            elif sport_id:
                teams = (
                    db.query(Team)
                    .filter(Team.sport_id == sport_id)
                    .filter(Team.is_deleted.is_(False))
                    .all()
                )
            else:
                teams = db.query(Team).filter(Team.is_deleted.is_(False)).all()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[
                    [object_to_dict(TeamRead.model_validate(team)) for team in teams]
                ],
            )
        else:
            teams: list[list[Team]] = []
            if chapter_id:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.chapter_id == chapter_id)
                    .filter(Team.is_deleted.is_(False))
                    .filter(Team.group.is_(None))
                    .all()
                )
            elif sport_id:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.sport_id == sport_id)
                    .filter(Team.is_deleted.is_(False))
                    .filter(Team.group.is_(None))
                    .all()
                )
            else:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.group.is_(None))
                    .filter(Team.is_deleted.is_(False))
                    .all()
                )

            if query_teams:
                teams.append(query_teams)

            for group in range(1, max_group[0] + 1):
                if chapter_id:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.chapter_id == chapter_id)
                        .filter(Team.is_deleted.is_(False))
                        .filter(Team.group == group)
                        .all()
                    )
                elif sport_id:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.sport_id == sport_id)
                        .filter(Team.is_deleted.is_(False))
                        .filter(Team.group == group)
                        .all()
                    )
                else:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.group == group)
                        .filter(Team.is_deleted.is_(False))
                        .all()
                    )

                if query_teams:
                    teams.append(query_teams)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[
                    [
                        object_to_dict(TeamRead.model_validate(team))
                        for team in group_team
                    ]
                    for group_team in teams
                ],
            )
    else:
        if chapter_id:
            teams = (
                db.query(Team)
                .filter(Team.chapter_id == chapter_id)
                .filter(Team.is_deleted.is_(False))
                .all()
            )
        elif sport_id:
            teams = (
                db.query(Team)
                .filter(Team.sport_id == sport_id)
                .filter(Team.is_deleted.is_(False))
                .all()
            )
        else:
            teams = db.query(Team).filter(Team.is_deleted.is_(False)).all()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[object_to_dict(TeamRead.model_validate(team)) for team in teams],
        )


@teams_router.put(
    "/team/{team_id}",
    tags=["teams"],
    description="Update team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team updated",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def update_team(
    team_id: UUID,
    team_details: TeamUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)
    """Update a team."""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    for field, value in team_details:
        setattr(team, field, value)
    db.add(team)
    db.commit()
    db.refresh(team)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.delete(
    "/team/{team_id}",
    tags=["teams"],
    description="Delete team.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: team deleted",
            "title": "Team deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def delete_team(
    team_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a team."""
    check_admin(current_user)
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    team.is_deleted = True
    db.add(team)
    db.commit()

    team_players = (
        db.query(Player)
        .filter(
            or_(Player.morning_team_id == team_id, Player.afternoon_team_id == team_id)
        )
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    for player in team_players:
        player.is_deleted = True
        db.add(player)
        db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


@teams_router.put(
    "/team/{team_id}/group",
    tags=["teams"],
    description="Update team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team updated",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def update_group(
    team_id: UUID,
    group: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)
    """Update a team's group."""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    team.group = group
    db.add(team)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )
