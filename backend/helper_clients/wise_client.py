"""WiseClient"""

import base64
from datetime import datetime, timedelta
from urllib import response
from urllib.parse import urlencode

import requests
import rsa
from fastapi import HTTPException, status

from backend.helper_clients.bearer_auth import BearerAuth


class WiseClient:
    """Wiseclient"""

    def __init__(  # noqa: PLR0913
        self: "WiseClient",
        base_url: str,
        token: str,
        profile_id: str,
        private_key: str,
        account_no: str,
    ) -> None:
        """Init"""
        self.base_url = base_url
        self.token = token
        self.profile_id = profile_id
        self._private_key = rsa.PrivateKey.load_pkcs1(private_key, "PEM")
        self.account_no = account_no

    def _do_sca_challenge(
        self: "WiseClient",
        one_time_token: str,
    ) -> bytes:  # pragma: no cover
        """Sign the one time token"""
        # Use the private key to sign the one-time-token that was returned
        # in the x-2fa-approval header of the HTTP 403.

        signed_token = rsa.sign(
            one_time_token.encode("ascii"),
            self._private_key,
            "SHA-256",
        )

        # Encode the signed message as friendly base64 format for HTTP
        # headers.
        return base64.b64encode(signed_token).decode("ascii")

    def get_transfer(
        self: "WiseClient",
        transfer_id: str,
    ) -> response:  # pragma: no cover
        """Find a specific transfer"""
        url = self.base_url + f"/v1/transfers/{transfer_id}"
        return requests.get(url, auth=BearerAuth(self.token))  # noqa: S113

    def get_balance_statement(
        self: "WiseClient",
        occurred_at: datetime,
        one_time_token: str = "",
        signature: str = "",
    ) -> response:  # pragma: no cover
        """Get the current statement"""
        params = urlencode(
            {
                "currency": "GBP",
                "type": "COMPACT",
                "intervalStart": (occurred_at + timedelta(minutes=-1)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                ),
                "intervalEnd": (occurred_at + timedelta(minutes=1)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ",
                ),
            },
        )

        url = (
            self.base_url
            + f"/v1/profiles/{self.profile_id}/balance-statements/{self.account_no}/statement.json?"
            + params
        )

        #'Authorization': 'Bearer ' + self.token,
        headers = {
            "User-Agent": "tw-statements-sca",
            "Content-Type": "application/json",
        }
        if one_time_token:
            headers["x-2fa-approval"] = one_time_token
            headers["X-Signature"] = signature
            print(headers["x-2fa-approval"], headers["X-Signature"])  # noqa: T201

        print("GET", url)  # noqa: T201

        r = requests.get(  # noqa: S113
            url,
            headers=headers,
            auth=BearerAuth(self.token),
        )
        # r = http.request('GET', url, headers=headers, retries=False)
        print("status:", r.status_code)  # noqa: T201

        if r.status_code == 200 or r.status_code == 201:  # noqa: PLR2004
            return r
        elif (
            r.status_code == 403  # noqa: PLR2004
            and r.headers["x-2fa-approval"] is not None
        ):
            one_time_token = r.headers["x-2fa-approval"]
            signature = self.do_sca_challenge(one_time_token)
            return self.get_statement(occurred_at, one_time_token, signature)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Payment Balance enquiry failed",
            )

    def get_balance_statement_old(
        self: "WiseClient",
        occurred_at: datetime,
    ) -> response:  # pragma: no cover
        """Get the current statement"""
        url = (
            self.base_url
            + f"/v1/profiles/{self.profile_id}/balance-statements/{self.account_no}/statement.json?currency=GBP"
            + f"&intervalStart={occurred_at.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            + f"&intervalEnd={(occurred_at + timedelta(minutes = 1)).strftime('%Y-%m-%dT%H:%M:%SZ') }&type=COMPACT"
        )
        fail_request = requests.get(url, auth=BearerAuth(self.token))  # noqa: S113
        if fail_request.status_code == 201:  # noqa: PLR2004
            return fail_request
        one_time_token = fail_request.headers["x-2fa-approval"]
        signature = self._do_sca_challenge(one_time_token)
        headers = {
            "x-2fa-approval": one_time_token,
            "X-Signature": signature,
        }
        return requests.get(  # noqa: S113
            url,
            auth=BearerAuth(self.token),
            headers=headers,
        )

    def get_lineitem(
        self: "WiseClient",
        occurred_at: datetime,
        amount: float,
        transaction_type: str = "CREDIT",
    ) -> response:  # pragma: no cover
        """Find a single LineItem"""
        balance_statement = self.get_balance_statement(occurred_at)
        if balance_statement.status_code != 200:  # noqa: PLR2004
            raise HTTPException(balance_statement.status_code, balance_statement.text)

        transactions = balance_statement.json()["transactions"]
        transfer = next(
            (
                transaction
                for transaction in transactions
                if transaction["type"] == transaction_type
                and transaction["amount"]["value"] == amount
            ),
            None,
        )
        if transfer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transfer not found",
            )
        transfer_id: str = transfer["referenceNumber"].replace("TRANSFER-", "")
        transfer = self.get_transfer(transfer_id)
        if transfer.status_code == 200:  # noqa: PLR2004
            if transfer.json()["hasActiveIssues"] is True:
                raise HTTPException(status_code=400, detail="Lineitem has issues")
            return transfer

        raise HTTPException(transfer.status_code, transfer.text)
