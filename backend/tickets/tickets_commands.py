from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.config import (
    TICKET_TAILOR_PLAYER_TICKET_TYPE_ID,
    TICKET_TAILOR_EVENT_ID,
)
from backend.errors.errors_models import Error
from backend.players.players_models import Player
from backend.players.players_schemas import PlayerRead
from backend.spectators.spectators_models import Spectator
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.tickets.tickets_models import Ticket
from backend.tickets.tickets_schemas import Payload
from backend.utils import generate_uuid, object_to_dict, datetime_now


def add_new_player_from_ticket_tailor(ticket: Ticket, db: Session) -> Player:
    chapter = None
    if ticket.chapter is None:
        morning_team_id = None
        afternoon_team_id = None
    else:
        chapter: Chapter | None = (
            db.query(Chapter)
            .filter(Chapter.name == ticket.chapter)
            .filter(Chapter.is_deleted.is_(False))
            .first()
        )
        if chapter is not None:
            if ticket.morning_sport == "Kabaddi (Women)":
                morning_sport_answer = "KabaddiW"
            else:
                morning_sport_answer = ticket.morning_sport
            if ticket.morning_sport == "None" or ticket.morning_sport is None:
                morning_team_id = None
            else:
                morning_sport: Sport | None = (
                    db.query(Sport)
                    .filter(Sport.name == morning_sport_answer)
                    .filter(Sport.is_deleted.is_(False))
                    .first()
                )
                if morning_sport is None:
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
                    error = Error(
                        id=generate_uuid(),
                        error=f"Morning team not found for {ticket.full_name}",
                        data=object_to_dict(ticket, format_date=True),
                        created_date=datetime_now(),
                    )
                    db.add(error)
                    db.commit()
                    morning_team_id = None
                else:
                    morning_team_id = morning_team.id
            if ticket.afternoon_sport == "Kabaddi (Men)":
                afternoon_sport_answer = "Kabaddi (Men)"
            elif ticket.afternoon_sport == "Kabaddi (Women)":
                afternoon_sport_answer = "Kabaddi (Women)"
            elif ticket.afternoon_sport == "Kho-Kho":
                afternoon_sport_answer = "Kho"
            else:
                afternoon_sport_answer = ticket.afternoon_sport
            if ticket.afternoon_sport == "None" or ticket.afternoon_sport is None:
                afternoon_team_id = None
            else:
                afternoon_sport: Sport | None = (
                    db.query(Sport)
                    .filter(Sport.name == afternoon_sport_answer)
                    .filter(Sport.is_deleted.is_(False))
                    .first()
                )
                if afternoon_sport is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Afternoon sport not found for {ticket.full_name}",
                    )
                afternoon_team: Team | None = (
                    db.query(Team)
                    .filter(Team.chapter_id == chapter.id)
                    .filter(Team.sport_id == afternoon_sport.id)
                    .filter(Team.is_deleted.is_(False))
                    .first()
                )
                if afternoon_team is None:
                    error = Error(
                        id=generate_uuid(),
                        error=f"Afternoon team not found for {ticket.full_name}",
                        data=object_to_dict(ticket, format_date=True),
                        created_date=datetime_now(),
                    )
                    db.add(error)
                    db.commit()
                    afternoon_team_id = None
                else:
                    afternoon_team_id = afternoon_team.id
        else:
            morning_team_id = None
            afternoon_team_id = None

    if morning_team_id is None and afternoon_team_id is None:
        error = Error(
            id=generate_uuid(),
            error=f"Chapter not found for {ticket.full_name}",
            data=object_to_dict(ticket, format_date=True),
        )
        db.add(error)
        db.commit()
        player = Player(
            id=generate_uuid(),
            name=ticket.full_name,
            email=ticket.email,
            morning_team_id=morning_team_id,
            afternoon_team_id=afternoon_team_id,
            created_date=datetime_now(),
        )
        db.add(player)
        db.commit()
        return player
    elif chapter is not None:
        player = (
            db.query(Player)
            .filter(Player.name == ticket.full_name)
            .filter(
                or_(
                    Player.morning_team_id == morning_team_id,
                    Player.afternoon_team_id == afternoon_team_id,
                )
            )
            .filter(Player.is_deleted.is_(False))
            .first()
        )

        if player:
            player.name = ticket.full_name
            player.email = ticket.email
            player.morning_team_id = morning_team_id
            player.afternoon_team_id = afternoon_team_id
            player.last_modified_date = datetime_now()
            db.add(player)
            db.commit()
            return player
        else:
            player = Player(
                id=generate_uuid(),
                name=ticket.full_name,
                email=ticket.email,
                morning_team_id=morning_team_id,
                afternoon_team_id=afternoon_team_id,
                created_date=datetime_now(),
            )
            db.add(player)
            db.commit()
            return player
    else:
        player = Player(
            id=generate_uuid(),
            name=ticket.full_name,
            email=ticket.email,
            morning_team_id=morning_team_id,
            afternoon_team_id=afternoon_team_id,
            created_date=datetime_now(),
        )
        db.add(player)
        db.commit()
        return player


