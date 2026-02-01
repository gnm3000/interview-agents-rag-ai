from __future__ import annotations

from typing import Any, Dict, Optional

from langchain_community.vectorstores import Chroma
from langchain_core.retrievers import BaseRetriever


def build_retriever(
    vectorstore: Chroma,
    *,
    k: int = 4,
    filter_by: Optional[Dict[str, Any]] = None,
    use_mmr: bool = True,
) -> BaseRetriever:
    """Return a retriever configured for interview experimentation."""
    search_type = "mmr" if use_mmr else "similarity"
    return vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k, "filter": filter_by or {}},
    )
