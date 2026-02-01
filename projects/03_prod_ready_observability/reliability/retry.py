from __future__ import annotations

from typing import Callable

from tenacity import retry, stop_after_attempt, wait_exponential


def with_retry(attempts: int = 3) -> Callable:
    return retry(
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        reraise=True,
    )
