from __future__ import annotations

import httpx


def run_regression(base_url: str = "http://localhost:8000") -> None:
    queries = ["hola", "status", "cache"]
    with httpx.Client() as client:
        for query in queries:
            response = client.get(f"{base_url}/ask", params={"query": query})
            response.raise_for_status()
            print(query, response.json())


if __name__ == "__main__":
    run_regression()
