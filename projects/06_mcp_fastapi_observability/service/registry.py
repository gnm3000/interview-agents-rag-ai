import json
from pathlib import Path
from typing import Dict, List, Optional

from .mcp_models import MCPPrompt, MCPResource, MCPTool

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_catalog.json"


class MCPRegistry:
    def __init__(self) -> None:
        self._resources: List[MCPResource] = []
        self._tools: Dict[str, MCPTool] = {}
        self._prompts: List[MCPPrompt] = []

    def load(self) -> None:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self._resources = [MCPResource(**item) for item in catalog.get("resources", [])]
        self._tools = {item["id"]: MCPTool(**item) for item in catalog.get("tools", [])}
        self._prompts = [MCPPrompt(**item) for item in catalog.get("prompts", [])]

    def list_resources(self, tags: Optional[List[str]] = None) -> List[MCPResource]:
        if not tags:
            return list(self._resources)
        return [resource for resource in self._resources if set(tags).issubset(resource.tags)]

    def list_prompts(self) -> List[MCPPrompt]:
        return list(self._prompts)

    def get_tool(self, tool_id: str) -> Optional[MCPTool]:
        return self._tools.get(tool_id)
