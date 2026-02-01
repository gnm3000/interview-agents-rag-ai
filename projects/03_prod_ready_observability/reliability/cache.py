from cachetools import TTLCache


def get_cache() -> TTLCache:
    return TTLCache(maxsize=512, ttl=60)
