# interview-agents-rag-ai

## Objetivo del repositorio
Repositorio “interview-ready” para evaluar en live-coding a un candidato en Agents + RAG usando LangChain + LangGraph, con foco en:

- Vector DB (diseño, filtros, embeddings, idempotencia, upserts)
- RAG (retrieval, rerank, grounding, citas, failure modes)
- Chunking strategies (splitters, overlap, structure-aware, metadata)
- Agents production-ready (tooling, routing, state, retries, tracing, tests, cost/latency)
- GraphRAG y razonamiento multi-step
- Multimodal ingestion + validación + feedback loops

## Choose your challenge (pick ONE)

- Track A – RAG Debugging & Chunking (01)
- Track B – Agent Routing with LangGraph (02)
- Track C – Production Readiness & Observability (03)
- Track D – GraphRAG Diagnostics (04)
- Track E – Multimodal Validation & Feedback Loops (05)

## Skills evaluadas por track

| Track | Skills Evaluated |
|------|------------------|
| 01 | Vector DBs, chunking, grounding, RAG evaluation |
| 02 | Agentic systems, tool routing, LangGraph, state |
| 03 | Production AI, retries, cost, observability |
| 04 | GraphRAG, multi-step reasoning, diagnostics |
| 05 | Multimodal AI, validation, confidence, feedback |

## Expectations (Senior/Staff level)

This repository is designed for Senior / Staff-level candidates.

We do NOT expect:
- finishing everything
- perfect code

We DO evaluate:
- diagnosis
- prioritization
- correctness
- production thinking
- ability to reason about tradeoffs

## Constraints

- Do not add new external services unless justified
- Prefer tests over explanations
- Prefer small, correct fixes over rewrites
- Explain tradeoffs verbally

## Reglas de la entrevista

- No se busca terminar todo. Se evalúa diagnosis, priorización, tradeoffs, tests y producción.
- El candidato elige un track y trabaja en vivo sobre ese proyecto.
- Cada proyecto está “casi completo” pero con bugs/diseños intencionalmente malos.

## Comandos

- `make setup`
- `make run PROJECT=01`
- `make test PROJECT=01`
- `make eval PROJECT=01`

## Diseño general del repo

Estructura propuesta:

```
ai-agents-interview-repo/
  README.md
  docs/
    interview_guide.md           # guía del entrevistador + rubric
    scoring_rubric.md            # scoring por competencias
    datasets/                    # documentos sample y ground-truth
  common/
    config.py                    # settings pydantic
    logging.py                   # structured logging
    tracing.py                   # langsmith/langfuse hooks (stub)
    types.py                     # dataclasses / pydantic models
    eval/
      metrics.py                 # RAG metrics (exact match, citation coverage)
      harness.py                 # runner de eval offline
  projects/
    01_rag_baseline_broken/
    02_agent_router_langgraph/
    03_prod_ready_observability/
    04_graph_rag_diagnostics/
    05_multimodal_validation_feedback/
  scripts/
    setup.sh
    run_project.sh
  pyproject.toml
  .env.example
```

## Convenciones obligatorias (repo-wide)

- Python 3.11+
- pyproject.toml con extras por proyecto: `.[rag]`, `.[agent]`, `.[prod]`
- `make test`, `make lint`, `make run PROJECT=01`
- Config por `pydantic-settings` (env vars) + `.env.example`
- Tests con pytest y fixtures de dataset estático
- “Golden tests” para respuestas con citas (snapshot o asserts mínimos)

## Proyecto 01: 01_rag_baseline_broken (RAG + chunking + vectorDB)

### Propósito de evaluación

- Diagnosticar por qué el RAG alucina, no cita, recupera mal
- Arreglar chunking/metadata
- Arreglar indexación/idempotencia
- Agregar rerank o mejorar retriever
- Agregar pruebas mínimas y un harness de evaluación

### Componentes

```
01_rag_baseline_broken/
  README.md
  ingest.py
  chunking.py
  retriever.py
  rag_chain.py
  vectorstore.py
  prompts.py
  api.py                     # FastAPI opcional (endpoint /ask)
  tests/
    test_ingest.py
    test_retrieval.py
    test_grounding.py
```

