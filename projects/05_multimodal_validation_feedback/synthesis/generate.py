from __future__ import annotations

from typing import Dict, List


def generate_qa(content: str) -> List[Dict[str, str]]:
    """Generate a simple Q/A structure from content.

    Candidates can swap this with an LLM-backed generator.
    """
    sentences = [line.strip() for line in content.split(".") if line.strip()]
    return [
        {"question": f"What about: {sentence}?", "answer": sentence}
        for sentence in sentences[:5]
    ]
