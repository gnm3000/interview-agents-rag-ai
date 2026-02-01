from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in text.split()]


@dataclass
class VectorIndex:
    documents: List[str]

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        query_tokens = set(tokenize(query))
        scored = []
        for doc in self.documents:
            tokens = set(tokenize(doc))
            overlap = len(tokens & query_tokens)
            score = overlap / max(len(tokens), 1)
            scored.append((doc, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:k]


def build_index(texts: Iterable[str]) -> VectorIndex:
    return VectorIndex(list(texts))
