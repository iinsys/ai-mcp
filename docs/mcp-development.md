# MCP Development Guide

A comprehensive guide to developing Model Context Protocol (MCP) servers and clients.

## What is MCP?

Model Context Protocol (MCP) is an open standard for connecting AI assistants to external data sources and tools. It enables secure, controlled access to local and remote resources.

## Key Concepts

### Servers
MCP servers provide tools and resources that clients can access. They run as separate processes and communicate via JSON-RPC.

### Clients
MCP clients (like Kiro, Claude Desktop, etc.) connect to servers to access their capabilities.

### Tools
Functions that clients can call to perform actions or retrieve information.

### Resources
Static or dynamic content that clients can read (files, API responses, etc.).

## Creating Your First MCP Server

### 1. Setup

Start with the template:
```bash
cp -r mcp-servers/template mcp-servers/my-server
cd mcp-servers/my-server
```

### 2. Basic Structure

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="my_tool",
            description="Description of what this tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Parameter description"}
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "my_tool":
        param = arguments.get("param")
        result = f"Processed: {param}"
        return CallToolResult(
            content=[TextContent(type="text", text=result)]
        )
```

### 3. Adding Resources

```python
@server.list_resources()
async def handle_list_resources():
    return [
        Resource(
            uri="my-server://data",
            name="My Data",
            description="Some useful data",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str):
    if uri == "my-server://data":
        data = {"key": "value", "items": [1, 2, 3]}
        return ReadResourceResult(
            contents=[TextContent(type="text", text=json.dumps(data, indent=2))]
        )
```

## Best Practices

### Error Handling
Always wrap your tool and resource handlers in try-catch blocks:

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    try:
        # Your tool logic here
        pass
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )
```

### Input Validation
Use Pydantic models for robust input validation:

```python
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param: str = Field(..., description="Required parameter")
    optional_param: int = Field(default=10, description="Optional parameter")

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "my_tool":
        try:
            input_data = MyToolInput(**arguments)
            # Use input_data.param, input_data.optional_param
        except ValidationError as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid input: {e}")]
            )
```

### Logging
Use structured logging for better debugging:

```python
import logging

logger = logging.getLogger(__name__)

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name} with args: {arguments}")
    # Tool logic here
```

## Testing Your Server

### Manual Testing
```bash
# Run your server
python server.py

# Test with the example client
python ../../examples/basic/simple-mcp-client.py
```

### Unit Testing
```python
import pytest
from your_server import server

@pytest.mark.asyncio
async def test_my_tool():
    result = await server.call_tool("my_tool", {"param": "test"})
    assert "test" in result.content[0].text
```

## Deployment

### Local Development
Use the server directly with Python:
```json
{
  "command": "python",
  "args": ["path/to/server.py"]
}
```

### Production with uvx
Package your server and use uvx:
```json
{
  "command": "uvx",
  "args": ["your-mcp-server-package"]
}
```

## Common Patterns

### Database Integration
```python
import sqlite3

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "query_db":
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        # Execute query safely
        cursor.execute("SELECT * FROM table WHERE id = ?", (arguments["id"],))
        results = cursor.fetchall()
        conn.close()
        return CallToolResult(
            content=[TextContent(type="text", text=str(results))]
        )
```

### API Integration
```python
import httpx

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "fetch_data":
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/data/{arguments['id']}")
            return CallToolResult(
                content=[TextContent(type="text", text=response.text)]
            )
```

## Troubleshooting

### Common Issues

1. **Server won't start**: Check Python path and dependencies
2. **Tools not appearing**: Verify `list_tools()` handler is registered
3. **Permission errors**: Check file permissions and paths
4. **JSON-RPC errors**: Validate input schemas and error handling

### Debugging Tips

- Use `logger.debug()` for detailed tracing
- Test tools individually before integration
- Validate JSON schemas with online tools
- Check MCP client logs for connection issues

## Next Steps

- Explore the [examples](../examples/) directory
- Check out [community MCP servers](../resources/awesome-mcp-servers.md)
- Join the [MCP community discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)