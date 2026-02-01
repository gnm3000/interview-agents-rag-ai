from __future__ import annotations

from typing import List

from retrieval.graph import graph_neighbors
from retrieval.vector import VectorIndex


def hybrid_search(index: VectorIndex, graph, query: str, seed: str) -> List[str]:
    vector_hits = [doc for doc, score in index.search(query) if score > 0]
    graph_hits = [f"{seed} -> {node} ({relation})" for node, relation in graph_neighbors(graph, seed)]
    return vector_hits + graph_hits
