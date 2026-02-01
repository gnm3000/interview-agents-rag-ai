from __future__ import annotations

from typing import Iterator

import httpx
from cachetools import TTLCache

from reliability.cache import get_cache


def get_http_client() -> Iterator[httpx.Client]:
    with httpx.Client(timeout=5.0) as client:
        yield client


def get_response_cache() -> TTLCache:
    return get_cache()
