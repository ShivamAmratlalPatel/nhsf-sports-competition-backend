"""Test helpers.py"""

from pathlib import Path
from typing import Any
from unittest import mock

from sendgrid import SendGridAPIClient

from backend.helper_clients import S3Client, WiseClient
from backend.helpers import (
    get_s3_client,
    get_sendgrid_client,
    get_wise_client,
)


def get_test_private_key() -> Any:  # noqa: ANN401
    """Load the Test Key into memory"""
    with Path.open("/app/testing/unit_tests/keys/test.key", mode="rb") as _file:
        return _file.read()


TEST_WISE_PRIVATE_KEY = get_test_private_key()


@mock.patch("backend.helpers.WISE_PRIVATE_KEY", TEST_WISE_PRIVATE_KEY)
def test_get_wise_client() -> None:
    """Test that the function returns a WiseClient object."""
    # Call the function under test
    wise_client = get_wise_client()
    # Assert that the function returns a WiseClient object
    assert isinstance(wise_client, WiseClient)


def test_get_s3_client() -> None:
    """Test that the function returns an S3Client object."""
    # Call the function under test
    s3_client = get_s3_client()

    # Assert that the function returns an S3Client object
    assert isinstance(s3_client, S3Client)


def test_get_sendgrid_client() -> None:
    """Test that the function returns a SendGridAPIClient object."""
    # Call the function under test
    sendgrid_client = get_sendgrid_client()

    # Assert that the function returns a SendGridAPIClient object
    assert isinstance(sendgrid_client, SendGridAPIClient)
