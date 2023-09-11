"""Basic auth for requests"""
import base64

from requests import PreparedRequest
from requests.auth import AuthBase


class BasicAuth(AuthBase):
    """Basic auth for requests"""

    def __init__(self: "BasicAuth", client_id: str, client_secret: str) -> None:
        """Init basic auth"""
        self.client_id = client_id
        self.client_secret = client_secret

    def __call__(
        self: "BasicAuth",
        r: PreparedRequest,
    ) -> PreparedRequest:
        """Add basic auth to request"""
        auth = self.client_id + ":" + self.client_secret
        base64_auth = base64.b64encode(auth.encode()).decode()
        if r.headers is None:
            r.headers = {}
        r.headers["authorization"] = "Basic " + base64_auth
        return r
