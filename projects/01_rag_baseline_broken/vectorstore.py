from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, List

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def _stable_id(document: Document) -> str:
    payload = f"{document.metadata.get('source','')}::{document.page_content}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get_vectorstore(
    *,
    persist_directory: Path,
    embedding: Embeddings,
    collection_name: str = "rag-baseline",
) -> Chroma:
    persist_directory.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(persist_directory),
        embedding_function=embedding,
    )


def upsert_documents(
    vectorstore: Chroma,
    documents: Iterable[Document],
) -> List[str]:
    docs = list(documents)
    ids = [_stable_id(doc) for doc in docs]
    vectorstore.add_documents(docs, ids=ids)
    return ids
