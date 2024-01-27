"""Endpoints for tickets"""

import requests
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.config import (
    TICKET_TAILOR_API_KEY,
    TICKET_TAILOR_BASE_URL,
    TICKET_TAILOR_EVENT_ID,
    TICKET_TAILOR_PLAYER_TICKET_TYPE_ID,
)
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerRead
from backend.spectators.spectators_models import Spectator
from backend.tickets.tickets_commands import (
    add_new_player_from_ticket_tailor,
    log_new_tickets,
    calculate_other_questions,
)
from backend.tickets.tickets_schemas import IssuedTicketCreatedEvent
from backend.utils import object_to_dict, generate_uuid

db_session = Depends(get_db)

ticket_router = APIRouter()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


@ticket_router.get("/check_in/{barcode}", tags=["tickets"])
def check_in(barcode: str, db: Session = db_session) -> JSONResponse:
    """Check in a ticket."""

    player: Player | None = (
        db.query(Player)
        .filter(Player.is_deleted.is_(False))
        .filter(Player.barcode == barcode)
        .first()
    )

    spectator: Spectator | None = (
        db.query(Spectator)
        .filter(Spectator.is_deleted.is_(False))
        .filter(Spectator.barcode == barcode)
        .first()
    )

    if player is None and spectator is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Player not found"},
        )

    if player:
        resp = requests.post(
            f"{TICKET_TAILOR_BASE_URL}/check_ins",
            auth=(TICKET_TAILOR_API_KEY, ""),
            headers=headers,
            data={
                "issued_ticket_id": f"{player.ticket_id}",
                "quantity": 1,
            },
        )

        player.checked_in = True
        db.add(player)
        db.commit()
    else:
        resp = requests.post(
            f"{TICKET_TAILOR_BASE_URL}/check_ins",
            auth=(TICKET_TAILOR_API_KEY, ""),
            headers=headers,
            data={
                "issued_ticket_id": f"{spectator.ticket_id}",
                "quantity": 1,
            },
        )

        spectator.checked_in = True
        db.add(spectator)
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
        print(resp.status_code)
        print(resp.content)
        return JSONResponse(
            status_code=resp.status_code,
            content={"message": "Ticket check in failed"},
        )


@ticket_router.post("/webhook_ticket_created", tags=["tickets"])
def webhook_ticket_created(
    data: IssuedTicketCreatedEvent,
    db: Session = db_session,
) -> JSONResponse:
    """Webhook for ticket created event."""

    barcode = data.payload.barcode
    ticket_id = data.payload.id
    order_id = data.payload.order_id

    if data.payload.ticket_type_id == TICKET_TAILOR_PLAYER_TICKET_TYPE_ID:
        player = add_new_player_from_ticket_tailor(data.payload, db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
        )
    else:
        (
            allergies_medical_conditions_answer,
            emergency_contact_name_answer,
            emergency_contact_number_answer,
            emergency_contact_relation_answer,
            original_chapter,
        ) = calculate_other_questions(data.payload)
        spectator = Spectator(
            id=generate_uuid(),
            name=data.payload.full_name,
            email=data.payload.email.lower(),
            order_id=order_id,
            ticket_id=ticket_id,
            barcode=barcode,
            checked_in=True if data.payload.checked_in == "true" else False,
            ticket_voided=False if data.payload.status == "valid" else True,
            emergency_contact_name=emergency_contact_name_answer,
            emergency_contact_number=emergency_contact_number_answer,
            emergency_contact_phone=emergency_contact_relation_answer,
            allergies_medical_conditions=allergies_medical_conditions_answer,
            original_chapter=original_chapter,
        )

        db.add(spectator)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(spectator, format_date=True),
        )


@ticket_router.post("/webhook_ticket_updated", tags=["tickets"])
def webhook_ticket_updated(
    data: IssuedTicketCreatedEvent,
    db: Session = db_session,
) -> JSONResponse:
    """Webhook for ticket created event."""

    barcode = data.payload.barcode
    ticket_id = data.payload.id
    order_id = data.payload.order_id

    if data.payload.ticket_type_id == TICKET_TAILOR_PLAYER_TICKET_TYPE_ID:
        player: Player | None = (
            db.query(Player)
            .filter(Player.ticket_id == ticket_id)
            .filter(Player.is_deleted.is_(False))
            .first()
        )

        if player:
            player.name = data.payload.full_name
            player.email = data.payload.email.lower()
            player.order_id = order_id
            player.ticket_id = ticket_id
            player.barcode = barcode
            player.checked_in = True if data.payload.checked_in == "true" else False
            player.ticket_voided = False if data.payload.status == "valid" else True
            db.add(player)
            db.commit()

        else:
            player = add_new_player_from_ticket_tailor(data.payload, db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
        )
    else:
        spectator: Spectator | None = (
            db.query(Spectator)
            .filter(Spectator.ticket_id == ticket_id)
            .filter(Spectator.is_deleted.is_(False))
            .first()
        )

        if spectator:
            spectator.name = data.payload.full_name
            spectator.email = data.payload.email.lower()
            spectator.order_id = order_id
            spectator.ticket_id = ticket_id
            spectator.barcode = barcode
            spectator.checked_in = True if data.payload.checked_in == "true" else False
            spectator.ticket_voided = False if data.payload.status == "valid" else True

        else:
            spectator = Spectator(
                id=generate_uuid(),
                name=data.payload.full_name,
                email=data.payload.email.lower(),
                order_id=order_id,
                ticket_id=ticket_id,
                barcode=barcode,
                checked_in=True if data.payload.checked_in == "true" else False,
                ticket_voided=False if data.payload.status == "valid" else True,
            )

        db.add(spectator)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(spectator, format_date=True),
        )


@ticket_router.get("/get_all_tickets", tags=["tickets"])
def get_all_tickets(
    db: Session = db_session,
) -> JSONResponse:
    """Get all tickets."""
    resp = requests.get(
        f"{TICKET_TAILOR_BASE_URL}/issued_tickets?event_id={TICKET_TAILOR_EVENT_ID}",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
    )

    if resp.status_code == status.HTTP_200_OK:
        tickets: list[dict] = resp.json()["data"]
        log_new_tickets(db, tickets)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Tickets fetch failed"},
        )

    x = False
    next_endpoint = None
    if resp.json()["links"]["next"] is not None:
        next_endpoint = resp.json()["links"]["next"]
        x = True
    while x and next_endpoint is not None:
        resp = requests.get(f"https://api.tickettailor.com{next_endpoint}")
        if resp.status_code == status.HTTP_200_OK:
            tickets: list[dict] = resp.json()["data"]
            log_new_tickets(db, tickets)
            if resp.json()["links"]["next"] is not None:
                next_endpoint = resp.json()["links"]["next"]
            else:
                x = False
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Tickets fetch failed"},
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Tickets fetched successfully"},
    )
