"""Fake Sendgrid client for testing purposes."""
from sendgrid.helpers.mail.mail import Mail
from starlette import status

from backend.utils import generate_uuid


class FakeSendgridResponse:
    """Fake Sendgrid response for testing purposes."""

    def __init__(self: "FakeSendgridResponse", body: Mail) -> None:
        """Initialise the fake Sendgrid response."""
        if body.contents:
            self.body = body.contents[0].content
        if (
            body.get()["personalizations"][0]["to"][0]["email"]
            == "bad_email@bad_email.com"
        ):
            self.status_code = status.HTTP_400_BAD_REQUEST
        else:
            self.status_code = status.HTTP_202_ACCEPTED
        self.headers = {"X-Message-Id": "SendgridMessageId"}


class FakeSendgridClient:
    """Fake Sendgrid client for testing purposes."""

    def __init__(self: "FakeSendgridClient") -> None:
        """Initialise the fake Sendgrid client."""
        self.email_array: list[Mail] = []

    def send(self: "FakeSendgridClient", message: Mail) -> FakeSendgridResponse:
        """Send an email."""
        self.email_array.append(message)
        return FakeSendgridResponse(message)


def get_fake_sendgrid_template() -> str:
    """Return a fake Sendgrid template ID."""
    return str(generate_uuid())
