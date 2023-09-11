"""Test the Wise object."""
from unittest import mock

import pytest
import requests
from requests import Response

from backend.config import (
    WISE_ACCOUNTNO,
    WISE_BASE_URL,
    WISE_PRIVATE_KEY,
    WISE_PROFILE,
    WISE_TOKEN,
)
from backend.helper_clients.bearer_auth import BearerAuth
from backend.helper_clients.wise_client import WiseClient


@pytest.fixture()
def mock_response() -> Response:  # pragma: no cover
    """Mock response object."""
    response = requests.Response()
    response.status_code = 200
    response._content = b'{"message": "OK"}'  # noqa: SLF001
    return response


def test_bearer_auth() -> None:
    """Test that the BearerAuth object is initialized correctly."""
    bearer_auth = BearerAuth(WISE_TOKEN)
    request_mock = mock.Mock()
    request_mock.headers = {}
    request_mock = bearer_auth(request_mock)

    assert "authorization" in request_mock.headers
    expected_auth = f"Bearer {WISE_TOKEN}"
    assert request_mock.headers["authorization"] == expected_auth


def test_wise_client_init() -> None:
    """Test that the WiseClient object is initialized correctly."""
    wise_client = WiseClient(
        WISE_BASE_URL,
        WISE_TOKEN,
        WISE_PROFILE,
        WISE_PRIVATE_KEY,
        WISE_ACCOUNTNO,
    )

    assert wise_client.base_url == WISE_BASE_URL
    assert wise_client.profile_id == WISE_PROFILE
    assert wise_client.account_no == WISE_ACCOUNTNO
    assert wise_client.token == WISE_TOKEN
