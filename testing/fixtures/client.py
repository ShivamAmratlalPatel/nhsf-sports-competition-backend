"""Test client fixture for FastAPI app."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.helpers import (
    get_db,
    get_s3_client,
    get_sendgrid_client,
    get_twilio_client,
    get_wise_client,
)
from backend.main import app
from testing.fixtures.integrations import (
    s3_client,
    sendgrid_client,
    twilio_client,
    wise_client,
)


# Fixtures with this client are not working. Have to create another client in the test file like in test_payments_routes.py
# TODO: Fix this
@pytest.fixture()
def client(session: Session) -> TestClient:
    """Generate test client."""
    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_sendgrid_client] = lambda: sendgrid_client
    app.dependency_overrides[get_twilio_client] = lambda: twilio_client
    app.dependency_overrides[get_wise_client] = lambda: wise_client
    app.dependency_overrides[get_s3_client] = lambda: s3_client

    yield TestClient(app)

    app.dependency_overrides = {}
