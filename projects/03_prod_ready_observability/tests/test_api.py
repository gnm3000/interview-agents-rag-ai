from fastapi.testclient import TestClient

from service.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cache_flow():
    response = client.get("/ask", params={"query": "hello"})
    assert response.status_code == 200
    assert response.json()["cached"] is False

    response = client.get("/ask", params={"query": "hello"})
    assert response.status_code == 200
    assert response.json()["cached"] is True
