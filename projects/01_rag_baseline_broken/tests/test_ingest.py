from pathlib import Path

from ingest import load_documents, normalize_metadata


def test_load_documents_sets_source():
    data_dir = Path(__file__).parents[1] / "data" / "sample_docs"
    docs = load_documents(data_dir)
    assert docs, "Expected sample docs"
    assert all("source" in doc.metadata for doc in docs)


def test_normalize_metadata_adds_doc_id():
    data_dir = Path(__file__).parents[1] / "data" / "sample_docs"
    docs = normalize_metadata(load_documents(data_dir))
    assert all("doc_id" in doc.metadata for doc in docs)
