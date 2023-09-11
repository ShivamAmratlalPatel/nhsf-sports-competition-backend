"""Ednpoints for matches"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.matches.matches_schemas import MatchCreate, MatchRead, MatchUpdate
from backend.utils import object_to_dict

matches_router = APIRouter()

db_session = Depends(get_db)


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
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    for field, value in match_details:
        setattr(match, field, value)
    db.add(match)
    db.commit()
    db.refresh(match)
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
