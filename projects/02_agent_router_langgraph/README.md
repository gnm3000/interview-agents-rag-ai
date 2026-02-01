# 02_agent_router_langgraph

Track B — Agent Routing with LangGraph.

## Objetivo
El candidato debe mejorar el enrutamiento, agregar herramientas reales y reforzar
políticas/guardrails.

## Qué incluye
- `graph.py`: definición del grafo (route -> call_tool -> synthesize -> done).
- `state.py`: modelos tipados del estado del agente.
- `tools/`: herramientas con schemas pydantic (weather, finance, docs_search).
- `policies.py`: guardrails y políticas de fallback.
- `tests/`: routing correcto y stop conditions básicas.

## Tareas sugeridas
1. Reemplazar el router simple por un router LLM con fallback.
2. Agregar manejo de errores en las herramientas.
3. Incluir stop conditions (max depth, timeouts).

## Cómo correr
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```
