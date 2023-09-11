"""
Module: test_team_routes

This module contains unit tests for the FastAPI routes related to team creation and handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.main import app
from backend.sports.sports_models import Sport
from backend.utils import generate_uuid, object_to_dict

from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import (
    fake_team,
    fake_name,
    fake_chapter,
    fake_sport,
)
from starlette import status


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


class TestPostTeam:
    """
    Test Class: TestPostTeam

    This class contains unit tests for the POST /team route.
    """

    def test_post_team(
        self: "TestPostTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_post_team

        Test the POST /team route for successful team creation.

        Args:
            client (TestClient): A FastAPI test client.
            session (Session): A SQLAlchemy database session.


        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

    def test_duplicate_team(
        self: "TestPostTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_duplicate_team

        Test the scenario where a team with the same data already exists.

        Args:
            client (TestClient): A FastAPI test client.
            session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Team already exists"


class TestGetTeam:
    """
    Test Class: TestGetTeam

    This class contains unit tests for the GET /team/{team_id} route.
    """

    def test_get_team(
        self: "TestGetTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_get_team

        Test the GET /team/{team_id} route for successful team retrieval.

        Args:
            client (TestClient): A FastAPI test client.
            session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

        response = client.get(f"/team/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

    def test_get_team_not_found(
        self: "TestGetTeam",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_team_not_found

        Test the GET /team/{team_id} route for a team that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/team/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Team not found"


class TestGetTeamList:
    """
    Test Class: TestGetTeamList

    This class contains unit tests for the GET /teams route.
    """

    def test_get_team_list(
        self: "TestGetTeamList",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_get_team_list

        Test the GET /teams route for successful team retrieval.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

        response = client.get("/teams")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == data["name"]

    def test_get_team_list_empty(
        self: "TestGetTeamList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_team_list_empty

        Test the GET /teams route for a team that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get("/teams")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Teams not found"


class TestPutTeam:
    """
    Test Class: TestPutTeam

    This class contains unit tests for the PUT /team/{team_id} route.
    """

    def test_put_team(
        self: "TestPutTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_put_team

        Test the PUT /team/{team_id} route for successful team update.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

        data["name"] = fake_name()

        response = client.put(
            f"/team/{response.json()['id']}",
            json=object_to_dict(data),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

    def test_put_team_not_found(
        self: "TestPutTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_put_team_not_found

        Test the PUT /team/{team_id} route for a team that does not exist.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.put(f"/team/{generate_uuid()}", json=object_to_dict(data))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Team not found"


class TestDeleteTeam:
    """
    Test Class: TestDeleteTeam

    This class contains unit tests for the DELETE /team/{team_id} route.
    """

    def test_delete_team(
        self: "TestDeleteTeam",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_delete_team

        Test the DELETE /team/{team_id} route for successful team deletion.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        chapter = Chapter(**fake_chapter())
        sport = Sport(**fake_sport())
        session.add(chapter)
        session.add(sport)
        session.commit()

        session.refresh(chapter)
        session.refresh(sport)

        data = fake_team(chapter_id=chapter.id, sport_id=sport.id)

        response = client.post("/team", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["chapter_id"] == str(data["chapter_id"])
        assert response.json()["sport_id"] == str(data["sport_id"])

        response = client.delete(f"/team/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.json() == {}

    def test_delete_team_not_found(
        self: "TestDeleteTeam",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_team_not_found

        Test the DELETE /team/{team_id} route for a team that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.delete(f"/team/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Team not found"
