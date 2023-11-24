"""Ednpoints for sports"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.sports.sports_models import Sport
from backend.sports.sports_schemas import SportCreate, SportRead, SportUpdate
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

sports_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@sports_router.post(
    "/sport",
    tags=["sports"],
    description="Create sport.",
    responses={
        status.HTTP_201_CREATED: {
            "model": SportRead,
            "description": "Successful response: sport created",
            "title": "Sport details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Sport already exists",
            "title": "Sport already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Sport already exists"},
                },
            },
        },
    },
)
def create_sport(
    sport_details: SportCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a sport."""
    try:
        sport = Sport(**sport_details.model_dump())
        db.add(sport)
        db.commit()
        db.refresh(sport)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sport already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(SportRead.model_validate(sport)),
    )


@sports_router.get(
    "/sport/{sport_id}",
    tags=["sports"],
    description="Get sport.",
    responses={
        status.HTTP_200_OK: {
            "model": SportRead,
            "description": "Successful response: sport found",
            "title": "Sport details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Sport not found",
            "title": "Sport not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Sport not found"},
                },
            },
        },
    },
)
def get_sport(
    sport_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a sport."""
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(SportRead.model_validate(sport)),
    )


@sports_router.get(
    "/sports",
    tags=["sports"],
    description="Get sports.",
    responses={
        status.HTTP_200_OK: {
            "model": list[SportRead],
            "description": "Successful response: sports found",
            "title": "Sport details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Sports not found",
            "title": "Sports not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Sports not found"},
                },
            },
        },
    },
)
def get_sports(
    db: Session = db_session,
) -> JSONResponse:
    """Get all sports."""
    sports = db.query(Sport).all()
    if not sports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sports not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(SportRead.model_validate(sport)) for sport in sports],
    )


@sports_router.put(
    "/sport/{sport_id}",
    tags=["sports"],
    description="Update sport.",
    responses={
        status.HTTP_200_OK: {
            "model": SportRead,
            "description": "Successful response: sport updated",
            "title": "Sport details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Sport not found",
            "title": "Sport not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Sport not found"},
                },
            },
        },
    },
)
def update_sport(
    sport_id: UUID,
    sport_details: SportUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a sport."""
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found",
        )
    for field, value in sport_details:
        setattr(sport, field, value)
    db.add(sport)
    db.commit()
    db.refresh(sport)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(SportRead.model_validate(sport)),
    )


@sports_router.delete(
    "/sport/{sport_id}",
    tags=["sports"],
    description="Delete sport.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: sport deleted",
            "title": "Sport deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Sport not found",
            "title": "Sport not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Sport not found"},
                },
            },
        },
    },
)
def delete_sport(
    sport_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a sport."""
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found",
        )
    sport.is_deleted = True
    db.add(sport)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
