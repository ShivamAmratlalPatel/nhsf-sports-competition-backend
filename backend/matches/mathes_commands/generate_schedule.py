"""Generate a schedule for a sport."""
from random import shuffle
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.matches.matches_models import Match
from backend.matches.mathes_commands.x_in_a_group import (
    five_in_a_group_schedule,
    four_in_a_group_schedule,
    seven_in_a_group_schedule,
    six_in_a_group_schedule,
    three_in_a_group_schedule,
    two_in_a_group_schedule,
)
from backend.pitches.pitches_models import Pitch
from backend.teams.teams_models import Team


def generate_schedule_for_group(
    db: Session,
    number_of_groups: int,
    sport_id: UUID,
) -> None:
    """Generate a schedule for a group."""
    pitches: list[Match] = (
        db.query(Pitch)
        .filter(Pitch.sport_id == sport_id)
        .filter(Pitch.is_deleted.is_(False))
        .all()
    )

    number_of_pitches = len(pitches)

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
            matches = two_in_a_group_schedule(
                group_teams,
                pitches[group % number_of_pitches],
            )
        except HTTPException:
            try:
                matches = three_in_a_group_schedule(
                    group_teams,
                    pitches[group % number_of_pitches],
                )
            except HTTPException:
                try:
                    matches = four_in_a_group_schedule(
                        group_teams,
                        pitches[group % number_of_pitches],
                    )
                except HTTPException:
                    try:
                        matches = five_in_a_group_schedule(
                            group_teams,
                            pitches[group % number_of_pitches],
                        )
                    except HTTPException:
                        try:
                            matches = six_in_a_group_schedule(
                                group_teams,
                                pitches[group % number_of_pitches],
                            )
                        except HTTPException:
                            try:
                                matches = seven_in_a_group_schedule(
                                    group_teams,
                                    pitches[group % number_of_pitches],
                                )
                            except HTTPException:
                                raise HTTPException(
                                    status_code=400,
                                    detail="Cannot generate schedule for group",
                                )
        # endregion
        for match in matches:
            db.add(match)
        db.commit()
    # endregion


def randomly_assign_groups(
    db: Session,
    number_of_groups: int,
    teams: list[Team],
) -> None:
    """Randomly assign teams to groups."""
    # region randomly assign groups
    shuffle(teams)
    assign_groups(db, number_of_groups, teams)
    # endregion


def assign_groups(db, number_of_groups, teams):
    for position, team in enumerate(teams):
        team.group = position % number_of_groups
        db.add(team)
    db.commit()


def check_groups_not_already_assigned(teams):
    # region check groups are not already assigned
    assigned: bool = teams[0].group is not None
    for team in teams:
        if team.group is not None != assigned:
            raise HTTPException(
                status_code=400,
                detail="Some teams are already assigned to groups. Either assign all teams to groups or none.",
            )
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


def order_assign_groups(db: Session, number_of_groups: int, teams: list[Team]) -> None:
    teams.sort(
        key=lambda x: (
            x.stage_reached,
            x.average_point_per_game_in_group_stage,
            x.regional_competition_id,
            x.id,
        ),
        reverse=True,
    )

    assign_groups(db, number_of_groups, teams)
