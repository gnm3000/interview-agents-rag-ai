from fastapi.testclient import TestClient

from api.main import app
from validation.rules import rule_based_validate


client = TestClient(app)


def test_rule_based_validation():
    result = rule_based_validate({"question": "Q", "answer": "Answer"})
    assert result["score"] > 0


def test_validate_endpoint():
    response = client.post("/validate", json={"content": "Paso 1. Paso 2."})
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
