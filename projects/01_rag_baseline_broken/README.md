# 01_rag_baseline_broken

Track A — RAG Debugging & Chunking.

## Qué debería incluir

- `ingest.py`: ingesta de documentos con metadata completa.
- `chunking.py`: splitters con overlap razonable y metadata preservada.
- `retriever.py`: retrieval con filtros + MMR/rerank opcional.
- `rag_chain.py`: pipeline de RAG con grounding y citas.
- `vectorstore.py`: ids determinísticos, upsert, idempotencia.
- `prompts.py`: prompts con “no evidence => no answer”.
- `api.py`: endpoint opcional `/ask`.
- `tests/`: tests de ingest, retrieval y grounding.
