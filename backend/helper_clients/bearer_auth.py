"""Bearer auth for requests"""

# from requests import PreparedRequest
from requests import request
from requests.auth import AuthBase


class BearerAuth(AuthBase):
    """BearerAuth"""

    def __init__(self: "BearerAuth", token: str) -> None:
        """token: to use"""
        self.token = token

    def __call__(self: "BearerAuth", r: request):  # noqa: ANN204
        """Override call and inject header"""
        r.headers["authorization"] = "Bearer " + self.token
        return r
