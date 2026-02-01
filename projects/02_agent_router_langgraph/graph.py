from __future__ import annotations

from langgraph.graph import END, StateGraph

from policies import enforce_route
from state import AgentState
from tools.docs_search import DocsSearchInput, run_docs_search
from tools.finance import FinanceInput, run_finance
from tools.weather import WeatherInput, run_weather


def route(state: AgentState) -> AgentState:
    query = state["query"].lower()
    if "weather" in query or "clima" in query:
        route_name = "weather"
    elif "stock" in query or "precio" in query or "ticker" in query:
        route_name = "finance"
    elif "doc" in query or "manual" in query or "policy" in query:
        route_name = "docs_search"
    else:
        route_name = "fallback"
    state["route"] = enforce_route(route_name)
    state.setdefault("messages", []).append(f"route={state['route']}")
    return state


def call_tool(state: AgentState) -> AgentState:
    route_name = state.get("route")
    if route_name == "weather":
        output = run_weather(WeatherInput(city=state["query"]))
    elif route_name == "finance":
        output = run_finance(FinanceInput(ticker=state["query"]))
    elif route_name == "docs_search":
        output = run_docs_search(DocsSearchInput(query=state["query"]))
    else:
        output = "No tool matched."
    state["tool_result"] = {"tool": route_name or "fallback", "output": output}
    return state


def synthesize(state: AgentState) -> AgentState:
    tool_result = state.get("tool_result")
    if tool_result:
        state["answer"] = f"{tool_result['output']}"
    else:
        state["answer"] = "I could not find a tool for that request."
    state.setdefault("messages", []).append("synthesize")
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("route", route)
    graph.add_node("call_tool", call_tool)
    graph.add_node("synthesize", synthesize)

    graph.set_entry_point("route")
    graph.add_edge("route", "call_tool")
    graph.add_edge("call_tool", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()
