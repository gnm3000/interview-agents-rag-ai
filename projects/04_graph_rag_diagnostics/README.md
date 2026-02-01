# 04_graph_rag_diagnostics

Track D — GraphRAG Diagnostics.

## Objetivo
Validar extracción de entidades, retrieval híbrido y razonamiento multi-step.

## Qué incluye
- `ingest/`: extracción de entidades y construcción del grafo.
- `retrieval/`: vector, graph y hybrid retrievers.
- `reasoning/`: planner multi-step.
- `answer/`: síntesis con evidencia y confidence simple.
- `tests/`: queries de GraphRAG.

## Tareas sugeridas
1. Mejorar extracción de entidades (NER real).
2. Integrar embeddings reales y reranking.
3. Agregar score de confianza y validación de rutas.

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```
