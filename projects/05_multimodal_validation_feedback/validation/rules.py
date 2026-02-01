from __future__ import annotations

from typing import Dict


def rule_based_validate(item: Dict[str, str]) -> Dict[str, float]:
    question = item.get("question", "")
    answer = item.get("answer", "")
    score = 1.0 if question and answer else 0.0
    if len(answer) < 5:
        score *= 0.5
    return {"score": score}
