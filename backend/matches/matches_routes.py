"""Ednpoints for matches"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.matches.matches_schemas import (
    MatchCreate,
    MatchRead,
    MatchUpdate,
    ScoreDetails,
)
from backend.tables.tables_commands.update_table import update_table_for_match
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

matches_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@matches_router.post(
    "/match",
    tags=["matches"],
    description="Create match.",
    responses={
        status.HTTP_201_CREATED: {
            "model": MatchRead,
            "description": "Successful response: match created",
            "title": "Match details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Match already exists",
            "title": "Match already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Match already exists"},
                },
            },
        },
    },
)
def create_match(
    match_details: MatchCreate,
    db: Session = db_session,
) -> JSONResponse:
    """Create a match."""
    match = Match(**match_details.model_dump())
    db.add(match)
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match already exists",
        ) from e
    db.refresh(match)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.get(
    "/match/{match_id}",
    tags=["matches"],
    description="Get match.",
    responses={
        status.HTTP_200_OK: {
            "model": MatchRead,
            "description": "Successful response: match found",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def get_match(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.get(
    "/matches",
    tags=["matches"],
    description="Get matches.",
    responses={
        status.HTTP_200_OK: {
            "model": list[MatchRead],
            "description": "Successful response: matches found",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Matches not found",
            "title": "Matches not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Matches not found"},
                },
            },
        },
    },
)
def get_matches(
    db: Session = db_session,
) -> JSONResponse:
    """Get all matches."""
    matches = db.query(Match).all()
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matches not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(MatchRead.model_validate(match)) for match in matches],
    )


@matches_router.put(
    "/match/{match_id}",
    tags=["matches"],
    description="Update match.",
    responses={
        status.HTTP_200_OK: {
            "model": MatchRead,
            "description": "Successful response: match updated",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def update_match(
    match_id: UUID,
    match_details: MatchUpdate,
    db: Session = db_session,
) -> JSONResponse:
    """Update a match."""
    match: Match | None = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    for field, value in match_details.__dict__.items():
        if field != "id":
            setattr(match, field, value)
    db.add(match)
    db.commit()
    update_table_for_match(match, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.delete(
    "/match/{match_id}",
    tags=["matches"],
    description="Delete match.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: match deleted",
            "title": "Match deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def delete_match(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Delete a match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    match.is_deleted = True
    db.add(match)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


@matches_router.get(
    "/schedule/{sport_id}",
    tags=["matches"],
    description="Get schedule.",
    responses={
        status.HTTP_200_OK: {
            "model": list[MatchRead],
            "description": "Successful response: schedule found",
            "title": "Schedule details",
        },
    },
)
def get_schedule(
    sport_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get schedule."""
    played_matches: list[Match] = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.is_deleted.is_(False))
        .filter(Match.home_score.is_not(None))
        .order_by(Match.time)
        .all()
    )

    if played_matches is None:
        played_matches = []

    unplayed_matches: list[Match] = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.is_deleted.is_(False))
        .filter(Match.home_score.is_(None))
        .order_by(Match.time)
        .all()
    )

    if unplayed_matches is None:
        unplayed_matches = []

    matches = played_matches + unplayed_matches

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(MatchRead.model_validate(match)) for match in matches],
    )


@matches_router.put(
    "/match/{match_id}/log_score",
    tags=["matches"],
)
def log_score(
    match_id: UUID,
    score_details: ScoreDetails,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Log score for a match."""
    check_admin(current_user)

    match: Match | None = db.get(Match, match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    match.home_score = score_details.home_score
    match.away_score = score_details.away_score
    match.home_penalties = score_details.home_penalties
    match.away_penalties = score_details.away_penalties

    db.add(match)
    db.commit()
    update_table_for_match(match, db)

    return JSONResponse(
        status_code=200,
        content=object_to_dict(MatchRead.model_validate(match), format_date=True),
    )
