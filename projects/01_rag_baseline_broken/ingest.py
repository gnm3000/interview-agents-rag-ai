from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


def load_documents(data_dir: Path) -> List[Document]:
    """Load documents from the data directory.

    The candidate can extend this loader to support PDFs, HTML, etc.
    """
    documents: List[Document] = []
    for path in data_dir.rglob("*.txt"):
        loader = TextLoader(str(path))
        docs = loader.load()
        for doc in docs:
            doc.metadata.setdefault("source", str(path))
        documents.extend(docs)
    return documents


def normalize_metadata(documents: Iterable[Document]) -> List[Document]:
    """Ensure metadata has required fields for traceability."""
    normalized: List[Document] = []
    for doc in documents:
        metadata = dict(doc.metadata)
        metadata.setdefault("doc_id", metadata.get("source", "unknown"))
        normalized.append(Document(page_content=doc.page_content, metadata=metadata))
    return normalized
