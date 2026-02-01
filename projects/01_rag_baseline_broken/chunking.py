from __future__ import annotations

from typing import Iterable, List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: Iterable[Document],
    *,
    chunk_size: int = 500,
    chunk_overlap: int = 80,
) -> List[Document]:
    """Split documents while preserving metadata.

    Adjust chunk_size/chunk_overlap during the interview to tune recall.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(list(documents))
