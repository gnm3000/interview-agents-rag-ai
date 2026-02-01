# 01_rag_baseline_broken

Track A — RAG Debugging & Chunking.

## Objetivo
Preparar un baseline de RAG para entrevistas. El candidato debe mejorar chunking,
retrieval y grounding sin romper la trazabilidad de fuentes.

## Qué incluye
- `ingest.py`: ingesta de documentos con metadata completa.
- `chunking.py`: splitters con overlap razonable y metadata preservada.
- `retriever.py`: retrieval con filtros + MMR opcional.
- `rag_chain.py`: pipeline de RAG con grounding y citas.
- `vectorstore.py`: ids determinísticos, upsert, idempotencia.
- `prompts.py`: prompts con “no evidence => no answer”.
- `api.py`: endpoint `/ask` con FastAPI.
- `tests/`: tests base de ingest y vectorstore.

## Tareas sugeridas para la entrevista
1. Ajustar chunking para maximizar recall sin ruido.
2. Agregar filtros por metadata (e.g. `doc_id`, `source`).
3. Incorporar un reranker o agregar citas en el output.
4. Endurecer el prompt contra alucinaciones.

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```

```bash
uvicorn api:app --reload
```
