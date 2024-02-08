"""Endpoints for teams"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Row, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.matches.matches_models import Match
from backend.players.players_models import Player
from backend.sports.sports_models import Sport
from backend.teams.teams_models import Team
from backend.teams.teams_schemas import (
    TeamCreate,
    TeamCreateAdmin,
    TeamRead,
    TeamUpdate,
)
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import generate_uuid, object_to_dict

teams_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@teams_router.post(
    "/team",
    tags=["teams"],
    description="Create team.",
    responses={
        status.HTTP_201_CREATED: {
            "model": TeamRead,
            "description": "Successful response: team created",
            "title": "Team details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Team already exists",
            "title": "Team already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Team already exists"},
                },
            },
        },
    },
)
def create_team(
    team_details: TeamCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a team."""
    check_admin(current_user)
    team = Team(**team_details.model_dump())
    db.add(team)
    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team already exists",
        ) from e
    db.refresh(team)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.post(
    "/team/admin",
    tags=["teams"],
    description="Create team.",
    responses={
        status.HTTP_201_CREATED: {
            "model": TeamRead,
            "description": "Successful response: team created",
            "title": "Team details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Team already exists",
            "title": "Team already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Team already exists"},
                },
            },
        },
    },
)
def create_team_admin(
    team_details: TeamCreateAdmin,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a team."""
    check_admin(current_user)

    existing_sport_teams: list[Team] | None = (
        db.query(Team)
        .filter(Team.sport_id == team_details.sport_id)
        .filter(Team.chapter_id == team_details.chapter_id)
        .filter(Team.is_deleted.is_(False))
        .all()
    )

    chapter = db.get(Chapter, team_details.chapter_id)
    sport = db.get(Sport, team_details.sport_id)

    new_team = Team(
        id=generate_uuid(),
        name=chapter.name,
        internal_name=sport.name,
        sport_id=team_details.sport_id,
        chapter_id=team_details.chapter_id,
    )

    if existing_sport_teams:
        for team in existing_sport_teams:
            if team.name == chapter.name:
                team.name = f"{team.name} A"
                new_team.name = f"{new_team.name} B"
            elif team.name == f"{chapter.name} A":
                new_team.name = f"{new_team.name} B"
            elif team.name == f"{chapter.name} B":
                new_team.name = f"{new_team.name} C"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Too many teams",
                )
            db.add(team)
    db.add(new_team)

    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(TeamRead.model_validate(new_team)),
    )


@teams_router.get(
    "/team/{team_id}",
    tags=["teams"],
    description="Get team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team found",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def get_team(
    team_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.get(
    "/teams",
    tags=["teams"],
    description="Get teams.",
    responses={
        status.HTTP_200_OK: {
            "model": list[TeamRead],
            "description": "Successful response: teams found",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Teams not found",
            "title": "Teams not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Teams not found"},
                },
            },
        },
    },
)
def get_teams(
    chapter_id: UUID | None = None,
    sport_id: UUID | None = None,
    sort_by_group: bool = False,
    db: Session = db_session,
) -> JSONResponse:
    """Get all teams."""
    if sort_by_group:
        max_group: Row | None = (
            db.query(Team.group)
            .filter(Team.group.is_not(None))
            .filter(Team.is_deleted.is_(False))
            .order_by(Team.group.desc())
            .first()
        )
        if max_group is None:
            if chapter_id:
                teams = (
                    db.query(Team)
                    .filter(Team.chapter_id == chapter_id)
                    .filter(Team.is_deleted.is_(False))
                    .order_by(Team.name)
                    .all()
                )
            elif sport_id:
                teams = (
                    db.query(Team)
                    .filter(Team.sport_id == sport_id)
                    .filter(Team.is_deleted.is_(False))
                    .order_by(Team.name)
                    .all()
                )
            else:
                teams = (
                    db.query(Team)
                    .filter(Team.is_deleted.is_(False))
                    .order_by(Team.name)
                    .all()
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[
                    [object_to_dict(TeamRead.model_validate(team)) for team in teams],
                ],
            )
        else:
            teams: list[list[Team]] = []
            if chapter_id:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.chapter_id == chapter_id)
                    .filter(Team.is_deleted.is_(False))
                    .filter(Team.group.is_(None))
                    .order_by(Team.name)
                    .all()
                )
            elif sport_id:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.sport_id == sport_id)
                    .filter(Team.is_deleted.is_(False))
                    .filter(Team.group.is_(None))
                    .order_by(Team.name)
                    .all()
                )
            else:
                query_teams: list[Team] | None = (
                    db.query(Team)
                    .filter(Team.group.is_(None))
                    .filter(Team.is_deleted.is_(False))
                    .order_by(Team.name)
                    .all()
                )

            if query_teams:
                teams.append(query_teams)

            for group in range(0, max_group[0] + 1):
                if chapter_id:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.chapter_id == chapter_id)
                        .filter(Team.is_deleted.is_(False))
                        .filter(Team.group == group)
                        .order_by(Team.name)
                        .all()
                    )
                elif sport_id:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.sport_id == sport_id)
                        .filter(Team.is_deleted.is_(False))
                        .filter(Team.group == group)
                        .order_by(Team.name)
                        .all()
                    )
                else:
                    query_teams: list[Team] | None = (
                        db.query(Team)
                        .filter(Team.group == group)
                        .filter(Team.is_deleted.is_(False))
                        .order_by(Team.name)
                        .all()
                    )

                if query_teams:
                    teams.append(query_teams)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[
                    [
                        object_to_dict(TeamRead.model_validate(team))
                        for team in group_team
                    ]
                    for group_team in teams
                ],
            )
    else:
        if chapter_id:
            teams = (
                db.query(Team)
                .filter(Team.chapter_id == chapter_id)
                .filter(Team.is_deleted.is_(False))
                .order_by(Team.name)
                .all()
            )
        elif sport_id:
            teams = (
                db.query(Team)
                .filter(Team.sport_id == sport_id)
                .filter(Team.is_deleted.is_(False))
                .order_by(Team.name)
                .all()
            )
        else:
            teams = (
                db.query(Team)
                .filter(Team.is_deleted.is_(False))
                .order_by(Team.name)
                .all()
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[object_to_dict(TeamRead.model_validate(team)) for team in teams],
        )


@teams_router.put(
    "/team/{team_id}",
    tags=["teams"],
    description="Update team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team updated",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def update_team(
    team_id: UUID,
    team_details: TeamUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)
    """Update a team."""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    for field, value in team_details:
        setattr(team, field, value)
    db.add(team)
    db.commit()
    db.refresh(team)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.delete(
    "/team/{team_id}",
    tags=["teams"],
    description="Delete team.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: team deleted",
            "title": "Team deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def delete_team(
    team_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a team."""
    check_admin(current_user)
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    team.is_deleted = True
    db.add(team)
    db.commit()

    team_players = (
        db.query(Player)
        .filter(
            or_(Player.morning_team_id == team_id, Player.afternoon_team_id == team_id),
        )
        .filter(Player.is_deleted.is_(False))
        .all()
    )

    for player in team_players:
        player.is_deleted = True
        db.add(player)
        db.commit()

    matches = (
        db.query(Match)
        .filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
        .filter(Match.is_deleted.is_(False))
        .all()
    )

    for match in matches:
        match.is_deleted = True
        db.add(match)
        db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


@teams_router.put(
    "/team/{team_id}/group",
    tags=["teams"],
    description="Update team.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team updated",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def update_group(
    team_id: UUID,
    group: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)
    """Update a team's group."""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    played_matches: list[Match] = (
        db.query(Match)
        .filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
        .filter(Match.is_deleted.is_(False))
        .filter(
            or_(
                Match.home_score.isnot(None),
                Match.away_score.isnot(None),
            ),
        )
    ).all()

    if played_matches:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change group of team that has played matches",
        )

    unplayed_matches: list[Match] = (
        db.query(Match)
        .filter(or_(Match.home_team_id == team_id, Match.away_team_id == team_id))
        .filter(Match.is_deleted.is_(False))
    ).all()

    for match in unplayed_matches:
        match.is_deleted = True
        db.add(match)

    team.group = group
    db.add(team)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(team)),
    )