### Bugs/diseños intencionalmente malos (para “arreglar”)

- Chunking defectuoso
  - Usa splitter fijo por caracteres sin respetar estructura (headers/listas)
  - Overlap mal configurado (0 o exagerado)
  - Pierde metadatos de source/page/section
- Vectorstore mal usado
  - IDs no determinísticos → duplicados en re-ingest
  - No hay upsert / no hay “delete previous index”
  - No hay filtros por metadata (p.ej. source)
- Retrieval pobre
  - k demasiado bajo y sin MMR
  - No hay query expansion / no hay normalization
  - No hay rerank (opcional) o score threshold
- Grounding ausente
  - La respuesta no trae citas ni evidencia
  - Prompt no fuerza “si no hay evidencia -> no sé”

### Requisitos funcionales (RF)

- RF-01: Ingesta de documentos desde `docs/datasets/*` con metadata completa (doc_id, source, page, section, chunk_id).
- RF-02: Indexación idempotente: ejecutar `ingest.py` dos veces no duplica embeddings.
- RF-03: Retrieval retorna chunks con score y metadata; soporta filtros (por source, por doc_id).
- RF-04: Respuesta final incluye citas (lista de chunk_ids o (source,page)).
- RF-05: Si la evidencia no alcanza un umbral, el sistema debe responder “insuficiente evidencia” (no inventar).

### Requisitos no funcionales (RNF)

- RNF-01: Tiempo de respuesta < 2.5s en dataset chico (sin LLM pesado en rerank; si hay rerank, justificar tradeoff).
- RNF-02: Cobertura de tests mínima: retrieval + grounding.
- RNF-03: Logging estructurado por request_id.

### Criterios de aceptación (CA)

- CA-01: `pytest` pasa.
- CA-02: `make eval PROJECT=01` produce métricas > umbral (ej: `citation_coverage >= 0.7`, `hallucination_rate <= 0.1`).
- CA-03: Re-ingesta no incrementa cantidad de vectores.

## Proyecto 02: 02_agent_router_langgraph (LangGraph agent + tools + state)

### Propósito de evaluación

- Diseñar un router de herramientas robusto
- Entender state machine, memory, tool schemas, error handling
- Evitar tool spam / loops / tool misuse

### Componentes

```
02_agent_router_langgraph/
  README.md
  graph.py
  state.py
  tools/
    weather.py
    finance.py
    docs_search.py          # usa vectorstore del proyecto 01 o mock
  policies.py              # guardrails simples
  tests/
    test_routing.py
    test_tool_errors.py
```

### Bugs/diseños intencionalmente malos

- Router frágil
  - Clasificación por prompt naive que confunde intents
  - No valida tool inputs (pydantic)
  - No hay “fallback to ask clarification” (pero en entrevista no se pregunta al usuario; se decide estrategia)
- Loops
  - Graph vuelve a “plan” infinitamente si tool devuelve vacío
  - No hay contador de steps / no hay stop condition
- State mal modelado
  - Mezcla mensajes, resultados de tools, y decisiones sin tipado
  - No persiste “tool inventory” ni capabilities

### Requisitos funcionales

- RF-10: LangGraph con nodos: route -> call_tool -> synthesize -> done.
- RF-11: Tools con schema estricto (pydantic) y validación.
- RF-12: Stop conditions: max_steps, no-evidence, tool-error fallback.
- RF-13: El agente debe devolver salida con:
  - decisión (qué tool llamó y por qué, breve)
  - resultado
  - evidencia (si aplica)

### Requisitos no funcionales (RNF)

- RNF-10: Determinismo parcial: con seed o “fixed prompts” los tests no flakean.
- RNF-11: Trazas/telemetría stubs listos (hooks).

### Criterios de aceptación

- CA-10: `test_routing.py` cubre 6–10 prompts; el router elige tool correcto.
- CA-11: `test_tool_errors.py` demuestra manejo de error sin loop.

