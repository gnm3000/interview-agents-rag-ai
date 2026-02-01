from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from feedback.store import save_feedback
from synthesis.generate import generate_qa
from validation.judge import llm_judge
from validation.rules import rule_based_validate

app = FastAPI(title="Multimodal Validation")


class ContentRequest(BaseModel):
    content: str


@app.post("/validate")
async def validate(request: ContentRequest):
    qa_items = generate_qa(request.content)
    validated = []
    for item in qa_items:
        rules = rule_based_validate(item)
        judge = llm_judge(item)
        score = (rules["score"] + judge["score"]) / 2
        validated.append({**item, "score": score})
    return {"items": validated}


@app.post("/feedback")
async def feedback(request: ContentRequest):
    qa_items = generate_qa(request.content)
    enriched = [{**item, "score": 0.5} for item in qa_items]
    save_feedback(enriched)
    return {"stored": len(enriched)}
