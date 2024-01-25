"""Endpoints for tickets"""
import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.config import TICKET_TAILOR_BASE_URL, TICKET_TAILOR_API_KEY
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerRead
from backend.utils import object_to_dict

db_session = Depends(get_db)

ticket_router = APIRouter()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


@ticket_router.get("/check_in/{ticket_id}", tags=["tickets"])
def check_in(ticket_id: str, db: Session = db_session) -> JSONResponse:
    resp = requests.post(
        f"{TICKET_TAILOR_BASE_URL}/check_ins",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
        data={
            "issued_ticket_id": f"{ticket_id}",
            "quantity": 1,
        },
    )

    player = (
        db.query(Player)
        .filter(Player.is_deleted.is_(False))
        .filter(Player.ticket_id == ticket_id)
        .first()
    )

    if player:
        player.checked_in = True
        db.add(player)
        db.commit()

    if resp.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED} and player:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
        )
    elif (
        resp.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED} and not player
    ):
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Ticket checked in successfully but no player found"},
        )
    else:
        return JSONResponse(
            status_code=resp.status_code,
            content={"message": "Ticket check in failed"},
        )
