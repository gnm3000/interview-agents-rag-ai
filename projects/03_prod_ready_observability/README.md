# 03_prod_ready_observability

Track C — Production Readiness & Observability.

## Objetivo
El candidato debe elevar un servicio FastAPI con retry policies, caching y
observabilidad mínima para producción.

## Qué incluye
- `service/`: FastAPI app y endpoints.
- `infra/`: docker-compose local.
- `reliability/`: retry policy, timeouts y cache.
- `eval/`: regression suite básica.
- `tests/`: API y políticas de cache.

## Tareas sugeridas
1. Agregar métricas (latencia, errores).
2. Implementar tracing distribuido (OpenTelemetry).
3. Endurecer políticas de retry/timeouts.

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```

```bash
uvicorn service.main:app --reload
```
