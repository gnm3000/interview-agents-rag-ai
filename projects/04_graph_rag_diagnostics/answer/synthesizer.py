from __future__ import annotations

from typing import Iterable


def synthesize_answer(question: str, evidence: Iterable[str]) -> str:
    evidence_list = list(evidence)
    if not evidence_list:
        return "No evidence found to answer the question."
    evidence_block = "\n".join(f"- {item}" for item in evidence_list)
    return f"Question: {question}\nEvidence:\n{evidence_block}"
