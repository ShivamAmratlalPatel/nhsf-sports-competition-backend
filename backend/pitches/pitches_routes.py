"""Endpoints for pitches"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.pitches.pitches_models import Pitch
from backend.pitches.pitches_schemas import PitchCreate, PitchRead, PitchUpdate
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

pitches_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@pitches_router.post(
    "/pitch",
    tags=["pitches"],
    description="Create pitch.",
    responses={
        status.HTTP_201_CREATED: {
            "model": PitchRead,
            "description": "Successful response: pitch created",
            "title": "Pitch details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Pitch already exists",
            "title": "Pitch already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Pitch already exists"},
                },
            },
        },
    },
)
def create_pitch(
    pitch_details: PitchCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a pitch."""
    check_admin(current_user)
    try:
        pitch = Pitch(**pitch_details.model_dump())
        db.add(pitch)
        db.commit()
        db.refresh(pitch)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pitch already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(PitchRead.model_validate(pitch)),
    )


@pitches_router.get(
    "/pitch/{pitch_id}",
    tags=["pitches"],
    description="Get pitch.",
    responses={
        status.HTTP_200_OK: {
            "model": PitchRead,
            "description": "Successful response: pitch found",
            "title": "Pitch details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Pitch not found",
            "title": "Pitch not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Pitch not found"},
                },
            },
        },
    },
)
def get_pitch(
    pitch_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a pitch."""
    pitch = db.query(Pitch).filter(Pitch.id == pitch_id).first()
    if not pitch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(PitchRead.model_validate(pitch)),
    )


@pitches_router.get(
    "/pitches/{sport_id}",
    tags=["pitches"],
    description="Get pitches.",
    responses={
        status.HTTP_200_OK: {
            "model": list[PitchRead],
            "description": "Successful response: pitches found",
            "title": "Pitch details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Pitches not found",
            "title": "Pitches not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Pitches not found"},
                },
            },
        },
    },
)
def get_pitches(
    sport_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get all pitches."""
    pitches = db.query(Pitch).filter(Pitch.sport_id == sport_id).all()
    if not pitches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitches not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(PitchRead.model_validate(pitch)) for pitch in pitches],
    )


@pitches_router.put(
    "/pitch/{pitch_id}",
    tags=["pitches"],
    description="Update pitch.",
    responses={
        status.HTTP_200_OK: {
            "model": PitchRead,
            "description": "Successful response: pitch updated",
            "title": "Pitch details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Pitch not found",
            "title": "Pitch not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Pitch not found"},
                },
            },
        },
    },
)
def update_pitch(
    pitch_id: UUID,
    pitch_details: PitchUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a pitch."""
    check_admin(current_user)
    pitch = db.query(Pitch).filter(Pitch.id == pitch_id).first()
    if not pitch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found",
        )
    for field, value in pitch_details:
        setattr(pitch, field, value)
    db.add(pitch)
    db.commit()
    db.refresh(pitch)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(PitchRead.model_validate(pitch)),
    )


@pitches_router.delete(
    "/pitch/{pitch_id}",
    tags=["pitches"],
    description="Delete pitch.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: pitch deleted",
            "title": "Pitch deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Pitch not found",
            "title": "Pitch not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Pitch not found"},
                },
            },
        },
    },
)
def delete_pitch(
    pitch_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a pitch."""
    check_admin(current_user)
    pitch = db.query(Pitch).filter(Pitch.id == pitch_id).first()
    if not pitch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found",
        )
    pitch.is_deleted = True
    db.add(pitch)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
