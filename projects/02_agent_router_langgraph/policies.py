from __future__ import annotations

from typing import Literal

ALLOWED_ROUTES = {"weather", "finance", "docs_search", "fallback"}


def enforce_route(route: str) -> Literal["weather", "finance", "docs_search", "fallback"]:
    if route in ALLOWED_ROUTES:
        return route  # type: ignore[return-value]
    return "fallback"