## Proyecto 03: 03_prod_ready_observability (producción: tracing, retries, caching, eval)

### Propósito de evaluación

- Convertir un prototipo a algo “deployable”
- Añadir observabilidad, control de costos, robustez
- Diseñar límites operativos (timeouts, retries, circuit breaker simple)

### Componentes

```
03_prod_ready_observability/
  README.md
  service/
    app.py                  # FastAPI
    endpoints.py            # /ask, /health, /metrics
    deps.py                 # inject llm, vectorstore, cache
  infra/
    docker-compose.yml
  reliability/
    retry.py
    timeouts.py
    cache.py                # redis opcional o in-memory LRU
  eval/
    regression_suite.yaml
  tests/
    test_api.py
    test_retry_policy.py
```

### Bugs/diseños intencionalmente malos

- Retries indiscriminados (duplica costo)
- Timeouts inexistentes
- No hay request_id ni correlación de logs
- No hay cache de embeddings / results
- No hay budgets por request

### Requisitos funcionales

- RF-20: Endpoint `/ask` con request/response models.
- RF-21: Middleware de request_id + logs estructurados.
- RF-22: Retry policy: solo en errores transitorios; backoff; límite.
- RF-23: Cache: al menos cache de embeddings o cache de respuestas por query+filters.
- RF-24: Regression suite: set de preguntas que no deben degradar.

### Requisitos no funcionales (RNF)

- RNF-20: No duplicar llamadas al LLM por defecto.
- RNF-21: Métricas mínimas: latency, llm_calls, token_estimate, retrieval_k.
- RNF-22: Docker runnable local.

### Criterios de aceptación

- CA-20: `test_api.py` pasa; `/health` responde.
- CA-21: Logs incluyen `request_id` en cada línea.
- CA-22: `regression_suite` muestra “no regression” vs baseline.

## Proyecto 04: 04_graph_rag_diagnostics (GraphRAG + diagnósticos complejos)

### Skill focus (qué evalúa)

- Graph-based retrieval (GraphRAG / KG-RAG)
- Multi-step reasoning sobre datos técnicos
- Diagnóstico complejo (procedures, parts, troubleshooting)
- Tradeoff vector search vs graph traversal
- Diseño de retrieval híbrido (vector + graph)

### Contexto funcional (para el candidato)

Sistema de soporte técnico que debe responder preguntas tipo:

- “¿Qué procedimiento seguir si el error E42 aparece después de reemplazar el módulo X?”
- “¿Qué piezas están comúnmente asociadas a este fallo y en qué orden se revisan?”
- “¿Qué pasos previos invalidan este diagnóstico?”

Estas preguntas no se resuelven con top-k vector search.

### Estructura

```
04_graph_rag_diagnostics/
  README.md
  ingest/
    extract_entities.py        # entities, relations (procedures, parts, faults)
    build_graph.py             # KG builder (networkx / neo4j mock)
  retrieval/
    vector_retriever.py
    graph_retriever.py         # BFS / constrained traversal
    hybrid_retriever.py        # vector → graph expansion
  reasoning/
    planner.py                 # multi-step plan (LLM-assisted or rule-based)
  answer/
    synthesizer.py
    confidence.py
  tests/
    test_graph_queries.py
    test_hybrid_retrieval.py
```

### Fallas intencionales (NO documentadas en README del candidato)

- El graph está construido pero no se usa en retrieval
- Traversal sin límites → explosión combinatoria
- No hay scoring entre paths
- El planner no explica pasos
- Respuestas correctas pero no justificadas

### Requisitos funcionales (RF)

- RF-30: Construir un knowledge graph con nodos: Procedure, Part, Fault, Symptom
- RF-31: Implementar retrieval híbrido:
  - Paso 1: vector search (seed nodes)
  - Paso 2: graph traversal (bounded, typed edges)
- RF-32: Soportar preguntas multi-step (orden temporal / dependencia)
- RF-33: La respuesta debe incluir:
  - pasos de razonamiento
  - nodos del grafo utilizados
  - evidencia documental

