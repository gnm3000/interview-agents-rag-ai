from __future__ import annotations

from typing import List


def plan_steps(question: str) -> List[str]:
    """Naive planner used for diagnostics."""
    steps = ["identify_entities", "retrieve_graph", "retrieve_vector", "synthesize"]
    if "owner" in question.lower():
        steps.insert(1, "focus_on_ownership")
    return steps
