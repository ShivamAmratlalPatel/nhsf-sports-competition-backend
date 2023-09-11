"""Fake Twilio client for testing."""


class TestTwilioResponse:
    """Fake Twilio response."""

    def __init__(
        self: "TestTwilioResponse",
        to: str,
        body: str,
        success: bool = True,
    ) -> None:
        """Initialize TestTwilioResponse."""
        self.sid = "Test"
        self.error_code = None if success else "Test_Error_Code"
        self.to = to
        self.body = body


class Message:
    """Fake Twilio client message."""

    def __init__(self: "Message") -> None:
        """Initialize FakeTwilioClient.Message."""

    def create(
        body: str,
        messaging_service_sid: str,
        to: str,
        shorten_urls: bool,
    ) -> TestTwilioResponse:
        """Create a fake Twilio response."""
        _ = messaging_service_sid
        _ = shorten_urls
        del _
        if to == "bad_number":
            return TestTwilioResponse(
                to,
                body,
                success=False,
            )
        return TestTwilioResponse(
            to,
            body,
        )


class FakeTwilioClient:
    """Fake Twilio client."""

    def __init__(
        self: "FakeTwilioClient",
        twilio_api_key: str,
        twilio_api_secret: str,
        twilio_account_sid: str,
    ) -> None:
        """Initialize FakeTwilioClient."""
        self.messages = Message
        self.account_sid = twilio_account_sid
        self.api_key = twilio_api_key
        self.api_secret = twilio_api_secret
