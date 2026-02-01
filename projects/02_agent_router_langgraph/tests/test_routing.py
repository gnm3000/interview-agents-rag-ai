from graph import build_graph


def test_weather_route():
    graph = build_graph()
    result = graph.invoke({"query": "weather in Lima", "messages": []})
    assert result["route"] == "weather"
    assert "Sunny" in result["answer"]


def test_finance_route():
    graph = build_graph()
    result = graph.invoke({"query": "ticker AAPL", "messages": []})
    assert result["route"] == "finance"
    assert "closed" in result["answer"]


def test_docs_route():
    graph = build_graph()
    result = graph.invoke({"query": "docs policy", "messages": []})
    assert result["route"] == "docs_search"
    assert "Found docs" in result["answer"]
