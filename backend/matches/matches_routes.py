"""Ednpoints for matches"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.matches.matches_models import Match, MatchAudit
from backend.matches.matches_schemas import (
    MatchCreate,
    MatchRead,
    MatchUpdate,
    ScoreDetails,
    KnockoutRead,
)
from backend.matches.mathes_commands.generate_schedule import (
    generate_schedule_for_group,
    randomly_assign_groups,
    check_teams,
    get_list_of_teams_for_sport,
    check_matches_have_not_been_generated,
)
from backend.matches.mathes_commands.get_team_from_match import (
    get_away_team_from_match,
    get_home_team_from_match,
)
from backend.sports.sports_models import Sport
from backend.tables.tables_commands.update_knockout import update_knockout_for_match
from backend.tables.tables_commands.update_table import update_table_for_match
from backend.tables.tables_models import LeagueTable
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict, generate_uuid, datetime_now

from backend.teams.teams_models import Team

matches_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@matches_router.post(
    "/match",
    tags=["matches"],
    description="Create match.",
    responses={
        status.HTTP_201_CREATED: {
            "model": MatchRead,
            "description": "Successful response: match created",
            "title": "Match details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Match already exists",
            "title": "Match already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Match already exists"},
                },
            },
        },
    },
)
def create_match(
    match_details: MatchCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a match."""
    match = Match(**match_details.model_dump())
    db.add(match)
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match already exists",
        ) from e
    db.refresh(match)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.get(
    "/match/{match_id}",
    tags=["matches"],
    description="Get match.",
    responses={
        status.HTTP_200_OK: {
            "model": MatchRead,
            "description": "Successful response: match found",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def get_match(
    match_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.get(
    "/matches",
    tags=["matches"],
    description="Get matches.",
    responses={
        status.HTTP_200_OK: {
            "model": list[MatchRead],
            "description": "Successful response: matches found",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Matches not found",
            "title": "Matches not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Matches not found"},
                },
            },
        },
    },
)
def get_matches(
    db: Session = db_session,
) -> JSONResponse:
    """Get all matches."""
    matches = db.query(Match).all()
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matches not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[object_to_dict(MatchRead.model_validate(match)) for match in matches],
    )


