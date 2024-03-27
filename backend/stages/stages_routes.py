"""Endpoints for stages"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.stages.stages_models import Stage
from backend.stages.stages_schemas import StageCreate, StageRead, StageUpdate
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

stages_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@stages_router.post(
    "/stage",
    tags=["stages"],
    description="Create stage.",
    responses={
        status.HTTP_201_CREATED: {
            "model": StageRead,
            "description": "Successful response: stage created",
            "title": "Stage details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Stage already exists",
            "title": "Stage already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Stage already exists"},
                },
            },
        },
    },
)
def create_stage(
    stage_details: StageCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a stage."""
    check_admin(current_user)
    try:
        stage = Stage(**stage_details.model_dump())
        db.add(stage)
        db.commit()
        db.refresh(stage)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Stage already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(StageRead.model_validate(stage)),
    )


@stages_router.get(
    "/stage/{stage_id}",
    tags=["stages"],
    description="Get stage.",
    responses={
        status.HTTP_200_OK: {
            "model": StageRead,
            "description": "Successful response: stage found",
            "title": "Stage details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Stage not found",
            "title": "Stage not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Stage not found"},
                },
            },
        },
    },
)
def get_stage(
    stage_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a stage."""
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(StageRead.model_validate(stage)),
    )


@stages_router.get(
    "/stages",
    tags=["stages"],
    description="Get stages.",
    responses={
        status.HTTP_200_OK: {
            "model": list[StageRead],
            "description": "Successful response: stages found",
            "title": "Stage details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Stages not found",
            "title": "Stages not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Stages not found"},
                },
            },
        },
    },
)
def get_stages(
    db: Session = db_session,
) -> JSONResponse:
    """Get all stages."""
    stages = db.query(Stage).order_by(Stage.name).all()
    if not stages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stages not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(StageRead.model_validate(stage)) for stage in stages],
    )


@stages_router.put(
    "/stage/{stage_id}",
    tags=["stages"],
    description="Update stage.",
    responses={
        status.HTTP_200_OK: {
            "model": StageRead,
            "description": "Successful response: stage updated",
            "title": "Stage details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Stage not found",
            "title": "Stage not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Stage not found"},
                },
            },
        },
    },
)
def update_stage(
    stage_id: UUID,
    stage_details: StageUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a stage."""
    check_admin(current_user)
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found",
        )
    for field, value in stage_details:
        setattr(stage, field, value)
    db.add(stage)
    db.commit()
    db.refresh(stage)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(StageRead.model_validate(stage)),
    )


@stages_router.delete(
    "/stage/{stage_id}",
    tags=["stages"],
    description="Delete stage.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: stage deleted",
            "title": "Stage deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Stage not found",
            "title": "Stage not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Stage not found"},
                },
            },
        },
    },
)
def delete_stage(
    stage_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a stage."""
    check_admin(current_user)
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found",
        )
    stage.is_deleted = True
    db.add(stage)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