### Requisitos no funcionales (RNF)

- RNF-30: Límite explícito de hops y branching factor
- RNF-31: Determinismo en traversal (tests reproducibles)
- RNF-32: Logging del path de reasoning

### Criterios de aceptación

- CA-30: `test_graph_queries.py` valida preguntas no resolubles con vector-only
- CA-31: El sistema explica por qué llega a una conclusión
- CA-32: No hay loops ni explosión de nodos

## Proyecto 05: 05_multimodal_validation_feedback (multimodal + validación + feedback)

### Skill focus

- Multimodal ingestion (PDFs, imágenes, esquemas)
- Content synthesis para training data
- Validation workflows
- Confidence scoring
- Feedback loop con datos reales
- Hallucination control + scope enforcement

### Contexto funcional

Sistema que transforma documentación técnica real (manuales, fotos, diagramas) en:

- Respuestas para técnicos
- Contenido validado para entrenamiento
- Señales de confianza basadas en evidencia

### Estructura

```
05_multimodal_validation_feedback/
  README.md
  ingest/
    pdf_ingest.py
    image_ingest.py            # OCR / vision model stub
    multimodal_normalizer.py
  synthesis/
    content_generator.py       # Q/A, procedures, summaries
  validation/
    validators.py              # rule-based + LLM judge
    confidence_scoring.py
  feedback/
    feedback_store.py          # simulated repair outcomes
    retraining_selector.py
  api/
    service.py
  tests/
    test_validation.py
    test_confidence.py
```

### Fallas intencionales

- Multimodal data se mezcla sin normalización
- El sistema genera contenido sin validarlo
- Confidence score es fake (hardcoded)
- Feedback existe pero no influye en nada
- El sistema responde incluso cuando la confianza es baja

### Requisitos funcionales

- RF-40: Ingestar y normalizar texto + imágenes + metadata
- RF-41: Generar contenido estructurado (procedures, Q/A)
- RF-42: Validar outputs usando:
  - reglas (coverage, citations)
  - LLM-based judge (stub)
- RF-43: Calcular confidence score trazable
- RF-44: Bloquear o degradar respuestas con baja confianza
- RF-45: Usar feedback histórico para ajustar scoring o retrieval

### Requisitos no funcionales (RNF)

- RNF-40: Separación clara entre generación y validación
- RNF-41: Determinismo en validation tests
- RNF-42: Auditable (por qué se aceptó o rechazó una respuesta)

### Criterios de aceptación

- CA-40: Ninguna respuesta “final” sale sin validation
- CA-41: Confidence score correlaciona con evidencia real
- CA-42: Feedback modifica comportamiento futuro (aunque sea simple)

## Guía del entrevistador y rubric (docs/)

- `docs/interview_guide.md` (flujo)
  - Setup (5 min): correr tests / reproducir bug
  - Diagnóstico (10 min): explicar hipótesis
  - Fix incremental (20–30 min): arreglos + tests
  - Tradeoffs (10 min): justificar decisiones
- `docs/scoring_rubric.md` (puntaje)
  - Diagnosis (reproduce, identifica causa raíz)
  - Correctness (fix real, tests)
  - RAG craft (chunking, metadata, retrieval strategy)
  - Agent craft (state, tools, stop conditions)
  - Production thinking (timeouts, retries, logging, eval, cost)
  - Comunicación técnica (precisa, decisiones explícitas)

## Mapeo explícito a responsabilidades del rol

This repository evaluates the same skills required to:

- build intelligent retrieval systems
- design RAG and GraphRAG pipelines
- validate and ground AI outputs
- deploy reliable, cost-aware AI systems
- collaborate with product on real constraints

## Instrucción final al equipo dev

- No simplificar.
- No “educar”.
- El código debe parecer real, no demo.
- Cada proyecto debe fallar de manera interesante.
- Cada fix debe revelar si el candidato piensa como ingeniero de sistemas AI, no como usuario de frameworks.

Este repo, bien ejecutado, filtra seniority real en 45–60 minutos.
