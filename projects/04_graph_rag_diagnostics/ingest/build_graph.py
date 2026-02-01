from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Tuple

import networkx as nx

RELATION_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"(.+?) connects to (.+?)\.", "connects_to"),
    (r"(.+?) depends on (.+?)\.", "depends_on"),
    (r"(.+?) has owner (.+?)\.", "owned_by"),
    (r"(.+?) is maintained by (.+?)\.", "maintained_by"),
)


def extract_relations(text: str) -> Iterable[Tuple[str, str, str]]:
    for pattern, relation in RELATION_PATTERNS:
        for match in re.finditer(pattern, text):
            left, right = match.group(1).strip(), match.group(2).strip()
            yield left, relation, right


def build_graph_from_files(paths: Iterable[Path]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for path in paths:
        text = path.read_text()
        for source, relation, target in extract_relations(text):
            graph.add_node(source)
            graph.add_node(target)
            graph.add_edge(source, target, relation=relation, source_file=str(path))
    return graph
