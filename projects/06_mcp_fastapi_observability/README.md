# 06_mcp_fastapi_observability (MCP avanzado + FastAPI + Observability)

## Propósito de evaluación

Evaluar la capacidad del candidato para diseñar y depurar un servidor MCP (Model Context Protocol) avanzado en FastAPI, con foco en observabilidad, seguridad, control de costos y compliance operacional.

## Contexto funcional

Se construye un "MCP Hub" interno que expone:

- **Tools** (ejecución de acciones internas)
- **Resources** (datos versionados y metadata)
- **Prompts** (plantillas reutilizables)
- **Sampling** (control de cuota, throttling, límites por tenant)

El hub se usa por múltiples equipos, por lo que requiere trazabilidad, métricas y controles finos.

## Estructura

```
06_mcp_fastapi_observability/
  README.md
  pyproject.toml
  service/
    __init__.py
    main.py
    routes.py
    mcp_models.py
    registry.py
    observability.py
    policies.py
  data/
    sample_catalog.json
  tests/
    test_mcp_api.py
```

## Fallas intencionales (para arreglar)

- **Observabilidad parcial**: no hay correlación `trace_id` entre `initialize`, `tools/call` y `resources/list`.
- **Redacción de datos** incompleta: se registran inputs sensibles sin máscara.
- **Control de cuota** inconsistente: los límites por tenant no se aplican a `tools/call`.
- **Tool schemas** inconsistentes: el catálogo declara un `input_schema` distinto a la validación real.
- **Pagination** incorrecta: `next_cursor` no es estable bajo actualizaciones.
- **Capabilities MCP** incompletas: falta declarar `prompts` y `sampling` como soportados.

## Requisitos funcionales (RF)

- **RF-60**: Endpoint `/mcp/initialize` retorna capabilities reales del servidor.
- **RF-61**: Endpoint `/mcp/resources/list` soporta filtros y paginación determinística.
- **RF-62**: Endpoint `/mcp/tools/call` valida inputs con schema versionado.
- **RF-63**: Endpoint `/mcp/prompts/list` expone templates por dominio.
- **RF-64**: Endpoint `/mcp/sampling/limits` devuelve cuotas por tenant y feature.
- **RF-65**: El hub debe propagar `trace_id`, `request_id` y `tenant_id` en logs.

## Requisitos no funcionales (RNF)

- **RNF-60**: Observabilidad mínima (latency, error_rate, tool_calls, token_estimate).
- **RNF-61**: Redacción de PII en logs.
- **RNF-62**: Determinismo en paginación (tests reproducibles).
- **RNF-63**: Documentar tradeoffs de seguridad vs debugging.

## Criterios de aceptación (CA)

- **CA-60**: `pytest` pasa y valida los flujos MCP críticos.
- **CA-61**: Logs incluyen `trace_id` y `tenant_id` en cada request.
- **CA-62**: Tool call rechaza payloads que no cumplan con el schema.

## Interview questions (para evaluar en vivo)

1. ¿Cómo versionarías el catálogo MCP para permitir backward compatibility?
2. ¿Cómo diseñarías la paginación para evitar saltos cuando el catálogo cambia?
3. ¿Qué estrategia usarías para redacción de PII sin perder debuggability?
4. ¿Cómo modelarías rate limits por tenant vs por tool?
5. ¿Qué métricas serían obligatorias para MCP observability?
6. ¿Cómo instrumentarías tracing distribuido entre cliente MCP y servidor?
7. ¿Cómo asegurarías que `tool` y `resource` mantienen contratos compatibles?
8. ¿Cómo manejarías errores en `tools/call` sin filtrar secretos?
9. ¿Qué harías para controlar costos por tool (LLM calls, APIs externas)?
10. ¿Cómo probarías determinismo de paginación y caching?

## Notas para el entrevistador

Este proyecto está diseñado para discutir MCP en profundidad (capabilities, contratos, observabilidad, y control de costos). El objetivo no es terminar todo, sino evaluar diagnóstico y priorización.
