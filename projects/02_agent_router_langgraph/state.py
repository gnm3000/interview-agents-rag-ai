from __future__ import annotations

from typing import List, Literal, Optional, TypedDict


class ToolResult(TypedDict):
    tool: str
    output: str


class AgentState(TypedDict):
    query: str
    route: Optional[Literal["weather", "finance", "docs_search", "fallback"]]
    tool_result: Optional[ToolResult]
    answer: Optional[str]
    messages: List[str]
