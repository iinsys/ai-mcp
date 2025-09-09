#!/usr/bin/env python3
"""
MCP Server Template

A basic template for creating MCP servers with example tools and resources.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server instance
server = Server("template-server")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back the provided text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back",
                    }
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="calculate",
            description="Perform basic arithmetic calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2')",
                    }
                },
                "required": ["expression"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "echo":
            text = arguments.get("text", "")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Echo: {text}")]
            )
        
        elif name == "calculate":
            expression = arguments.get("expression", "")
            # Simple evaluation - in production, use a safer approach
            try:
                result = eval(expression)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Result: {result}")]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    
    except Exception as e:
        logger.error(f"Error in tool call {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="template://info",
            name="Server Information",
            description="Information about this template server",
            mimeType="text/plain",
        ),
        Resource(
            uri="template://help",
            name="Help Documentation",
            description="Help and usage information",
            mimeType="text/markdown",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> ReadResourceResult:
    """Handle resource reading."""
    try:
        if uri == "template://info":
            info = """
MCP Server Template
==================

This is a template MCP server that demonstrates:
- Basic tool implementation
- Resource handling
- Error management
- Logging and debugging

Version: 1.0.0
Author: Template Author
"""
            return ReadResourceResult(
                contents=[TextContent(type="text", text=info)]
            )
        
        elif uri == "template://help":
            help_text = """
# MCP Server Template Help

## Available Tools

### echo
Echo back the provided text.

**Parameters:**
- `text` (string): Text to echo back

**Example:**
```json
{
  "text": "Hello, World!"
}
```

### calculate
Perform basic arithmetic calculations.

**Parameters:**
- `expression` (string): Mathematical expression to evaluate

**Example:**
```json
{
  "expression": "2 + 2 * 3"
}
```

## Available Resources

- `template://info` - Server information
- `template://help` - This help documentation

## Usage

Configure this server in your MCP client and start using the tools and resources.
"""
            return ReadResourceResult(
                contents=[TextContent(type="text", text=help_text)]
            )
        
        else:
            return ReadResourceResult(
                contents=[TextContent(type="text", text=f"Resource not found: {uri}")]
            )
    
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return ReadResourceResult(
            contents=[TextContent(type="text", text=f"Error: {str(e)}")]
        )


async def main():
    """Main server entry point."""
    # Initialize server with stdio transport
    async with server.run_stdio() as streams:
        await server.run(
            streams[0], streams[1], InitializationOptions(
                server_name="template-server",
                server_version="1.0.0",
            )
        )


if __name__ == "__main__":
    asyncio.run(main())