from typing import Dict

DEFAULT_LIMITS = {
    "tools_per_minute": 30,
    "resources_per_minute": 60,
    "prompts_per_minute": 120,
}

TENANT_OVERRIDES: Dict[str, Dict[str, int]] = {
    "enterprise": {"tools_per_minute": 120},
}


def get_limits(tenant_id: str) -> Dict[str, int]:
    limits = DEFAULT_LIMITS.copy()
    overrides = TENANT_OVERRIDES.get(tenant_id)
    if overrides:
        limits.update(overrides)
    return limits
