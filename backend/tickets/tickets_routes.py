"""Endpoints for tickets"""
from datetime import datetime
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from backend.commands.get_paginated_result import GetPaginatedResult
from backend.config import (
    TICKET_TAILOR_API_KEY,
    TICKET_TAILOR_BASE_URL,
    TICKET_TAILOR_EVENT_ID,
)
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerRead
from backend.schemas import SortBy, PaginationResult
from backend.spectators.spectators_models import Spectator
from backend.spectators.spectators_schemas import SpectatorRead
from backend.tickets.tickets_commands import (
    log_new_tickets,
    create_ticket,
    update_ticket,
)
from backend.tickets.tickets_models import Ticket
from backend.tickets.tickets_schemas import (
    IssuedTicketCreatedEvent,
    Payload,
    TicketRead,
)
from backend.utils import object_to_dict

db_session = Depends(get_db)

ticket_router = APIRouter()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


def check_ticket(ticket: Ticket) -> bool:
    """Check if ticket is valid."""
    resp = requests.get(
        f"{TICKET_TAILOR_BASE_URL}/issued_tickets/{ticket.ticket_id}",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
    )

    if resp.status_code == status.HTTP_200_OK:
        try:
            ticket = Payload(**resp.json())
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ticket fetch failed with status code {resp.status_code} and { resp.text }. Please refer them to the registration desk.",
            ) from e
        if ticket.status != "valid":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket voided. Please refer them to the registration desk.",
            )
        elif ticket.checked_in == "true":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket already checked in. Please refer them to the registration desk.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticket fetch failed with status code {resp.status_code} and { resp.text }. Please refer them to the registration desk.",
        )

    return True


@ticket_router.get("/check_in/{barcode}", tags=["tickets"])
def check_in(barcode: str, db: Session = db_session) -> JSONResponse:
    """Check in a ticket."""
    ticket: Ticket = db.query(Ticket).filter(Ticket.barcode == barcode).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket not found. Please refer them to the registration desk.",
        )

    check_ticket(ticket)

    resp = requests.post(
        f"{TICKET_TAILOR_BASE_URL}/check_ins",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
        data={
            "issued_ticket_id": f"{ticket.ticket_id}",
            "quantity": 1,
        },
    )

    if resp.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED}:
        ticket.checked_in = True
        db.add(ticket)
        db.commit()

        if ticket.player_id:
            player = db.get(Player, ticket.player_id)

            if player is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ticket checked in but player not found. Please refer them to the registration desk.",
                )

            if player.is_deleted is True:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Player has been deleted. Please refer them to the registration desk.",
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=object_to_dict(
                    PlayerRead.model_validate(player),
                    format_date=True,
                ),
            )
        elif ticket.spectator_id:
            spectator = db.get(Spectator, ticket.spectator_id)

            if spectator is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ticket checked in but spectator not found. Please refer them to the registration desk.",
                )

            if spectator.is_deleted is True:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Spectator has been deleted. Please refer them to the registration desk.",
                )

            return JSONResponse(
                status_code=status.HTTP_207_MULTI_STATUS,
                content=object_to_dict(
                    SpectatorRead(
                        id=spectator.id,
                        name=spectator.name,
                        email=spectator.email,
                    ),
                    format_date=True,
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket checked in but player/spectator not found. Please refer them to the registration desk.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Check in failed with status code {resp.status_code} and { resp.text }. Please refer them to the registration desk.",
        )


@ticket_router.post("/webhook_ticket_created", tags=["tickets"])
def webhook_ticket_created(
    data: IssuedTicketCreatedEvent,
    db: Session = db_session,
) -> JSONResponse:
    """Webhook for ticket created event."""
    return create_ticket(data.payload, db)


@ticket_router.post("/webhook_ticket_updated", tags=["tickets"])
def webhook_ticket_updated(
    data: IssuedTicketCreatedEvent,
    db: Session = db_session,
) -> JSONResponse:
    """Webhook for ticket updated event."""
    resp = requests.get(
        f"{TICKET_TAILOR_BASE_URL}/issued_tickets/{data.payload.id}",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
    )

    if resp.status_code == status.HTTP_200_OK:
        ticket: Payload = Payload(**resp.json())

        return update_ticket(ticket, db)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticket fetch failed with status code {resp.status_code} and { resp.text }.",
        )


@ticket_router.get("/get_all_tickets", tags=["tickets"])
def get_all_tickets(
    db: Session = db_session,
) -> JSONResponse:
    """Get all tickets."""
    resp = requests.get(
        f"{TICKET_TAILOR_BASE_URL}/issued_tickets",
        auth=(TICKET_TAILOR_API_KEY, ""),
        headers=headers,
        params={"event_id": TICKET_TAILOR_EVENT_ID},
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
        url = f"https://api.tickettailor.com/v1{next_endpoint}"
        resp = requests.get(
            url,
            auth=(TICKET_TAILOR_API_KEY, ""),
            headers=headers,
            params={"event_id": TICKET_TAILOR_EVENT_ID},
        )
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
                content={
                    "message": f"Tickets fetch failed with {resp.status_code} and {resp.text}",
                },
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Tickets fetched successfully"},
    )


@ticket_router.get("/tickets", tags=["tickets"])
def list_tickets(
    cursor_column: datetime | str | None = None,
    cursor_id: UUID | None = None,
    previous: bool | None = None,
    per_page: int | None = 20,
    filter_by: str | None = None,
    sort_by: SortBy | None = SortBy.date_asc,
    db: Session = db_session,
) -> PaginationResult:
    """Get all tickets."""
    pagination = GetPaginatedResult()

    filters = []

    if filter_by is not None and filter_by != "":
        filters.append(
            or_(
                Ticket.first_name.ilike(f"%{filter_by}%"),
                Ticket.last_name.ilike(f"%{filter_by}%"),
            ),
        )

    query = (
        db.query(Ticket)
        .filter(*filters)
        .order_by(
            pagination.get_sort_by(
                Ticket.first_name,
                Ticket.created_date,
                sort_by,
            ),
            Ticket.id.desc(),
        )
    )
    return pagination.run(
        cursor_id,
        cursor_column,
        previous,
        query,
        TicketRead,
        per_page,
    )


@ticket_router.get("/tickets/{ticket_id}", tags=["tickets"])
def get_ticket(
    ticket_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a ticket."""
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TicketRead.model_validate(ticket), format_date=True),
    )
