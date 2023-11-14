"""Generate a schedule for a sport."""
from random import shuffle, randint
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.matches.matches_models import Match
from backend.pitches.pitches_models import Pitch
from backend.teams.teams_models import Team
from backend.utils import generate_uuid, random_datetime


def generate_schedule_for_group(db: Session, number_of_groups: int, sport_id: UUID) -> None:
    """Generate a schedule for a group."""
    # region generate schedule for each group
    pitches: list[Pitch] = db.query(Pitch).filter(Pitch.sport_id == sport_id).all()
    number_of_pitches = len(pitches)
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
        for i, home_team in enumerate(group_teams[:-1]):
            if i >= number_of_pitches:
                pitch_no = randint(0, number_of_pitches - 1) # noqa: S311
            else:
                pitch_no = i
            for away_team in group_teams[i + 1 :]:
                if home_team.id != away_team.id:
                    match = Match(
                        id=generate_uuid(),
                        sport_id=sport_id,
                        stage_id=0,
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        time=random_datetime(),
                        pitch_id=pitches[pitch_no].id,
                    )
                    db.add(match)
        # endregion
        db.commit()
    # endregion


def randomly_assign_groups(db: Session, number_of_groups: int, teams: list[Team]) -> None:
    """Randomly assign teams to groups."""
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
