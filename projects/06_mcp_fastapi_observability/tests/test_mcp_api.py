from fastapi.testclient import TestClient

from service.main import app


client = TestClient(app)


def test_initialize_returns_capabilities():
    response = client.post(
        "/mcp/initialize",
        json={
            "client_name": "interview-suite",
            "client_version": "0.1",
            "context": {
                "tenant_id": "default",
                "request_id": "req-1",
                "trace_id": "trace-1",
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["server_name"] == "mcp-hub"
    assert "capabilities" in payload


def test_resources_list_paginates():
    response = client.post(
        "/mcp/resources/list",
        json={
            "cursor": None,
            "limit": 1,
            "tags": None,
            "context": {
                "tenant_id": "default",
                "request_id": "req-2",
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 1
    assert payload["next_cursor"] is not None


def test_tool_call_unknown_tool():
    response = client.post(
        "/mcp/tools/call",
        json={
            "tool_id": "missing",
            "input": {},
            "context": {
                "tenant_id": "default",
                "request_id": "req-3",
            },
        },
    )
    assert response.status_code == 404
