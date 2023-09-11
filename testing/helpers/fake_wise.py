"""Fake Wise client for testing"""
from datetime import datetime
from unittest.mock import Mock

import pytz
from requests import Response
from starlette import status


class FakeWiseClient:
    """Fake Wise client for testing"""

    def __init__(self: "FakeWiseClient") -> None:
        """Initialize the fake client"""

    def get_lineitem(
        self: "FakeWiseClient",
        occurred_at: datetime,
        amount: float,
        transaction_type: str = "CREDIT",  # noqa: ARG002
    ) -> Response:
        """Fake implementation of get_lineitem method"""
        # For testing purposes, we'll return a mocked response instead of making an actual request
        # You can customize this response to test different scenarios
        response = Mock(spec=Response)

        test_amount = float(100)
        amount = float(amount)

        # Customize the response according to your test cases
        if amount == test_amount and occurred_at == datetime(
            2023,
            7,
            29,
            tzinfo=pytz.timezone("Europe/London"),
        ):
            response.status_code = status.HTTP_200_OK
            response.json.return_value = {
                "id": "123456789",
                "targetValue": amount,
                "details": {"reference": "payref123"},
                "created": occurred_at.isoformat(),
            }
        elif amount == test_amount and occurred_at == datetime(
            2023,
            7,
            30,
            0,
            0,
            tzinfo=pytz.timezone("Europe/London"),
        ):
            response.status_code = status.HTTP_200_OK
            response.json.return_value = {
                "id": "123456789",
                "targetValue": amount,
                "details": {"reference": "payref123"},
            }
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.json.return_value = {"error": "Transfer not found"}

        return response
