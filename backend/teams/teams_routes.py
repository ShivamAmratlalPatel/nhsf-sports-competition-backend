"""Ednpoints for teams"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.teams.teams_models import Team
from backend.teams.teams_schemas import TeamCreate, TeamRead, TeamUpdate
from backend.utils import object_to_dict

teams_router = APIRouter()

db_session = Depends(get_db)


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
) -> JSONResponse:
    """Create a team."""
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
    db: Session = db_session,
) -> JSONResponse:
    """Get all teams."""
    teams = db.query(Team).all()
    if not teams:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teams not found",
        )
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
) -> JSONResponse:
    """Update a team."""
    team = db.query(Team).filter(Team.id == team_id).first()
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
) -> JSONResponse:
    """Delete a team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    team.is_deleted = True
    db.add(team)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
