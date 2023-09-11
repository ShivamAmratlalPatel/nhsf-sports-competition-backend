"""Test helpers.py"""

from pathlib import Path
from typing import Any

import rsa


def get_test_private_key() -> Any:  # noqa: ANN401
    """Load the Test Key into memory"""
    with Path.open("/app/testing/unit_tests/keys/test.key", mode="rb") as _file:
        return _file.read()


TEST_WISE_PRIVATE_KEY = get_test_private_key()


def test_private_key_load_pkcs1() -> None:
    """Test default Loading"""
    rsa.PrivateKey.load_pkcs1(TEST_WISE_PRIVATE_KEY, "PEM")


def test_private_key_load_pkcs1_pem() -> None:
    """Test _pem loading"""
    rsa.PrivateKey._load_pkcs1_pem(TEST_WISE_PRIVATE_KEY)  # noqa: SLF001
