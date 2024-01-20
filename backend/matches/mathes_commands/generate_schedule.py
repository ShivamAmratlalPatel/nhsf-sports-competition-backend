"""Generate a schedule for a sport."""
from random import shuffle, randint
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.matches.matches_models import Match
from backend.pitches.pitches_models import Pitch
from backend.stages.stages_schemas import StagesEnum
from backend.teams.teams_models import Team
from backend.utils import generate_uuid, random_datetime


def generate_schedule_for_group(
    db: Session, number_of_groups: int, sport_id: UUID
) -> None:
    """Generate a schedule for a group."""
    # region generate schedule for each group
    for group in range(number_of_groups):
        # region get teams in group
        group_teams: list[Team] = (
            db.query(Team)
            .filter(Team.sport_id == sport_id)
            .filter(Team.is_deleted.is_(False))
            .filter(Team.group == group)
            .all()
        )
        # endregion

        # region check there are teams in group

        if not group_teams:
            # continue to next iteration of loop
            continue

        # endregion

        # region generate schedule for group
        try:
            matches = two_in_a_group_schedule(group_teams)
        except HTTPException:
            try:
                matches = three_in_a_group_schedule(group_teams)
            except HTTPException:
                try:
                    matches = four_in_a_group_schedule(group_teams)
                except HTTPException:
                    try:
                        matches = five_in_a_group_schedule(group_teams)
                    except HTTPException:
                        try:
                            matches = six_in_a_group_schedule(group_teams)
                        except HTTPException:
                            raise HTTPException(
                                status_code=400, detail="More than 6 in the group"
                            )
        # endregion
        for match in matches:
            db.add(match)
        db.commit()
    # endregion


def randomly_assign_groups(
    db: Session, number_of_groups: int, teams: list[Team]
) -> None:
    """Randomly assign teams to groups."""
    # region check groups are not already assigned
    assigned: bool = teams[0].group is not None
    for team in teams:
        if team.group is not None != assigned:
            raise HTTPException(
                status_code=400,
                detail="Some teams are already assigned to groups. Either assign all teams to groups or none.",
            )
    # endregion
    # region randomly assign groups
    shuffle(teams)
    for position, team in enumerate(teams):
        team.group = position % number_of_groups
        db.add(team)
    db.commit()
    # endregion


def check_teams(teams: list[Team]) -> None:
    """Check that there are teams for a sport."""
    # region check there are teams
    if not teams:
        raise HTTPException(
            status_code=400,
            detail="There are no teams for this sport",
        )
    # endregion


def get_list_of_teams_for_sport(db: Session, sport_id: UUID) -> list[Team]:
    """Get a list of teams for a sport."""
    # region get list of teams for sport
    teams: list[Team] = (
        db.query(Team)
        .filter(Team.sport_id == sport_id)
        .filter(Team.is_deleted.is_(False))
        .all()
    )
    # endregion
    return teams


def check_matches_have_not_been_generated(db: Session, sport_id: UUID) -> None:
    """Check that matches have not already been generated."""
    # region check matches have not already been generated
    existing_matches = (
        db.query(Match)
        .filter(Match.sport_id == sport_id)
        .filter(Match.is_deleted.is_(False))
        .all()
    )
    if existing_matches:
        raise HTTPException(
            status_code=400,
            detail="Matches have already been generated",
        )
    # endregion


def make_match(home_team_id: UUID, away_team_id: UUID, sport_id: UUID) -> Match:
    return Match(
        id=generate_uuid(),
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        sport_id=sport_id,
        stage_id=StagesEnum.group_stage.value,
    )


def two_in_a_group_schedule(teams: list[Team]) -> list[Match]:
    if len(teams) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong number of teams"
        )

    team_1 = teams[0]
    team_2 = teams[1]

    sport_id: UUID = team_1.id
    match_1 = make_match(team_1.id, team_2.id, sport_id)

    return [match_1]


def three_in_a_group_schedule(teams: list[Team]) -> list[Match]:
    if len(teams) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong number on teams"
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]

    sport_id: UUID = team_1.id

    match_1 = make_match(team_1.id, team_2.id, sport_id)
    match_2 = make_match(team_3.id, team_2.id, sport_id)
    match_3 = make_match(team_1.id, team_3.id, sport_id)

    return [match_1, match_2, match_3]


def four_in_a_group_schedule(teams: list[Team]) -> list[Match]:
    if len(teams) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong number on teams"
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]

    sport_id: UUID = team_1.sport_id

    match_1 = make_match(team_1.id, team_2.id, sport_id)
    match_2 = make_match(team_3.id, team_4.id, sport_id)
    match_3 = make_match(team_1.id, team_3.id, sport_id)
    match_4 = make_match(team_2.id, team_4.id, sport_id)
    match_5 = make_match(team_3.id, team_2.id, sport_id)
    match_6 = make_match(team_1.id, team_4.id, sport_id)

    return [match_1, match_2, match_3, match_4, match_5, match_6]


def five_in_a_group_schedule(teams: list[Team]) -> list[Match]:
    if len(teams) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong number of teams"
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]

    sport_id: UUID = team_1.sport_id

    match_1 = make_match(team_1.id, team_4.id, sport_id)
    match_2 = make_match(team_2.id, team_5.id, sport_id)
    match_3 = make_match(team_3.id, team_1.id, sport_id)
    match_4 = make_match(team_5.id, team_4.id, sport_id)
    match_5 = make_match(team_3.id, team_2.id, sport_id)
    match_6 = make_match(team_5.id, team_1.id, sport_id)
    match_7 = make_match(team_2.id, team_4.id, sport_id)
    match_8 = make_match(team_3.id, team_5.id, sport_id)
    match_9 = make_match(team_1.id, team_2.id, sport_id)
    match_10 = make_match(team_4.id, team_3.id, sport_id)

    return [
        match_1,
        match_2,
        match_3,
        match_4,
        match_5,
        match_6,
        match_7,
        match_8,
        match_9,
        match_10,
    ]


def six_in_a_group_schedule(teams: list[Team]) -> list[Match]:
    if len(teams) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong number of teams"
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]
    team_6 = teams[5]

    sport_id: UUID = team_1.id

    match_1 = make_match(team_6.id, team_3.id, sport_id)
    match_2 = make_match(team_1.id, team_4.id, sport_id)
    match_3 = make_match(team_5.id, team_2.id, sport_id)
    match_4 = make_match(team_4.id, team_6.id, sport_id)
    match_5 = make_match(team_2.id, team_3.id, sport_id)
    match_6 = make_match(team_5.id, team_1.id, sport_id)
    match_7 = make_match(team_6.id, team_2.id, sport_id)
    match_8 = make_match(team_4.id, team_5.id, sport_id)
    match_9 = make_match(team_3.id, team_1.id, sport_id)
    match_10 = make_match(team_5.id, team_6.id, sport_id)
    match_11 = make_match(team_1.id, team_2.id, sport_id)
    match_12 = make_match(team_3.id, team_4.id, sport_id)
    match_13 = make_match(team_6.id, team_1.id, sport_id)
    match_14 = make_match(team_5.id, team_3.id, sport_id)
    match_15 = make_match(team_2.id, team_4.id, sport_id)

    return [
        match_1,
        match_2,
        match_3,
        match_4,
        match_5,
        match_6,
        match_7,
        match_8,
        match_9,
        match_10,
        match_11,
        match_12,
        match_13,
        match_14,
        match_15,
    ]
