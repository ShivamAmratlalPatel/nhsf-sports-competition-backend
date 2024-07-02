from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import HTTPException
from starlette import status

from backend.matches.matches_models import Match
from backend.pitches.pitches_models import Pitch
from backend.stages.stages_schemas import StagesEnum
from backend.teams.teams_models import Team
from backend.utils import generate_uuid

if TYPE_CHECKING:
    from backend.sports.sports_models import Sport


def two_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number of teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]

    sport: Sport = team_1.sport
    match_1 = make_match(team_1.id, team_2.id, sport.id, sport.start_time, pitch.id)

    return [match_1]


def three_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number on teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]

    sport: Sport = team_1.sport

    match_1 = make_match(team_1.id, team_2.id, sport.id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_3.id,
        team_2.id,
        sport.id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_1.id,
        team_3.id,
        sport.id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

    return [match_1, match_2, match_3]


def four_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number on teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]

    sport_id: UUID = team_1.sport_id
    sport: Sport = team_1.sport

    match_1 = make_match(team_1.id, team_2.id, sport_id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_3.id,
        team_4.id,
        sport_id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_1.id,
        team_3.id,
        sport_id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_4 = make_match(
        team_2.id,
        team_4.id,
        sport_id,
        sport.start_time + 3 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_5 = make_match(
        team_3.id,
        team_2.id,
        sport_id,
        sport.start_time + 4 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_6 = make_match(
        team_1.id,
        team_4.id,
        sport_id,
        sport.start_time + 5 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

    return [match_1, match_2, match_3, match_4, match_5, match_6]


def five_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number of teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]

    sport_id: UUID = team_1.sport_id
    sport = team_1.sport

    match_1 = make_match(team_1.id, team_4.id, sport_id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_2.id,
        team_5.id,
        sport_id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_3.id,
        team_1.id,
        sport_id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_4 = make_match(
        team_5.id,
        team_4.id,
        sport_id,
        sport.start_time + 3 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_5 = make_match(
        team_3.id,
        team_2.id,
        sport_id,
        sport.start_time + 4 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_6 = make_match(
        team_5.id,
        team_1.id,
        sport_id,
        sport.start_time + 5 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_7 = make_match(
        team_2.id,
        team_4.id,
        sport_id,
        sport.start_time + 6 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_8 = make_match(
        team_3.id,
        team_5.id,
        sport_id,
        sport.start_time + 7 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_9 = make_match(
        team_1.id,
        team_2.id,
        sport_id,
        sport.start_time + 8 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_10 = make_match(
        team_4.id,
        team_3.id,
        sport_id,
        sport.start_time + 9 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

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


def six_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number of teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]
    team_6 = teams[5]

    sport: Sport = team_1.sport

    match_1 = make_match(team_6.id, team_3.id, sport.id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_1.id,
        team_4.id,
        sport.id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_5.id,
        team_2.id,
        sport.id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_4 = make_match(
        team_4.id,
        team_6.id,
        sport.id,
        sport.start_time + 3 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_5 = make_match(
        team_2.id,
        team_3.id,
        sport.id,
        sport.start_time + 4 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_6 = make_match(
        team_5.id,
        team_1.id,
        sport.id,
        sport.start_time + 5 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_7 = make_match(
        team_6.id,
        team_2.id,
        sport.id,
        sport.start_time + 6 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_8 = make_match(
        team_4.id,
        team_5.id,
        sport.id,
        sport.start_time + 7 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_9 = make_match(
        team_3.id,
        team_1.id,
        sport.id,
        sport.start_time + 8 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_10 = make_match(
        team_5.id,
        team_6.id,
        sport.id,
        sport.start_time + 9 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_11 = make_match(
        team_1.id,
        team_2.id,
        sport.id,
        sport.start_time + 10 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_12 = make_match(
        team_3.id,
        team_4.id,
        sport.id,
        sport.start_time + 11 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_13 = make_match(
        team_6.id,
        team_1.id,
        sport.id,
        sport.start_time + 12 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_14 = make_match(
        team_5.id,
        team_3.id,
        sport.id,
        sport.start_time + 13 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_15 = make_match(
        team_2.id,
        team_4.id,
        sport.id,
        sport.start_time + 14 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

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


def seven_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number of teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]
    team_6 = teams[5]
    team_7 = teams[6]

    sport = team_1.sport

    match_1 = make_match(team_5.id, team_2.id, sport.id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_4.id,
        team_7.id,
        sport.id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_1.id,
        team_6.id,
        sport.id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_4 = make_match(
        team_3.id,
        team_4.id,
        sport.id,
        sport.start_time + 3 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_5 = make_match(
        team_6.id,
        team_5.id,
        sport.id,
        sport.start_time + 4 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_6 = make_match(
        team_7.id,
        team_1.id,
        sport.id,
        sport.start_time + 5 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_7 = make_match(
        team_2.id,
        team_6.id,
        sport.id,
        sport.start_time + 6 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_8 = make_match(
        team_1.id,
        team_3.id,
        sport.id,
        sport.start_time + 7 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_9 = make_match(
        team_5.id,
        team_7.id,
        sport.id,
        sport.start_time + 8 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_10 = make_match(
        team_1.id,
        team_4.id,
        sport.id,
        sport.start_time + 9 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_11 = make_match(
        team_2.id,
        team_7.id,
        sport.id,
        sport.start_time + 10 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_12 = make_match(
        team_5.id,
        team_3.id,
        sport.id,
        sport.start_time + 11 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_13 = make_match(
        team_7.id,
        team_6.id,
        sport.id,
        sport.start_time + 12 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_14 = make_match(
        team_4.id,
        team_5.id,
        sport.id,
        sport.start_time + 13 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_15 = make_match(
        team_3.id,
        team_2.id,
        sport.id,
        sport.start_time + 14 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_16 = make_match(
        team_5.id,
        team_1.id,
        sport.id,
        sport.start_time + 15 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_17 = make_match(
        team_6.id,
        team_3.id,
        sport.id,
        sport.start_time + 16 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_18 = make_match(
        team_2.id,
        team_4.id,
        sport.id,
        sport.start_time + 17 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_19 = make_match(
        team_3.id,
        team_7.id,
        sport.id,
        sport.start_time + 18 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_20 = make_match(
        team_1.id,
        team_2.id,
        sport.id,
        sport.start_time + 19 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_21 = make_match(
        team_4.id,
        team_6.id,
        sport.id,
        sport.start_time + 20 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

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
        match_16,
        match_17,
        match_18,
        match_19,
        match_20,
        match_21,
    ]


def eight_in_a_group_schedule(teams: list[Team], pitch: Pitch) -> list[Match]:
    if len(teams) != 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong number of teams",
        )

    team_1 = teams[0]
    team_2 = teams[1]
    team_3 = teams[2]
    team_4 = teams[3]
    team_5 = teams[4]
    team_6 = teams[5]
    team_7 = teams[6]
    team_8 = teams[7]

    sport = team_1.sport

    # 1 vs. 8
    # 2 vs. 7
    # 3 vs. 6
    # 4 vs. 5
    # 1 vs. 7
    # 8 vs. 6
    # 2 vs. 5
    # 3 vs. 4
    # 1 vs. 6
    # 7 vs. 5
    # 8 vs. 4
    # 2 vs. 3
    # 1 vs. 5
    # 6 vs. 4
    # 7 vs. 3
    # 8 vs. 2
    # 1 vs. 4
    # 5 vs. 3
    # 6 vs. 2
    # 7 vs. 8
    # 1 vs. 3
    # 4 vs. 2
    # 5 vs. 8
    # 6 vs. 7
    # 1 vs. 2
    # 3 vs. 8
    # 4 vs. 7
    # 5 vs. 6

    match_1 = make_match(team_1.id, team_8.id, sport.id, sport.start_time, pitch.id)
    match_2 = make_match(
        team_2.id,
        team_7.id,
        sport.id,
        sport.start_time + timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_3 = make_match(
        team_3.id,
        team_6.id,
        sport.id,
        sport.start_time + 2 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_4 = make_match(
        team_4.id,
        team_5.id,
        sport.id,
        sport.start_time + 3 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_5 = make_match(
        team_1.id,
        team_7.id,
        sport.id,
        sport.start_time + 4 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_6 = make_match(
        team_8.id,
        team_6.id,
        sport.id,
        sport.start_time + 5 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_7 = make_match(
        team_2.id,
        team_5.id,
        sport.id,
        sport.start_time + 6 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_8 = make_match(
        team_3.id,
        team_4.id,
        sport.id,
        sport.start_time + 7 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_9 = make_match(
        team_1.id,
        team_6.id,
        sport.id,
        sport.start_time + 8 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_10 = make_match(
        team_7.id,
        team_5.id,
        sport.id,
        sport.start_time + 9 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_11 = make_match(
        team_8.id,
        team_4.id,
        sport.id,
        sport.start_time + 10 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_12 = make_match(
        team_2.id,
        team_3.id,
        sport.id,
        sport.start_time + 11 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_13 = make_match(
        team_1.id,
        team_5.id,
        sport.id,
        sport.start_time + 12 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_14 = make_match(
        team_6.id,
        team_4.id,
        sport.id,
        sport.start_time + 13 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_15 = make_match(
        team_7.id,
        team_3.id,
        sport.id,
        sport.start_time + 14 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_16 = make_match(
        team_8.id,
        team_2.id,
        sport.id,
        sport.start_time + 15 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_17 = make_match(
        team_1.id,
        team_4.id,
        sport.id,
        sport.start_time + 16 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_18 = make_match(
        team_5.id,
        team_3.id,
        sport.id,
        sport.start_time + 17 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_19 = make_match(
        team_6.id,
        team_2.id,
        sport.id,
        sport.start_time + 18 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_20 = make_match(
        team_7.id,
        team_8.id,
        sport.id,
        sport.start_time + 19 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_21 = make_match(
        team_1.id,
        team_3.id,
        sport.id,
        sport.start_time + 20 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_22 = make_match(
        team_4.id,
        team_2.id,
        sport.id,
        sport.start_time + 21 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_23 = make_match(
        team_5.id,
        team_8.id,
        sport.id,
        sport.start_time + 22 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_24 = make_match(
        team_6.id,
        team_7.id,
        sport.id,
        sport.start_time + 23 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_25 = make_match(
        team_1.id,
        team_2.id,
        sport.id,
        sport.start_time + 24 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_26 = make_match(
        team_3.id,
        team_8.id,
        sport.id,
        sport.start_time + 25 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_27 = make_match(
        team_4.id,
        team_7.id,
        sport.id,
        sport.start_time + 26 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )
    match_28 = make_match(
        team_5.id,
        team_6.id,
        sport.id,
        sport.start_time + 27 * timedelta(minutes=sport.minutes_per_game),
        pitch.id,
    )

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
        match_16,
        match_17,
        match_18,
        match_19,
        match_20,
        match_21,
        match_22,
        match_23,
        match_24,
        match_25,
        match_26,
        match_27,
        match_28,
    ]


def make_match(
    home_team_id: UUID,
    away_team_id: UUID,
    sport_id: UUID,
    time: datetime | None = None,
    pitch_id: UUID | None = None,
) -> Match:
    return Match(
        id=generate_uuid(),
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        sport_id=sport_id,
        stage_id=StagesEnum.group_stage.value,
        time=time,
        pitch_id=pitch_id,
    )
