"""Helper functions."""
from sendgrid import SendGridAPIClient
from sqlalchemy.orm import Session
from twilio.rest import Client as TwilioClient

from backend import database
from backend.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    SENDGRID_API_KEY,
    TWILIO_ACCOUNT_SID,
    TWILIO_API_KEY,
    TWILIO_API_SECRET,
    WISE_ACCOUNTNO,
    WISE_BASE_URL,
    WISE_PRIVATE_KEY,
    WISE_PROFILE,
    WISE_TOKEN,
)
from backend.helper_clients import S3Client, WiseClient


def get_db() -> Session:  # pragma: no cover
    """
    Get a database session.

    Returns
        Session: database session

    """
    db = None
    try:
        db = database.session_local_factory()()
        yield db
    finally:
        if db:
            db.close()


def get_wise_client() -> WiseClient:
    """Get a simple WISE Client with correct settings"""
    return WiseClient(
        WISE_BASE_URL,
        WISE_TOKEN,
        WISE_PROFILE,
        WISE_PRIVATE_KEY,
        WISE_ACCOUNTNO,
    )


def get_s3_client() -> S3Client:
    """
    Get an S3 client.

    Returns
        S3Client: S3 client

    """
    return S3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


def get_sendgrid_client() -> SendGridAPIClient:
    """
    Get a SendGrid client.

    Returns
        SendGridAPIClient: SendGrid client

    """
    return SendGridAPIClient(SENDGRID_API_KEY)


def get_twilio_client() -> TwilioClient:  # pragma: no cover
    """
    Get a Twilio client.

    Returns
        TwilioClient: Twilio client

    """
    return TwilioClient(TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_ACCOUNT_SID)
