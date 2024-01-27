from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.config import TICKET_TAILOR_PLAYER_TICKET_TYPE_ID
from backend.errors.errors_models import Error
from backend.players.players_models import Player
from backend.spectators.spectators_models import Spectator
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.tickets.tickets_schemas import Payload
from backend.utils import generate_uuid, object_to_dict


def add_new_player_from_ticket_tailor(payload: Payload, db: Session) -> Player:
    morning_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which morning sport are you playing?"
        ),
        None,
    )
    if morning_sport_answer is None:
        player = Player(
            id=generate_uuid(),
            name=payload.full_name,
            email=payload.email.lower(),
            order_id=payload.order_id,
            ticket_id=payload.id,
            barcode=payload.barcode_url,
            cards=[],
            checked_in=True if payload.checked_in == "true" else False,
            ticket_voided=False if payload.status == "valid" else True,
        )
        db.add(player)
        db.commit()
        return player
    afternoon_sport_answer = next(
        (
            question.answer
            for question in payload.custom_questions
            if question.question == "Which afternoon sport are you playing?"
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
            for question in payload.custom_questions
            if question.question == "Which University/School are you playing for?"
        ),
        None,
    )
    if chapter_answer is None:
        print("Chapter answer not found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter answer not found",
        )
    chapter: Chapter | None = (
        db.query(Chapter)
        .filter(Chapter.name == chapter_answer)
        .filter(Chapter.is_deleted.is_(False))
        .first()
    )
    if chapter is None:
        print("Chapter not found")
        print(chapter_answer)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter not found",
        )
    if morning_sport_answer == "Kabaddi Womens":
        morning_sport_answer = "KabaddiF"
    if afternoon_sport_answer == "Kabaddi Mens":
        afternoon_sport_answer = "KabaddiM"
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
            error = Error(
                id=generate_uuid(),
                error=f"Morning team not found for {payload.full_name}",
                data=object_to_dict(payload, format_date=True),
            )
            db.add(error)
            db.commit()
            morning_team_id = None
        else:
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
            print(payload)
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
            error = Error(
                id=generate_uuid(),
                error=f"Afternoon team not found for {payload.full_name}",
                data=object_to_dict(payload, format_date=True),
            )
            db.add(error)
            db.commit()
            afternoon_team_id = None
        else:
            afternoon_team_id = afternoon_team.id

    (
        allergies_medical_conditions_answer,
        emergency_contact_name_answer,
        emergency_contact_number_answer,
        emergency_contact_relation_answer,
        original_chapter,
    ) = calculate_other_questions(payload)

    player = Player(
        id=generate_uuid(),
        name=payload.full_name,
        email=payload.email.lower(),
        order_id=payload.order_id,
        ticket_id=payload.id,
        barcode=payload.barcode,
        morning_team_id=morning_team_id,
        afternoon_team_id=afternoon_team_id,
        cards=[],
        checked_in=True if payload.checked_in == "true" else False,
        ticket_voided=False if payload.status == "valid" else True,
        emergency_contact_name=emergency_contact_name_answer,
        emergency_contact_number=emergency_contact_number_answer,
        emergency_contact_phone=emergency_contact_relation_answer,
        allergies_medical_conditions=allergies_medical_conditions_answer,
        original_chapter=original_chapter,
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
            == "If you are playing for another university/school, please write your university here"
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
            if question.question == "Emergency Contact Number"
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
        (
            allergies_medical_conditions_answer,
            emergency_contact_name_answer,
            emergency_contact_number_answer,
            emergency_contact_relation_answer,
            original_chapter,
        ) = calculate_other_questions(payload)
        if payload.ticket_type_id == TICKET_TAILOR_PLAYER_TICKET_TYPE_ID:
            player: Player | None = (
                db.query(Player)
                .filter(Player.is_deleted.is_(False))
                .filter(Player.ticket_id == ticket["id"])
                .first()
            )

            if player:
                player.name = payload.full_name
                player.email = payload.email
                player.order_id = payload.order_id
                player.ticket_id = payload.id
                player.barcode = payload.barcode
                player.checked_in = True if payload.checked_in == "true" else False
                player.ticket_voided = False if payload.status == "valid" else True
                player.emergency_contact_name = emergency_contact_name_answer
                player.emergency_contact_number = emergency_contact_number_answer
                player.emergency_contact_phone = emergency_contact_relation_answer
                player.allergies_medical_conditions = (
                    allergies_medical_conditions_answer
                )
                db.add(player)
                db.commit()
                continue
            else:
                add_new_player_from_ticket_tailor(payload, db)
        else:
            spectator: Spectator | None = (
                db.query(Spectator)
                .filter(Spectator.is_deleted.is_(False))
                .filter(Spectator.ticket_id == ticket["id"])
                .first()
            )

            if spectator:
                spectator.name = ticket["full_name"]
                spectator.email = ticket["email"]
                spectator.order_id = ticket["order_id"]
                spectator.ticket_id = ticket["id"]
                spectator.barcode = ticket["barcode"]
                spectator.checked_in = True if ticket["checked_in"] == "true" else False
                spectator.ticket_voided = False if ticket["status"] == "valid" else True
                spectator.emergency_contact_name = emergency_contact_name_answer
                spectator.emergency_contact_number = emergency_contact_number_answer
                spectator.emergency_contact_phone = emergency_contact_relation_answer
                spectator.allergies_medical_conditions = (
                    allergies_medical_conditions_answer
                )
                db.add(spectator)
                db.commit()
                continue
            else:
                spectator = Spectator(
                    name=ticket["full_name"],
                    email=ticket["email"],
                    order_id=ticket["order_id"],
                    ticket_id=ticket["id"],
                    barcode=ticket["barcode"],
                    checked_in=True if ticket["checked_in"] == "true" else False,
                    ticket_voided=False if ticket["status"] == "valid" else True,
                    emergency_contact_name=emergency_contact_name_answer,
                    emergency_contact_number=emergency_contact_number_answer,
                    emergency_contact_phone=emergency_contact_relation_answer,
                    allergies_medical_conditions=allergies_medical_conditions_answer,
                )
                db.add(spectator)
                db.commit()
