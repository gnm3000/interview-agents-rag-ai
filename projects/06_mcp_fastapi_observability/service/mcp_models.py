from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TenantContext(BaseModel):
    tenant_id: str = Field(..., description="Tenant identifier")
    request_id: str = Field(..., description="Request identifier")
    trace_id: Optional[str] = Field(None, description="Trace identifier")


class MCPInitializeRequest(BaseModel):
    client_name: str
    client_version: str
    context: TenantContext


class MCPCapabilities(BaseModel):
    resources: bool
    tools: bool
    prompts: bool
    sampling: bool


class MCPInitializeResponse(BaseModel):
    server_name: str
    server_version: str
    protocol_version: str
    capabilities: MCPCapabilities


class MCPResource(BaseModel):
    id: str
    name: str
    description: str
    mime_type: str
    version: str
    tags: List[str]


class MCPResourceListRequest(BaseModel):
    cursor: Optional[str] = None
    limit: int = Field(10, ge=1, le=100)
    tags: Optional[List[str]] = None
    context: TenantContext


class MCPResourceListResponse(BaseModel):
    items: List[MCPResource]
    next_cursor: Optional[str]


class MCPTool(BaseModel):
    id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    version: str


class MCPToolCallRequest(BaseModel):
    tool_id: str
    input: Dict[str, Any]
    context: TenantContext


class MCPToolCallResponse(BaseModel):
    tool_id: str
    output: Dict[str, Any]
    status: str


class MCPPrompt(BaseModel):
    id: str
    name: str
    description: str
    template: str
    version: str


class MCPPromptListRequest(BaseModel):
    context: TenantContext


class MCPPromptListResponse(BaseModel):
    items: List[MCPPrompt]


class MCPSamplingLimitsResponse(BaseModel):
    tenant_id: str
    limits: Dict[str, int]
