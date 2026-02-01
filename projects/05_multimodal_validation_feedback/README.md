# 05_multimodal_validation_feedback

Track E — Multimodal Validation & Feedback Loops.

## Objetivo
Preparar un pipeline multimodal con validación y feedback para entrenamiento
posterior.

## Qué incluye
- `ingest/`: ingesta PDF + imágenes, normalización multimodal.
- `synthesis/`: generación de contenido estructurado (Q/A, procedures).
- `validation/`: validadores rule-based + LLM judge, confidence scoring.
- `feedback/`: store de resultados reales y selección de retraining.
- `api/`: servicio de acceso controlado.
- `tests/`: validación y confidence score.

## Tareas sugeridas
1. Integrar OCR/vision para imágenes.
2. Reemplazar `llm_judge` por un modelo real.
3. Generar estadísticas de feedback para retraining.

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```

```bash
uvicorn api.main:app --reload
```