def calculate_other_questions(payload: Payload) -> tuple[str, str, str, str, str]:
    original_chapter = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question
            == "If you are playing for another university/school, please write down who you are representing"
        ),
        None,
    )
    emergency_contact_name_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Emergency Contact Name"
        ),
        None,
    )
    emergency_contact_relation_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Emergency Contact Relation"
        ),
        None,
    )
    emergency_contact_number_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Emergency Contact Phone Number"
        ),
        None,
    )
    allergies_medical_conditions_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Do you have any allergies/medical requirements?"
        ),
        None,
    )
    return (
        allergies_medical_conditions_answer,
        emergency_contact_name_answer,
        emergency_contact_number_answer,
        emergency_contact_relation_answer,
        original_chapter,
    )


def log_new_tickets(db: Session, tickets: list[dict]) -> None:
    for ticket in tickets:
        payload = Payload(**ticket)
        if str(payload.event_id) == TICKET_TAILOR_EVENT_ID:
            db_ticket = db.query(Ticket).filter(Ticket.ticket_id == payload.id).first()

            if db_ticket is None:
                create_ticket(payload, db)
            else:
                update_ticket(payload, db)


def create_ticket(payload: Payload, db: Session) -> JSONResponse:
    if payload.event_id != TICKET_TAILOR_EVENT_ID:
        return JSONResponse(
                status_code=status.HTTP_201_CREATED
            )
    barcode = payload.barcode
    ticket_id = payload.id
    order_id = payload.order_id
    (
        allergies_medical_conditions_answer,
        emergency_contact_name_answer,
        emergency_contact_number_answer,
        emergency_contact_relation_answer,
        original_chapter,
    ) = calculate_other_questions(payload)
    chapter_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which University/School are you representing?"
        ),
        None,
    )
    morning_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which morning sport are you playing?"
        ),
        None,
    )
    afternoon_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which afternoon sport are you playing?"
        ),
        None,
    )

    exisiting_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if exisiting_ticket:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=object_to_dict(exisiting_ticket, format_date=True),
        )
    else:
        ticket = Ticket(
            id=generate_uuid(),
            first_name=payload.first_name,
            last_name=payload.last_name,
            created_date=datetime_now(),
            email=payload.email.lower() if payload.email else None,
            chapter=chapter_answer,
            original_chapter=original_chapter,
            morning_sport=morning_sport_answer,
            afternoon_sport=afternoon_sport_answer,
            emergency_contact_name=emergency_contact_name_answer,
            emergency_contact_number=emergency_contact_number_answer,
            emergency_contact_relationship=emergency_contact_relation_answer,
            allergies_medical_conditions=allergies_medical_conditions_answer,
            order_id=order_id,
            ticket_id=ticket_id,
            barcode=barcode,
            checked_in=payload.checked_in == "true",
            ticket_voided=payload.status != "valid",
            data=object_to_dict(payload, format_date=True),
        )
        db.add(ticket)
        db.commit()
        if payload.ticket_type_id == TICKET_TAILOR_PLAYER_TICKET_TYPE_ID:
            player = add_new_player_from_ticket_tailor(ticket, db)

            ticket.player_id = player.id

            db.add(ticket)
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=object_to_dict(
                    PlayerRead.model_validate(player),
                    format_date=True,
                ),
            )
        else:
            spectator = Spectator(
                id=generate_uuid(),
                name=payload.full_name,
                email=payload.email.lower() if payload.email else None,
            )
            ticket.spectator_id = spectator.id

            db.add(spectator)
            db.add(ticket)

            db.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=object_to_dict(spectator, format_date=True),
            )


