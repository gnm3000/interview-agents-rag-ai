from __future__ import annotations

import logging
from datetime import datetime

from cachetools import TTLCache
from fastapi import APIRouter, Depends

from reliability.retry import with_retry
from service.dependencies import get_response_cache

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@router.get("/ask")
@with_retry()
async def ask(query: str, cache: TTLCache = Depends(get_response_cache)):
    if query in cache:
        logger.info("cache_hit", extra={"query": query})
        return {"query": query, "answer": cache[query], "cached": True}

    answer = f"Echo: {query}"  # TODO: replace with RAG or LLM call
    cache[query] = answer
    logger.info("cache_miss", extra={"query": query})
    return {"query": query, "answer": answer, "cached": False}
