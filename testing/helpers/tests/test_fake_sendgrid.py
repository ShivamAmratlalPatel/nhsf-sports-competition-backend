"""Tests for the FakeSendgridClient class."""
import unittest

from sendgrid.helpers.mail.mail import Mail
from starlette import status

from testing.helpers.fake_data import fake_email
from testing.helpers.fake_sendgrid import (
    FakeSendgridClient,
    FakeSendgridResponse,
    get_fake_sendgrid_template,
)


class TestFakeSendgridClient(unittest.TestCase):
    """Tests for the FakeSendgridClient class."""

    def test_send(self: "TestFakeSendgridClient") -> None:
        """Test send() sends an email and returns a FakeSendgridResponse."""
        client = FakeSendgridClient()
        content = "<strong>test</strong>"
        message = Mail(
            from_email=fake_email(),
            to_emails=fake_email(),
            html_content=content,
        )

        template_data = {
            "test": "test",
        }

        message.dynamic_template_data = template_data
        message.template_id = get_fake_sendgrid_template()
        response = client.send(message)

        # Assert that the message was added to the email_array
        assert message in client.email_array

        # Assert that the response is an instance of TestSendgridResponse
        assert isinstance(response, FakeSendgridResponse)

        # Assert the properties of the response object
        assert response.body == content
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.headers["X-Message-Id"] == "SendgridMessageId"