def update_ticket(payload: Payload, db):
    if payload.event_id != TICKET_TAILOR_EVENT_ID:
        return JSONResponse(
                status_code=status.HTTP_201_CREATED
            )
    barcode = payload.barcode
    ticket_id = payload.id
    order_id = payload.order_id
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Ticket not found"},
        )
    (
        allergies_medical_conditions_answer,
        emergency_contact_name_answer,
        emergency_contact_number_answer,
        emergency_contact_relation_answer,
        original_chapter,
    ) = calculate_other_questions(payload)
    chapter_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which University/School are you representing?"
        ),
        None,
    )
    morning_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which morning sport are you playing?"
        ),
        None,
    )
    afternoon_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which afternoon sport are you playing?"
        ),
        None,
    )
    ticket.first_name = payload.first_name
    ticket.last_name = payload.last_name
    ticket.email = payload.email.lower() if payload.email else None
    ticket.chapter = chapter_answer
    ticket.original_chapter = original_chapter
    ticket.morning_sport = morning_sport_answer
    ticket.afternoon_sport = afternoon_sport_answer
    ticket.emergency_contact_name = emergency_contact_name_answer
    ticket.emergency_contact_number = emergency_contact_number_answer
    ticket.emergency_contact_relationship = emergency_contact_relation_answer
    ticket.allergies_medical_conditions = allergies_medical_conditions_answer
    ticket.order_id = order_id
    ticket.ticket_id = ticket_id
    ticket.barcode = barcode
    ticket.checked_in = payload.checked_in == "true"
    ticket.ticket_voided = payload.status != "valid"
    ticket.update_data = object_to_dict(payload, format_date=True)
    ticket.last_modified_date = datetime_now()
    if payload.ticket_type_id == TICKET_TAILOR_PLAYER_TICKET_TYPE_ID:
        if ticket.player_id is None:
            player = add_new_player_from_ticket_tailor(ticket, db)
            ticket.player_id = player.id
        player: Player | None = db.get(Player, ticket.player_id)

        if player:
            player.name = payload.full_name
            player.email = payload.email.lower() if payload.email else None
            db.add(player)
            db.commit()

        else:
            player = add_new_player_from_ticket_tailor(ticket, db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(PlayerRead.model_validate(player), format_date=True),
        )
    else:
        if ticket.spectator_id is None:
            spectator = Spectator(
                id=generate_uuid(),
                name=payload.full_name,
                email=payload.email.lower() if payload.email else None,
            )
            ticket.spectator_id = spectator.id
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=object_to_dict(spectator, format_date=True),
            )
        spectator: Spectator | None = db.get(Spectator, ticket.spectator_id)
        if spectator:
            spectator.name = payload.full_name
            spectator.email = payload.email.lower() if payload.email else None

        else:
            spectator = Spectator(
                id=generate_uuid(),
                name=payload.full_name,
                email=payload.email.lower() if payload.email else None,
                created_date=datetime_now(),
            )

        db.add(spectator)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=object_to_dict(spectator, format_date=True),
        )
