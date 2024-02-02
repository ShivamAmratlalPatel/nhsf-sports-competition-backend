"""Endpoints for spectators"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.spectators.spectators_models import Spectator
from backend.spectators.spectators_schemas import SpectatorRead
from backend.users.users_commands.get_users import get_current_active_user
from backend.utils import object_to_dict

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
