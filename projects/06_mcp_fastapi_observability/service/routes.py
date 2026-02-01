from typing import List, Optional

from fastapi import APIRouter, HTTPException

from .mcp_models import (
    MCPInitializeRequest,
    MCPInitializeResponse,
    MCPCapabilities,
    MCPPromptListRequest,
    MCPPromptListResponse,
    MCPResourceListRequest,
    MCPResourceListResponse,
    MCPToolCallRequest,
    MCPToolCallResponse,
    MCPSamplingLimitsResponse,
)
from .observability import log_event
from .policies import get_limits
from .registry import MCPRegistry

router = APIRouter()
registry = MCPRegistry()
registry.load()


@router.post("/mcp/initialize", response_model=MCPInitializeResponse)
def initialize(request: MCPInitializeRequest) -> MCPInitializeResponse:
    log_event(
        "initialize",
        {
            "client_name": request.client_name,
            "client_version": request.client_version,
            "tenant_id": request.context.tenant_id,
            "request_id": request.context.request_id,
        },
    )
    return MCPInitializeResponse(
        server_name="mcp-hub",
        server_version="0.1.0",
        protocol_version="2024-10-07",
        capabilities=MCPCapabilities(
            resources=True,
            tools=True,
            prompts=False,
            sampling=False,
        ),
    )


@router.post("/mcp/resources/list", response_model=MCPResourceListResponse)
def list_resources(request: MCPResourceListRequest) -> MCPResourceListResponse:
    log_event(
        "resources.list",
        {
            "tenant_id": request.context.tenant_id,
            "request_id": request.context.request_id,
            "cursor": request.cursor,
            "limit": request.limit,
        },
    )
    resources = registry.list_resources(tags=request.tags)
    start = int(request.cursor or 0)
    end = start + request.limit
    items = resources[start:end]
    next_cursor = str(end) if end < len(resources) else None
    return MCPResourceListResponse(items=items, next_cursor=next_cursor)


@router.post("/mcp/tools/call", response_model=MCPToolCallResponse)
def call_tool(request: MCPToolCallRequest) -> MCPToolCallResponse:
    tool = registry.get_tool(request.tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    log_event(
        "tools.call",
        {
            "tenant_id": request.context.tenant_id,
            "request_id": request.context.request_id,
            "tool_id": request.tool_id,
            "input": request.input,
        },
    )

    return MCPToolCallResponse(
        tool_id=request.tool_id,
        status="ok",
        output={"message": "tool executed", "echo": request.input},
    )


@router.post("/mcp/prompts/list", response_model=MCPPromptListResponse)
def list_prompts(request: MCPPromptListRequest) -> MCPPromptListResponse:
    log_event(
        "prompts.list",
        {
            "tenant_id": request.context.tenant_id,
            "request_id": request.context.request_id,
        },
    )
    return MCPPromptListResponse(items=registry.list_prompts())


@router.get("/mcp/sampling/limits", response_model=MCPSamplingLimitsResponse)
def sampling_limits(tenant_id: str) -> MCPSamplingLimitsResponse:
    limits = get_limits(tenant_id)
    log_event("sampling.limits", {"tenant_id": tenant_id})
    return MCPSamplingLimitsResponse(tenant_id=tenant_id, limits=limits)
