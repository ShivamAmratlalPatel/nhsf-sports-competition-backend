"""Tests for the Fake WISE client."""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import pytz
from requests import Response
from starlette import status

from testing.helpers.fake_wise import FakeWiseClient


@pytest.fixture()
def fake_client() -> FakeWiseClient:
    """Get a fake Wise client."""
    return FakeWiseClient()


def test_get_wise_transfer_successful(fake_client: FakeWiseClient) -> None:
    """Test a successful response for a specific amount and occurred_at"""
    amount = 100
    occurred_at = datetime(2023, 7, 29, tzinfo=pytz.timezone("Europe/London"))

    with patch("requests.get") as mock_get:
        expected_response = {
            "created": occurred_at.isoformat(),
            "details": {"reference": "payref123"},
            "id": "123456789",
            "targetValue": amount,
        }
        mock_response = Mock(spec=Response)
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        response = fake_client.get_lineitem(occurred_at, amount, "CREDIT")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_get_wise_transfer_invalid_response(fake_client: FakeWiseClient) -> None:
    """Test a 200 response but invalid response body"""
    amount = 100
    occurred_at = datetime(2023, 7, 30, 0, 0, tzinfo=pytz.timezone("Europe/London"))

    with patch("requests.get") as mock_get:
        expected_response = {
            "details": {"reference": "payref123"},
            "id": "123456789",
            "targetValue": amount,
        }
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        response = fake_client.get_lineitem(occurred_at, amount, "CREDIT")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_get_wise_transfer_not_found(fake_client: FakeWiseClient) -> None:
    """Test a 404 response for an amount and occurred_at that does not exist"""
    amount = 200
    occurred_at = datetime(2023, 7, 31, tzinfo=pytz.timezone("Europe/London"))

    with patch("requests.get") as mock_get:
        expected_response = {"error": "Transfer not found"}
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        response = fake_client.get_lineitem(occurred_at, amount, "CREDIT")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response


def test_get_wise_transfer_invalid_amount(fake_client: FakeWiseClient) -> None:
    """Test invalid amount (negative amount) input"""
    amount = -50
    occurred_at = datetime(2023, 7, 29, tzinfo=pytz.timezone("Europe/London"))

    response = fake_client.get_lineitem(occurred_at, amount, "CREDIT")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Transfer not found"}


def test_get_wise_transfer_invalid_date(fake_client: FakeWiseClient) -> None:
    """Test invalid date input (future date)"""
    amount = 100
    occurred_at = datetime(2030, 7, 29, tzinfo=pytz.timezone("Europe/London"))

    response = fake_client.get_lineitem(occurred_at, amount, "CREDIT")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Transfer not found"}
