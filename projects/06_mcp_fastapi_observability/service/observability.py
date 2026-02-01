import logging
from typing import Any, Dict

logger = logging.getLogger("mcp-observability")

SENSITIVE_KEYS = {"token", "secret", "password"}


def _redact(payload: Dict[str, Any]) -> Dict[str, Any]:
    redacted: Dict[str, Any] = {}
    for key, value in payload.items():
        if key in SENSITIVE_KEYS:
            redacted[key] = "***"
        else:
            redacted[key] = value
    return redacted


def log_event(event: str, payload: Dict[str, Any]) -> None:
    logger.info("mcp_event", extra={"event": event, "payload": _redact(payload)})