@teams_router.put(
    "/team/{team_id}/change_chapter/{chapter_id}",
    tags=["teams"],
    description="Change team's chapter.",
    responses={
        status.HTTP_200_OK: {
            "model": TeamRead,
            "description": "Successful response: team updated",
            "title": "Team details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Team not found",
            "title": "Team not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Team not found"},
                },
            },
        },
    },
)
def change_chapter(
    team_id: UUID,
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    check_admin(current_user)
    """Change a team's chapter."""
    check_admin(current_user)

    old_team = db.get(Team, team_id)

    if not old_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if old_team.chapter_id == chapter_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team already in chapter",
        )

    old_chapter = db.get(Chapter, old_team.chapter_id)

    sport = db.get(Sport, old_team.sport_id)

    old_chapter_teams = (
        db.query(Team)
        .filter(Team.chapter_id == old_chapter.id)
        .filter(Team.is_deleted.is_(False))
        .filter(Team.id != old_team.id)
        .filter(Team.sport_id == old_team.sport_id)
        .all()
    )

    if old_team.name[-1] in ["A", "B", "C", "D"]:
        if len(old_chapter_teams) == 1:
            old_chapter_teams[0].name = old_chapter.name
            old_chapter_teams[0].internal_name = sport.name
            db.add(old_chapter_teams[0])
            db.commit()
        else:
            old_chapter_teams.sort(key=lambda x: x.name[-1])
            for index, team in enumerate(old_chapter_teams):
                if index == 0:
                    team.name = f"{old_chapter.name} A"
                    team.internal_name = f"{sport.name} A"
                elif index == 1:
                    team.name = f"{old_chapter.name} B"
                    team.internal_name = f"{sport.name} B"
                elif index == 2:
                    team.name = f"{old_chapter.name} C"
                    team.internal_name = f"{sport.name} C"
                elif index == 3:
                    team.name = f"{old_chapter.name} D"
                    team.internal_name = f"{sport.name} D"
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Too many teams",
                    )
                db.add(index)
                db.commit()

    existing_sport_teams: list[Team] | None = (
        db.query(Team)
        .filter(Team.sport_id == old_team.sport_id)
        .filter(Team.chapter_id == chapter_id)
        .filter(Team.is_deleted.is_(False))
        .all()
    )

    chapter = db.get(Chapter, chapter_id)

    old_team.chapter_id = chapter_id
    old_team.name = chapter.name
    old_team.internal_name = sport.name

    if existing_sport_teams:
        for team in existing_sport_teams:
            if team.name == chapter.name:
                team.name = f"{team.name} A"
                old_team.name = f"{old_team.name} B"
            elif team.name == f"{chapter.name} A":
                old_team.name = f"{old_team.name} C"
            elif team.name == f"{chapter.name} B":
                old_team.name = f"{old_team.name} D"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Too many teams",
                )
            db.add(team)

    db.add(old_team)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(TeamRead.model_validate(old_team)),
    )


