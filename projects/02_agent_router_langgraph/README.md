# 02_agent_router_langgraph

Track B — Agent Routing with LangGraph.

## Qué debería incluir

- `graph.py`: definición del grafo (route -> call_tool -> synthesize -> done).
- `state.py`: modelos tipados del estado del agente.
- `tools/`: herramientas con schemas pydantic (weather, finance, docs_search).
- `policies.py`: guardrails y políticas de fallback.
- `tests/`: routing correcto, manejo de errores y stop conditions.
