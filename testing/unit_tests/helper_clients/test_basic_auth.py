"""Test basic auth"""
from requests import PreparedRequest

from backend.helper_clients.basic_auth import BasicAuth


def test_basic_auth() -> None:
    """Test basic auth"""
    client_id = "your_client_id"
    client_secret = "your_client_secret"  # noqa: S105
    auth = BasicAuth(client_id, client_secret)
    request = PreparedRequest()
    request = auth(request)
    assert "authorization" in request.headers
    assert request.headers["authorization"].startswith("Basic ")
