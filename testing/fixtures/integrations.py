"""Integration test fixtures."""
import pytest

from backend.config import TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET
from testing.helpers import (
    FakeS3Client,
    FakeSendgridClient,
    FakeTwilioClient,
    FakeWiseClient,
)


@pytest.fixture()
def sendgrid_client() -> FakeSendgridClient:
    """Get a fake Sendgrid client."""
    return FakeSendgridClient()


@pytest.fixture()
def twilio_client() -> FakeTwilioClient:
    """Get a fake Twilio client."""
    return FakeTwilioClient(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)


@pytest.fixture()
def wise_client() -> FakeWiseClient:
    """Get a fake Wise client."""
    return FakeWiseClient()


@pytest.fixture()
def s3_client() -> FakeS3Client:
    """Get a fake S3 client."""
    return FakeS3Client()