@teams_router.get("/team/{team_id}/valid")
def check_team_valid(team_id: UUID, db: Session = db_session):
    """Check a team's valid"""
    team: Team | None = db.get(Team, team_id)

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    team_sport: Sport | None = db.get(Sport, team.sport_id)

    if team_sport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found"
        )

    if team_sport.morning_sport is True:
        afternoon_players: list[Player] = (
            db.query(Player)
            .filter(Player.afternoon_team_id == team.id)
            .filter(Player.is_deleted.is_(False))
            .all()
        )

        if afternoon_players:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some players have this sport listed as a afternoon sport but this is a morning sport",
            )
        else:
            morning_players: list[Player] = (
                db.query(Player)
                .filter(Player.morning_team_id == team.id)
                .filter(Player.is_deleted.is_(False))
                .all()
            )

            if len(morning_players) != team_sport.number_of_players:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect number of players",
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_204_NO_CONTENT, content=None
                )
    else:
        morning_players: list[Player] = (
            db.query(Player)
            .filter(Player.morning_team_id == team.id)
            .filter(Player.is_deleted.is_(False))
            .all()
        )

        if morning_players:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some players have this sport listed as their morning sport however it's an afternoon sport",
            )
        else:
            afternoon_players: list[Player] = (
                db.query(Player)
                .filter(Player.afternoon_team_id == team.id)
                .filter(Player.is_deleted.is_(False))
                .all()
            )

            if len(afternoon_players) != team_sport.number_of_players:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect number of players",
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_204_NO_CONTENT, content=None
                )
