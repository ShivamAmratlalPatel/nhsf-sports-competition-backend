"""
Module: test_match_routes

This module contains unit tests for the FastAPI routes related to match creation and handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.main import app
from backend.matches.matches_models import Match
from backend.pitches.pitches_models import Pitch
from backend.sports.sports_models import Sport
from backend.stages.stages_schemas import StagesEnum
from backend.teams.teams_models import Team
from backend.utils import generate_uuid, object_to_dict
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import (
    fake_chapter,
    fake_match,
    fake_name,
    fake_pitch,
    fake_sport,
    fake_team,
)


@pytest.fixture()
def client(
    session: Session,
) -> TestClient:
    """
    Fixture Function: client

    Generate a test client with the provided database session.

    Args:
       session (Session): A SQLAlchemy database session.

    Yields:
       TestClient: A FastAPI test client configured to use the provided session.
    """
    app.dependency_overrides[get_db] = lambda: session

    yield TestClient(app)

    app.dependency_overrides = {}


@pytest.fixture()
def match_data(session: Session) -> dict:
    """Return a dictionary of match data."""
    home_chapter = Chapter(**fake_chapter())
    away_chapter = Chapter(**fake_chapter())
    home_chapter.id = generate_uuid()
    away_chapter.id = generate_uuid()
    sport = Sport(**fake_sport())
    sport.id = generate_uuid()
    home_team = Team(**fake_team(chapter_id=home_chapter.id, sport_id=sport.id))
    away_team = Team(**fake_team(chapter_id=away_chapter.id, sport_id=sport.id))
    away_team.id = generate_uuid()
    pitch = Pitch(**fake_pitch())
    pitch.id = generate_uuid()
    session.add(home_chapter)
    session.add(away_chapter)
    session.add(home_team)
    session.add(away_team)
    session.add(sport)
    session.add(pitch)
    session.commit()

    return fake_match(
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        sport_id=sport.id,
        pitch_id=pitch.id,
        stage=StagesEnum.group_stage,
    )


class TestPostMatch:
    """
    Test Class: TestPostMatch

    This class contains unit tests for the POST /match route.
    """

    def test_post_match(
        self: "TestPostMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_post_match

        Test the POST /match route for successful match creation.

        Args:
            client (TestClient): A FastAPI test client.
            match_data (dict): A dictionary of match data.


        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_match(
        self: "TestPostMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_duplicate_match

        Test the scenario where a match with the same data already exists.

        Args:
            client (TestClient): A FastAPI test client.
            match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Match already exists"


class TestGetMatch:
    """
    Test Class: TestGetMatch

    This class contains unit tests for the GET /match/{match_id} route.
    """

    def test_get_match(
        self: "TestGetMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_get_match

        Test the GET /match/{match_id} route for successful match retrieval.

        Args:
            client (TestClient): A FastAPI test client.
            match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get(f"/match/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK

    def test_get_match_not_found(
        self: "TestGetMatch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_match_not_found

        Test the GET /match/{match_id} route for a match that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/match/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Match not found"


class TestGetMatchList:
    """
    Test Class: TestGetMatchList

    This class contains unit tests for the GET /matches route.
    """

    def test_get_match_list(
        self: "TestGetMatchList",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_get_match_list

        Test the GET /matches route for successful match retrieval.

        Args:
           client (TestClient): A FastAPI test client.
           match_data (dict): A dictionary of match data.


        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get("/matches")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_get_match_list_empty(
        self: "TestGetMatchList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_match_list_empty

        Test the GET /matches route for a match that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get("/matches")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Matches not found"


class TestPutMatch:
    """
    Test Class: TestPutMatch

    This class contains unit tests for the PUT /match/{match_id} route.
    """

    def test_put_match(
        self: "TestPutMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_put_match

        Test the PUT /match/{match_id} route for successful match update.

        Args:
           client (TestClient): A FastAPI test client.
           match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        match_data["name"] = fake_name()

        response = client.put(
            f"/match/{response.json()['id']}",
            json=object_to_dict(match_data),
        )
        assert response.status_code == status.HTTP_200_OK

    def test_put_match_not_found(
        self: "TestPutMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_put_match_not_found

        Test the PUT /match/{match_id} route for a match that does not exist.

        Args:
           client (TestClient): A FastAPI test client.
           match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.put(
            f"/match/{generate_uuid()}",
            json=object_to_dict(match_data),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Match not found"


class TestDeleteMatch:
    """
    Test Class: TestDeleteMatch

    This class contains unit tests for the DELETE /match/{match_id} route.
    """

    def test_delete_match(
        self: "TestDeleteMatch",
        client: TestClient,
        match_data: dict,
    ) -> None:
        """
        Test Method: test_delete_match

        Test the DELETE /match/{match_id} route for successful match deletion.

        Args:
           client (TestClient): A FastAPI test client.
           match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        response = client.delete(f"/match/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.json() == {}

    def test_delete_match_not_found(
        self: "TestDeleteMatch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_match_not_found

        Test the DELETE /match/{match_id} route for a match that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.delete(f"/match/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Match not found"


class TestGetSchedule:
    """
    Test Class: TestGetSchedule

    This class contains unit tests for the GET /schedule route.
    """

    def test_get_schedule(
        self: "TestGetSchedule", client: TestClient, match_data: dict, session: Session
    ) -> None:
        """
        Test Method: test_get_schedule

        Test the GET /schedule route for successful match retrieval.

        Args:
           client (TestClient): A FastAPI test client.
           match_data (dict): A dictionary of match data.

        Returns:
           None
        """
        response = client.post("/match", json=object_to_dict(match_data))
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get(f"/schedule/{match_data['sport_id']}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_get_schedule_empty(
        self: "TestGetSchedule",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_schedule_empty

        Test the GET /schedule route for a match that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/schedule/{generate_uuid()}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
