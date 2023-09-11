"""Configuration for the backend application."""
import os

import pem

try:  # pragma: no cover
    AGREEMENT_BUCKET_NAME = os.environ["AGREEMENT_BUCKET_NAME"]
except KeyError:  # pragma: no cover
    AGREEMENT_BUCKET_NAME = ""

try:  # pragma: no cover
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
except KeyError:  # pragma: no cover
    AWS_ACCESS_KEY_ID = ""

try:  # pragma: no cover
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
except KeyError:  # pragma: no cover
    AWS_SECRET_ACCESS_KEY = ""

try:  # pragma: no cover
    AWS_REGION = os.environ["AWS_REGION"]
except KeyError:  # pragma: no cover
    AWS_REGION = ""

try:  # pragma: no cover
    BACKEND_ENDPOINT = os.environ["BACKEND_ENDPOINT"]
except KeyError:  # pragma: no cover
    BACKEND_ENDPOINT = ""

try:  # pragma: no cover
    CORS_ORIGINS = os.environ["CORS_ORIGINS"]
except KeyError:  # pragma: no cover
    CORS_ORIGINS = ""

try:  # pragma: no cover
    ENVIRONMENT = os.environ["ENVIRONMENT"]
except KeyError:  # pragma: no cover
    ENVIRONMENT = ""

try:  # pragma: no cover
    FRONTEND_ENDPOINT = os.environ["FRONTEND_ENDPOINT"]
except KeyError:  # pragma: no cover
    FRONTEND_ENDPOINT = ""

try:  # pragma: no cover
    INFO_EMAIL = os.environ["INFO_EMAIL"]
except KeyError:  # pragma: no cover
    INFO_EMAIL = ""

try:  # pragma: no cover
    PDF_CLIENT_ID = os.environ["PDF_CLIENT_ID"]
except KeyError:  # pragma: no cover
    PDF_CLIENT_ID = ""

try:  # pragma: no cover
    PDF_CLIENT_SECRET = os.environ["PDF_CLIENT_SECRET"]
except KeyError:  # pragma: no cover
    PDF_CLIENT_SECRET = ""

try:  # pragma: no cover
    PDF_SERVICE_URL = os.environ["PDF_SERVICE_URL"]
except KeyError:  # pragma: no cover
    PDF_SERVICE_URL = ""

try:  # pragma: no cover
    WISE_BASE_URL = os.environ["WISE_BASE_URL"]
except KeyError:  # pragma: no cover
    WISE_BASE_URL = ""
try:  # pragma: no cover
    WISE_TOKEN = os.environ["WISE_TOKEN"]
except KeyError:  # pragma: no cover
    WISE_TOKEN = ""
try:  # pragma: no cover
    WISE_PROFILE = os.environ["WISE_PROFILE"]
except KeyError:  # pragma: no cover
    WISE_PROFILE = ""
try:  # pragma: no cover
    WISE_ACCOUNTNO = os.environ["WISE_ACCOUNTNO"]
except KeyError:  # pragma: no cover
    WISE_ACCOUNTNO = ""
try:  # pragma: no cover
    WISE_PRIVATE_KEY_FILE = os.environ["WISE_PRIVATE_KEY_FILE"]
except KeyError:  # pragma: no cover
    WISE_PRIVATE_KEY_FILE = ""  # "/opt/secrets/wise_private_key.pem"

try:  # pragma: no cover
    if not WISE_PRIVATE_KEY_FILE:
        WISE_PRIVATE_KEY = ""
    else:
        WISE_PRIVATE_KEY = pem.parse_file(WISE_PRIVATE_KEY_FILE)[0].as_bytes()
except KeyError:  # pragma: no cover
    WISE_PRIVATE_KEY = ""  # "/opt/secrets/wise_private_key.pem"


try:  # pragma: no cover
    SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
except KeyError:  # pragma: no cover
    SENDGRID_API_KEY = ""

try:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_COUNTERSIGNED = os.environ[
        "SG_TEMPLATE_AGREEMENT_COUNTERSIGNED"
    ]
except KeyError:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_COUNTERSIGNED = ""

try:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_COUNTERSIGNED_THIRDPATY = os.environ[
        "SG_TEMPLATE_AGREEMENT_COUNTERSIGNED_THIRDPATY"
    ]
except KeyError:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_COUNTERSIGNED_THIRDPATY = ""

try:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_SIGNING = os.environ["SG_TEMPLATE_AGREEMENT_SIGNING"]
except KeyError:  # pragma: no cover
    SG_TEMPLATE_AGREEMENT_SIGNING = ""

try:  # pragma: no cover
    SLACK_ALERT_WEBHOOK = os.environ["SLACK_ALERT_WEBHOOK"]
except KeyError:  # pragma: no cover
    SLACK_ALERT_WEBHOOK = ""

try:  # pragma: no cover
    SLACK_PAYMENT_WEBHOOK = os.environ["SLACK_PAYMENT_WEBHOOK"]
except KeyError:  # pragma: no cover
    SLACK_PAYMENT_WEBHOOK = ""

try:  # pragma: no cover
    TWILIO_MESSAGING_SID = os.environ["TWILIO_MESSAGING_SID"]
except KeyError:  # pragma: no cover
    TWILIO_MESSAGING_SID = ""

try:  # pragma: no cover
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
except KeyError:  # pragma: no cover
    TWILIO_ACCOUNT_SID = ""

try:  # pragma: no cover
    TWILIO_API_KEY = os.environ["TWILIO_API_KEY"]
except KeyError:  # pragma: no cover
    TWILIO_API_KEY = ""

try:  # pragma: no cover
    TWILIO_API_SECRET = os.environ["TWILIO_API_SECRET"]
except KeyError:  # pragma: no cover
    TWILIO_API_SECRET = ""

try:  # pragma: no cover
    SUPPORT_FROM_RENT_CENTAINTY_EMAIL = f"Rent Certainty Support <support{INFO_EMAIL}>"
except KeyError:  # pragma: no cover
    SUPPORT_FROM_RENT_CENTAINTY_EMAIL = ""
