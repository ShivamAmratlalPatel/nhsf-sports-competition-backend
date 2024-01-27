"""Endpoints for tickets"""

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.config import (
    TICKET_TAILOR_API_KEY,
    TICKET_TAILOR_BASE_URL,
)
from backend.helpers import get_db
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerRead
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.tickets.tickets_schemas import IssuedTicketCreatedEvent
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


@ticket_router.post("/webhook_ticket_created", tags=["tickets"])
def webhook_ticket_created(
    data: IssuedTicketCreatedEvent,
    db: Session = db_session,
) -> JSONResponse:
    """Webhook for ticket created event."""

    barcode = data.payload.barcode
    ticket_id = data.payload.id
    order_id = data.payload.order_id

    if data.payload.ticket_type_id == "tt_3815953":
        morning_sport_answer = next(
            (
                question.answer
                for question in data.payload.custom_questions
                if question.question == "What sport are you playing in the morning?"
            ),
            None,
        )

        if morning_sport_answer is None:
            print("Morning Sport Answer not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mornings Sport Answer not found",
            )

        afternoon_sport_answer = next(
            (
                question.answer
                for question in data.payload.custom_questions
                if question.question == "What sport are you playing in the afternoon?"
            ),
            None,
        )

        if afternoon_sport_answer is None:
            print("Afternoon Sport Answer not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Afternoon Sport Answer not found",
            )

        chapter_answer = next(
            (
                question.answer
                for question in data.payload.custom_questions
                if question.question == "What chapter are you from?"
            ),
            None,
        )

        if chapter_answer is None:
            print("Chapter answer not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chapter answer not found",
            )
        chapter_name = chapter_answer

        chapter: Chapter | None = (
            db.query(Chapter)
            .filter(Chapter.name == chapter_name)
            .filter(Chapter.is_deleted.is_(False))
            .first()
        )

        if chapter is None:
            print("Chapter not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chapter not found",
            )

        if morning_sport_answer == "Kabaddi Mens":
            morning_sport_answer = "KabaddiM"
        elif afternoon_sport_answer == "Kabaddi Womens":
            afternoon_sport_answer = "KabaddiF"

        if morning_sport_answer == "None":
            morning_team_id = None
        else:
            morning_sport: Sport | None = (
                db.query(Sport)
                .filter(Sport.name == morning_sport_answer)
                .filter(Sport.is_deleted.is_(False))
                .first()
            )
            if morning_sport is None:
                print("Morning sport not found")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Morning sport not found",
                )
            morning_team: Team | None = (
                db.query(Team)
                .filter(Team.chapter_id == chapter.id)
                .filter(Team.sport_id == morning_sport.id)
                .filter(Team.is_deleted.is_(False))
                .first()
            )
            if morning_team is None:
                print("Morning team not found")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Morning team not found",
                )
            morning_team_id = morning_team.id

        if afternoon_sport_answer == "None":
            afternoon_team_id = None
        else:
            afternoon_sport: Sport | None = (
                db.query(Sport)
                .filter(Sport.name == afternoon_sport_answer)
                .filter(Sport.is_deleted.is_(False))
                .first()
            )
            if afternoon_sport is None:
                print("Afternoon sport not found")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Afternoon sport not found",
                )
            afternoon_team: Team | None = (
                db.query(Team)
                .filter(Team.chapter_id == chapter.id)
                .filter(Team.sport_id == afternoon_sport.id)
                .filter(Team.is_deleted.is_(False))
                .first()
            )
            if afternoon_team is None:
                print("Afternoon team not found")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Afternoon team not found",
                )
            afternoon_team_id = afternoon_team.id

        existing_player: Player | None = (
            db.query(Player)
            .filter(Player.is_deleted.is_(False))
            .filter(Player.email == data.payload.email.lower())
            .first()
        )

        if existing_player:
            existing_player.order_id = order_id
            existing_player.ticket_id = ticket_id
            existing_player.barcode = barcode
            existing_player.morning_team_id = morning_team_id
            existing_player.afternoon_team_id = afternoon_team_id

            db.add(existing_player)
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=object_to_dict(
                    PlayerRead.model_validate(existing_player), format_date=True
                ),
            )
        else:
            player = Player(
                name=data.payload.full_name,
                email=data.payload.email.lower(),
                order_id=order_id,
                ticket_id=ticket_id,
                barcode=barcode,
                morning_team_id=morning_team_id,
                afternoon_team_id=afternoon_team_id,
                cards=[],
            )

            db.add(player)
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=object_to_dict(
                    PlayerRead.model_validate(player), format_date=True
                ),
            )
