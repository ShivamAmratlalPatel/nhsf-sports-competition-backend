"""
Module: test_sport_routes

This module contains unit tests for the FastAPI routes related to sport creation and handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.main import app
from backend.utils import generate_uuid
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_name, fake_sport


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


class TestPostSport:
    """
    Test Class: TestPostSport

    This class contains unit tests for the POST /sport route.
    """

    def test_post_sport(self: "TestPostSport", client: TestClient) -> None:
        """
        Test Method: test_post_sport

        Test the POST /sport route for successful sport creation.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

    def test_duplicate_sport(self: "TestPostSport", client: TestClient) -> None:
        """
        Test Method: test_duplicate_sport

        Test the scenario where a sport with the same data already exists.

        Args:
            client (TestClient): A FastAPI test client.



        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Sport already exists"


class TestGetSport:
    """
    Test Class: TestGetSport

    This class contains unit tests for the GET /sport/{sport_id} route.
    """

    def test_get_sport(
        self: "TestGetSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_sport

        Test the GET /sport/{sport_id} route for successful sport retrieval.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.get(f"/sport/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]

    def test_get_sport_not_found(
        self: "TestGetSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_sport_not_found

        Test the GET /sport/{sport_id} route for a sport that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/sport/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sport not found"


class TestGetSportList:
    """
    Test Class: TestGetSportList

    This class contains unit tests for the GET /sports route.
    """

    def test_get_sport_list(
        self: "TestGetSportList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_sport_list

        Test the GET /sports route for successful sport retrieval.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.get("/sports")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == data["name"]

    def test_get_sport_list_empty(
        self: "TestGetSportList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_sport_list_empty

        Test the GET /sports route for a sport that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get("/sports")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sports not found"


class TestPutSport:
    """
    Test Class: TestPutSport

    This class contains unit tests for the PUT /sport/{sport_id} route.
    """

    def test_put_sport(
        self: "TestPutSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_put_sport

        Test the PUT /sport/{sport_id} route for successful sport update.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        data["name"] = fake_name()

        response = client.put(f"/sport/{response.json()['id']}", json=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]

    def test_put_sport_not_found(
        self: "TestPutSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_put_sport_not_found

        Test the PUT /sport/{sport_id} route for a sport that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.put(f"/sport/{generate_uuid()}", json=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sport not found"


class TestDeleteSport:
    """
    Test Class: TestDeleteSport

    This class contains unit tests for the DELETE /sport/{sport_id} route.
    """

    def test_delete_sport(
        self: "TestDeleteSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_sport

        Test the DELETE /sport/{sport_id} route for successful sport deletion.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_sport()

        response = client.post("/sport", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.delete(f"/sport/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.json() == {}

    def test_delete_sport_not_found(
        self: "TestDeleteSport",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_sport_not_found

        Test the DELETE /sport/{sport_id} route for a sport that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.delete(f"/sport/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Sport not found"
