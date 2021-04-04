import hashlib
from itertools import cycle
from typing import Any

import pytest


@pytest.fixture
def mock_hash():
    hashlib.md5()

    def _hash(value: str):
        return int(hashlib.md5(value.encode()).hexdigest(), 16)

    return _hash