@matches_router.put(
    "/match/{match_id}",
    tags=["matches"],
    description="Update match.",
    responses={
        status.HTTP_200_OK: {
            "model": MatchRead,
            "description": "Successful response: match updated",
            "title": "Match details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def update_match(
    match_id: UUID,
    match_details: MatchUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a match."""
    match: Match | None = db.query(Match).filter(Match.id == match_id).first()
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    for field, value in match_details.__dict__.items():
        if field != "id":
            setattr(match, field, value)
    db.add(match)
    db.commit()
    update_table_for_match(match, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatchRead.model_validate(match)),
    )


@matches_router.delete(
    "/match/{match_id}",
    tags=["matches"],
    description="Delete match.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: match deleted",
            "title": "Match deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Match not found",
            "title": "Match not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Match not found"},
                },
            },
        },
    },
)
def delete_match(
    match_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a match."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    db.delete(match)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


def get_group_from_match(db: Session, match: Match) -> int:
    home_team = get_home_team_from_match(db=db, match=match)

    return home_team.group


@matches_router.get(
    "/schedule/{sport_id}",
    tags=["matches"],
    description="Get schedule.",
    responses={
        status.HTTP_200_OK: {
            "model": list[MatchRead],
            "description": "Successful response: schedule found",
            "title": "Schedule details",
        },
    },
)
def get_schedule(
    sport_id: UUID,
    team_id: UUID | None = None,
    db: Session = db_session,
) -> JSONResponse:
    """Get schedule."""
    filters = [
        Match.sport_id == sport_id,
        Match.is_deleted.is_(False),
        Match.stage_id == 0,
    ]

    played_matches: list[Match] = (
        db.query(Match)
        .filter(*filters)
        .filter(Match.home_score.is_not(None))
        .order_by(Match.time)
        .order_by(Match.id)
        .all()
    )

    if played_matches is None:
        played_matches = []

    unplayed_matches_with_pitches: list[Match] = (
        db.query(Match)
        .filter(*filters)
        .filter(Match.home_score.is_(None))
        .filter(Match.pitch_id.is_not(None))
        .order_by(Match.time)
        .order_by(Match.id)
        .all()
    )

    if unplayed_matches_with_pitches is None:
        unplayed_matches_with_pitches = []

    unplayed_matches_without_pitches: list[Match] = (
        db.query(Match)
        .filter(*filters)
        .filter(Match.home_score.is_(None))
        .filter(Match.pitch_id.is_(None))
        .order_by(Match.time)
        .order_by(Match.id)
        .all()
    )

    if unplayed_matches_without_pitches is None:
        unplayed_matches_without_pitches = []

    matches = (
        played_matches
        + unplayed_matches_with_pitches
        + unplayed_matches_without_pitches
    )

    # TODO optimise this query and make it a function to be used elsewhere
    teams = (
        db.query(Team)
        .filter(Team.sport_id == sport_id)
        .filter(Team.is_deleted.is_(False))
        .all()
    )

    if not teams or teams == []:
        return JSONResponse(status_code=200, content=[])

    try:
        max_groups = max([team.group for team in teams])
    except TypeError:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[
                [object_to_dict(MatchRead.model_validate(match)) for match in matches],
            ],
        )

    output = []
    for i in range(max_groups):
        output.append(
            [
                object_to_dict(MatchRead.model_validate(match))
                for match in matches
                if get_group_from_match(db, match) == i + 1
            ],
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )


@matches_router.put(
    "/match/{match_id}/log_score",
    tags=["matches"],
)
def log_score(
    match_id: UUID,
    score_details: ScoreDetails,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Log score for a match."""
    check_admin(current_user)

    match: Match | None = db.get(Match, match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    match.home_score = score_details.home_score
    match.away_score = score_details.away_score
    match.home_penalties = score_details.home_penalties
    match.away_penalties = score_details.away_penalties

    match_audit = MatchAudit(
        id=generate_uuid(),
        match_id=match.id,
        home_score=match.home_score,
        away_score=match.away_score,
        home_penalties=match.home_penalties,
        away_penalties=match.away_penalties,
        actioner=current_user.full_name
        if current_user and current_user.full_name
        else "Unknown",
    )

    db.add(match_audit)

    db.add(match)
    db.commit()

    if match.stage_id == 0:
        update_table_for_match(match, db)
    else:
        update_knockout_for_match(match, db)

    return JSONResponse(
        status_code=200,
        content=object_to_dict(MatchRead.model_validate(match), format_date=True),
    )


@matches_router.get(
    "/knockout/{sport_id}",
    tags=["matches"],
)
def get_knockout_matches(
    sport_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get knockout matches."""
    sport: Sport = db.get(Sport, sport_id)

    qf1 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 1)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    qf2 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 2)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    qf3 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 3)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    qf4 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 4)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    sf1 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 5)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    sf2 = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 6)
        .filter(Match.is_deleted.is_(False))
        .first()
    )
    final = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.stage_id == 7)
        .filter(Match.is_deleted.is_(False))
        .first()
    )

    matches = [qf1, qf2, qf3, qf4, sf1, sf2, final]

    resp = []

    for i, match in enumerate(matches):
        if match is not None:
            home_team: Team = get_home_team_from_match(db, match)
            away_team: Team = get_away_team_from_match(db, match)
            resp.append(
                object_to_dict(
                    KnockoutRead(
                        id=match.id,
                        stage=match.stage_id,
                        home_team=home_team.name,
                        away_team=away_team.name,
                        home_team_score=float(match.home_score)
                        if match.home_score
                        else None,
                        away_team_score=float(match.away_score)
                        if match.away_score
                        else None,
                        home_team_penalties=float(match.home_penalties)
                        if match.home_penalties
                        else None,
                        away_team_penalties=float(match.away_penalties)
                        if match.away_penalties
                        else None,
                    ),
                ),
            )
        else:
            if i == 0:
                if sport.quarter_finals:
                    home_team = "Quarter Final 1"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 1:
                if sport.quarter_finals:
                    home_team = "Quarter Final 2"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 2:
                if sport.quarter_finals:
                    home_team = "Quarter Final 3"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 3:
                if sport.quarter_finals:
                    home_team = "Quarter Final 4"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 4:
                if sport.quarter_finals and sport.semi_finals:
                    home_team = "Winner of QF1"
                    away_team = "Winner of QF2"
                elif sport.semi_finals:
                    home_team = "Semi Final 1"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 5:
                if sport.quarter_finals and sport.semi_finals:
                    home_team = "Winner of QF3"
                    away_team = "Winner of QF4"
                elif sport.semi_finals:
                    home_team = "Semi Final 2"
                    away_team = ""
                else:
                    home_team = ""
                    away_team = ""
            elif i == 6:
                if sport.semi_finals:
                    home_team = "Winner of SF1"
                    away_team = "Winner of SF2"
                else:
                    home_team = ""
                    away_team = ""
            else:
                home_team = ""
                away_team = ""

            resp.append(
                object_to_dict(
                    KnockoutRead(
                        id=None,
                        stage=i + 1,
                        home_team=home_team,
                        away_team=away_team,
                    ),
                ),
            )
    return JSONResponse(
        status_code=200,
        content=resp,
    )


@matches_router.put(
    "/generate_knockout/{sport_id}",
    tags=["matches"],
)
def generate_knockout(
    sport_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Generate knockout matches."""
    check_admin(current_user)
    table_rows = (
        db.query(LeagueTable)
        .filter(LeagueTable.sport_id == sport_id)
        .filter(LeagueTable.is_deleted.is_(False))
        .all()
    )

    # Sort by points_per_game, then score_difference_per_game then scores_for_per_game
    table_rows.sort(
        key=lambda x: (
            x.points_per_game,
            x.score_difference_per_game,
            x.scores_for_per_game,
        ),
        reverse=True,
    )

    sport = db.get(Sport, sport_id)

    if sport.quarter_finals:
        qf1 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=1,
            home_team_id=table_rows[0].team_id,
            away_team_id=table_rows[7].team_id,
        )
        qf2 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=3,
            home_team_id=table_rows[1].team_id,
            away_team_id=table_rows[6].team_id,
        )
        qf3 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=3,
            home_team_id=table_rows[2].team_id,
            away_team_id=table_rows[5].team_id,
        )
        qf4 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=4,
            home_team_id=table_rows[3].team_id,
            away_team_id=table_rows[4].team_id,
        )
        db.add(qf1)
        db.add(qf2)
        db.add(qf3)
        db.add(qf4)
    elif sport.semi_finals:
        sf1 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=5,
            home_team_id=table_rows[0].team_id,
            away_team_id=table_rows[3].team_id,
        )
        sf2 = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=6,
            home_team_id=table_rows[1].team_id,
            away_team_id=table_rows[2].team_id,
        )
        db.add(sf1)
        db.add(sf2)
    else:
        final = Match(
            id=generate_uuid(),
            sport_id=sport_id,
            stage_id=7,
            home_team_id=table_rows[0].team_id,
            away_team_id=table_rows[1].team_id,
        )
        db.add(final)
    db.commit()
    return JSONResponse(status_code=200, content={})


@matches_router.put(
    "/generate_schedule/{sport_id}",
    tags=["matches"],
)
def generate_schedule(
    sport_id: UUID,
    number_of_groups: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Generate schedule for a sport."""
    check_admin(current_user)

    check_matches_have_not_been_generated(db, sport_id)

    teams = get_list_of_teams_for_sport(db, sport_id)

    check_teams(teams)

    randomly_assign_groups(db, number_of_groups, teams)

    generate_schedule_for_group(db, number_of_groups, sport_id)


@matches_router.get("/unassigned_matches/{sport_id}", tags=["matches"])
def any_unassigned_matches(sport_id: UUID, db: Session = db_session) -> bool:
    """Check if there are any unassigned matches."""
    games = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.is_deleted.is_(False))
        .filter(Match.pitch_id.is_(None))
        .all()
    )

    return bool(games)


@matches_router.put("/match/{match_id}/pitch_edit/{pitch_id}", tags=["matches"])
def edit_pitch(
    match_id: UUID,
    pitch_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)

    match: Match = db.get(Match, match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    else:
        match.pitch_id = pitch_id
        match.time = datetime_now()
        db.add(match)
        db.commit()
        return JSONResponse(status_code=200, content="Match pitch updated")
