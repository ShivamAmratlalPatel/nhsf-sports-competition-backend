"""Tests for the FakeTwilioClient class."""
from backend.config import TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET
from testing.helpers import FakeTwilioClient


def test_send_message() -> None:
    """Test sending a message."""
    # Arrange
    client = FakeTwilioClient(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)
    to = "+1234567890"
    body = "Hello, Twilio!"

    # Act
    response = client.messages.create(
        body=body,
        messaging_service_sid="",
        to=to,
        shorten_urls=False,
    )

    # Assert
    assert response.to == to
    assert response.body == body
    assert response.sid == "Test"
    assert response.error_code is None
