"""
Module: test_pitch_routes

This module contains unit tests for the FastAPI routes related to pitch creation and handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.helpers import get_db
from backend.main import app
from backend.sports.sports_models import Sport
from backend.utils import generate_uuid, object_to_dict

from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_pitch, fake_name, fake_sport
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


class TestPostPitch:
    """
    Test Class: TestPostPitch

    This class contains unit tests for the POST /pitch route.
    """

    def test_post_pitch(
        self: "TestPostPitch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_post_pitch

        Test the POST /pitch route for successful pitch creation.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

    def test_duplicate_pitch(
        self: "TestPostPitch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_duplicate_pitch

        Test the scenario where a pitch with the same data already exists.

        Args:
            client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Pitch already exists"


class TestGetPitch:
    """
    Test Class: TestGetPitch

    This class contains unit tests for the GET /pitch/{pitch_id} route.
    """

    def test_get_pitch(
        self: "TestGetPitch",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_get_pitch

        Test the GET /pitch/{pitch_id} route for successful pitch retrieval.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.


        Returns:
           None
        """
        sport = Sport(**fake_sport())
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.get(f"/pitch/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]

    def test_get_pitch_not_found(
        self: "TestGetPitch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_pitch_not_found

        Test the GET /pitch/{pitch_id} route for a pitch that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/pitch/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pitch not found"


class TestGetPitchList:
    """
    Test Class: TestGetPitchList

    This class contains unit tests for the GET /pitches route.
    """

    def test_get_pitch_list(
        self: "TestGetPitchList",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_get_pitch_list

        Test the GET /pitches route for successful pitch retrieval.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.


        Returns:
           None
        """
        sport = Sport(**fake_sport())
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.get("/pitches")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == data["name"]

    def test_get_pitch_list_empty(
        self: "TestGetPitchList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_pitch_list_empty

        Test the GET /pitches route for a pitch that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get("/pitches")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pitches not found"


class TestPutPitch:
    """
    Test Class: TestPutPitch

    This class contains unit tests for the PUT /pitch/{pitch_id} route.
    """

    def test_put_pitch(
        self: "TestPutPitch",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_put_pitch

        Test the PUT /pitch/{pitch_id} route for successful pitch update.

        Args:
           client (TestClient): A FastAPI test client.
           session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        sport = Sport(**fake_sport())
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        sport = Sport(**fake_sport())
        sport.id = generate_uuid()
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data["name"] = fake_name()
        data["sport_id"] = sport.id

        response = client.put(
            f"/pitch/{response.json()['id']}",
            json=object_to_dict(data),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]

    def test_put_pitch_not_found(
        self: "TestPutPitch",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_put_pitch_not_found

        Test the PUT /pitch/{pitch_id} route for a pitch that does not exist.

        Args:
            client (TestClient): A FastAPI test client.
            session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        sport = Sport(**fake_sport())
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data = fake_pitch()

        response = client.put(f"/pitch/{generate_uuid()}", json=object_to_dict(data))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pitch not found"


class TestDeletePitch:
    """
    Test Class: TestDeletePitch

    This class contains unit tests for the DELETE /pitch/{pitch_id} route.
    """

    def test_delete_pitch(
        self: "TestDeletePitch",
        client: TestClient,
        session: Session,
    ) -> None:
        """
        Test Method: test_delete_pitch

        Test the DELETE /pitch/{pitch_id} route for successful pitch deletion.

        Args:
            client (TestClient): A FastAPI test client.
            session (Session): A SQLAlchemy database session.

        Returns:
           None
        """
        sport = Sport(**fake_sport())
        session.add(sport)
        session.commit()
        session.refresh(sport)

        data = fake_pitch()

        response = client.post("/pitch", json=object_to_dict(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]

        response = client.delete(f"/pitch/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.json() == {}

    def test_delete_pitch_not_found(
        self: "TestDeletePitch",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_pitch_not_found

        Test the DELETE /pitch/{pitch_id} route for a pitch that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.delete(f"/pitch/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Pitch not found"
