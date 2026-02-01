from __future__ import annotations

from typing import List, Tuple

import networkx as nx


def graph_neighbors(graph: nx.DiGraph, node: str, depth: int = 1) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    if node not in graph:
        return results
    for neighbor in graph.successors(node):
        relation = graph.edges[node, neighbor].get("relation", "related")
        results.append((neighbor, relation))
        if depth > 1:
            results.extend(graph_neighbors(graph, neighbor, depth - 1))
    return results
