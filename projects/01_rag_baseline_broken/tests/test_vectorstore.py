from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from vectorstore import get_vectorstore, upsert_documents


class DummyEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[float(len(text) % 5)] * 3 for text in texts]

    def embed_query(self, text):
        return [float(len(text) % 5)] * 3


def test_upsert_documents_returns_ids(tmp_path: Path):
    store = get_vectorstore(
        persist_directory=tmp_path,
        embedding=DummyEmbeddings(),
        collection_name="test-collection",
    )
    docs = [Document(page_content="hello", metadata={"source": "x"})]
    ids = upsert_documents(store, docs)
    assert len(ids) == 1
