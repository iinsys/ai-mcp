# Client Integration - Connect to MCP Servers

Learn how to build MCP clients and integrate MCP servers into your applications.

## What You'll Learn

- How to create MCP clients from scratch
- Different ways to connect to MCP servers
- Integration patterns for various use cases
- Best practices for client development
- Error handling and connection management

## Prerequisites

- Completed [MCP Basics](../mcp-basics/) and [Your First Server](../first-server/)
- Python 3.8+ installed
- Basic understanding of async programming

## Understanding MCP Clients

### What is an MCP Client?

An MCP client is any application that connects to MCP servers to access their tools and resources. Examples include:

- **AI Assistants**: Claude Desktop, Kiro IDE
- **Custom Applications**: Your own apps that need MCP functionality
- **CLI Tools**: Command-line utilities
- **Web Applications**: Browser-based tools
- **Scripts**: Automation and integration scripts

### Client Responsibilities

1. **Connection Management**: Establish and maintain server connections
2. **Protocol Handling**: Send/receive MCP messages correctly
3. **Error Management**: Handle failures gracefully
4. **Security**: Validate server responses and manage permissions
5. **User Interface**: Present tools and resources to users

## Basic Client Implementation

### Step 1: Simple Client Structure

Create `basic_client.py`:

```python
#!/usr/bin/env python3
"""
Basic MCP Client Example

Shows how to connect to and interact with MCP servers.
"""

import asyncio
import logging
from typing import Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.types import CallToolResult, ReadResourceResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    """A basic MCP client."""
    
    def __init__(self, server_command: str, server_args: List[str]):
        self.server_params = StdioServerParameters(
            command=server_command,
            args=server_args
        )
        self.session: Optional[ClientSession] = None
    
    async def connect(self) -> None:
        """Connect to the MCP server."""
        try:
            self.session = ClientSession(self.server_params)
            await self.session.__aenter__()
            await self.session.initialize()
            logger.info("Connected to MCP server successfully")
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
                logger.info("Disconnected from MCP server")
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")
    
    async def list_tools(self) -> List[str]:
        """Get list of available tools."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            tools_response = await self.session.list_tools()
            return [tool.name for tool in tools_response.tools]
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict) -> Optional[str]:
        """Call a tool and return the result."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            result = await self.session.call_tool(name, arguments)
            if result.content:
                return result.content[0].text
            return None
        except Exception as e:
            logger.error(f"Failed to call tool {name}: {e}")
            return None
    
    async def list_resources(self) -> List[str]:
        """Get list of available resources."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            resources_response = await self.session.list_resources()
            return [resource.uri for resource in resources_response.resources]
        except Exception as e:
            logger.error(f"Failed to list resources: {e}")
            return []
    
    async def read_resource(self, uri: str) -> Optional[str]:
        """Read a resource and return its content."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        try:
            result = await self.session.read_resource(uri)
            if result.contents:
                return result.contents[0].text
            return None
        except Exception as e:
            logger.error(f"Failed to read resource {uri}: {e}")
            return None

# Example usage
async def main():
    """Example client usage."""
    client = MCPClient("python", ["../first-server/src/server.py"])
    
    try:
        # Connect to server
        await client.connect()
        
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call a tool
        result = await client.call_tool("calculate", {"expression": "5 * 8"})
        print(f"Calculation result: {result}")
        
        # List resources
        resources = await client.list_resources()
        print(f"Available resources: {resources}")
        
        # Read a resource
        if resources:
            content = await client.read_resource(resources[0])
            print(f"Resource content: {content}")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Client Patterns

### Step 2: Connection Pool Client

For applications that need to connect to multiple servers:

```python
import asyncio
from typing import Dict, List
from contextlib import asynccontextmanager

class MCPConnectionPool:
    """Manages connections to multiple MCP servers."""
    
    def __init__(self):
        self.connections: Dict[str, MCPClient] = {}
    
    async def add_server(self, name: str, command: str, args: List[str]) -> None:
        """Add a server to the pool."""
        client = MCPClient(command, args)
        await client.connect()
        self.connections[name] = client
        logger.info(f"Added server '{name}' to pool")
    
    async def remove_server(self, name: str) -> None:
        """Remove a server from the pool."""
        if name in self.connections:
            await self.connections[name].disconnect()
            del self.connections[name]
            logger.info(f"Removed server '{name}' from pool")
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Optional[str]:
        """Call a tool on a specific server."""
        if server_name not in self.connections:
            raise ValueError(f"Server '{server_name}' not found in pool")
        
        return await self.connections[server_name].call_tool(tool_name, arguments)
    
    async def broadcast_tool_call(self, tool_name: str, arguments: Dict) -> Dict[str, Optional[str]]:
        """Call a tool on all servers that have it."""
        results = {}
        
        for server_name, client in self.connections.items():
            try:
                tools = await client.list_tools()
                if tool_name in tools:
                    result = await client.call_tool(tool_name, arguments)
                    results[server_name] = result
            except Exception as e:
                logger.error(f"Error calling {tool_name} on {server_name}: {e}")
                results[server_name] = None
        
        return results
    
    async def close_all(self) -> None:
        """Close all connections."""
        for name in list(self.connections.keys()):
            await self.remove_server(name)

# Example usage
async def pool_example():
    """Example using connection pool."""
    pool = MCPConnectionPool()
    
    try:
        # Add multiple servers
        await pool.add_server("assistant", "python", ["../first-server/src/server.py"])
        await pool.add_server("weather", "uvx", ["weather-mcp-server"])
        
        # Call tool on specific server
        result = await pool.call_tool("assistant", "calculate", {"expression": "10 + 5"})
        print(f"Assistant calculation: {result}")
        
        # Broadcast to all servers
        results = await pool.broadcast_tool_call("get_info", {})
        print(f"Broadcast results: {results}")
    
    finally:
        await pool.close_all()
```

### Step 3: Reactive Client with Events

For applications that need to respond to server changes:

```python
import asyncio
from typing import Callable, Dict, Any
from dataclasses import dataclass

@dataclass
class MCPEvent:
    """Represents an MCP-related event."""
    event_type: str
    server_name: str
    data: Dict[str, Any]

class ReactiveClient(MCPClient):
    """MCP client with event handling capabilities."""
    
    def __init__(self, server_name: str, server_command: str, server_args: List[str]):
        super().__init__(server_command, server_args)
        self.server_name = server_name
        self.event_handlers: Dict[str, List[Callable]] = {}
    
    def on(self, event_type: str, handler: Callable[[MCPEvent], None]) -> None:
        """Register an event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit an event to all registered handlers."""
        event = MCPEvent(event_type, self.server_name, data)
        
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
    
    async def call_tool(self, name: str, arguments: Dict) -> Optional[str]:
        """Call tool with event emission."""
        self.emit("tool_call_start", {"tool": name, "arguments": arguments})
        
        try:
            result = await super().call_tool(name, arguments)
            self.emit("tool_call_success", {"tool": name, "result": result})
            return result
        except Exception as e:
            self.emit("tool_call_error", {"tool": name, "error": str(e)})
            raise

# Example event handlers
def on_tool_call(event: MCPEvent) -> None:
    """Handle tool call events."""
    print(f"Tool called on {event.server_name}: {event.data}")

def on_error(event: MCPEvent) -> None:
    """Handle error events."""
    print(f"Error on {event.server_name}: {event.data}")

# Usage example
async def reactive_example():
    """Example using reactive client."""
    client = ReactiveClient("assistant", "python", ["../first-server/src/server.py"])
    
    # Register event handlers
    client.on("tool_call_start", on_tool_call)
    client.on("tool_call_success", on_tool_call)
    client.on("tool_call_error", on_error)
    
    try:
        await client.connect()
        
        # This will trigger events
        result = await client.call_tool("calculate", {"expression": "2 + 2"})
        print(f"Result: {result}")
    
    finally:
        await client.disconnect()
```

## Integration Patterns

### Web Application Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

# Global MCP client
mcp_client: Optional[MCPClient] = None

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Initialize MCP connection on startup."""
    global mcp_client
    mcp_client = MCPClient("python", ["../first-server/src/server.py"])
    await mcp_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up MCP connection on shutdown."""
    if mcp_client:
        await mcp_client.disconnect()

@app.get("/tools")
async def list_tools():
    """API endpoint to list available tools."""
    if not mcp_client:
        raise HTTPException(status_code=500, detail="MCP client not initialized")
    
    tools = await mcp_client.list_tools()
    return {"tools": tools}

@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """API endpoint to call MCP tools."""
    if not mcp_client:
        raise HTTPException(status_code=500, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.call_tool(request.tool_name, request.arguments)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### CLI Tool Integration

```python
import click
import asyncio
from typing import Dict, Any

class CLIMCPClient:
    """CLI wrapper for MCP client."""
    
    def __init__(self):
        self.client: Optional[MCPClient] = None
    
    async def setup(self, server_command: str, server_args: List[str]) -> None:
        """Setup MCP connection."""
        self.client = MCPClient(server_command, server_args)
        await self.client.connect()
    
    async def cleanup(self) -> None:
        """Cleanup MCP connection."""
        if self.client:
            await self.client.disconnect()

# Global CLI client
cli_client = CLIMCPClient()

@click.group()
@click.option('--server-command', default='python', help='MCP server command')
@click.option('--server-args', multiple=True, help='MCP server arguments')
@click.pass_context
def cli(ctx, server_command: str, server_args: tuple):
    """MCP CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj['server_command'] = server_command
    ctx.obj['server_args'] = list(server_args)

@cli.command()
@click.pass_context
def list_tools(ctx):
    """List available MCP tools."""
    async def _list_tools():
        await cli_client.setup(ctx.obj['server_command'], ctx.obj['server_args'])
        try:
            tools = await cli_client.client.list_tools()
            for tool in tools:
                click.echo(f"- {tool}")
        finally:
            await cli_client.cleanup()
    
    asyncio.run(_list_tools())

@cli.command()
@click.argument('tool_name')
@click.argument('arguments', type=click.STRING)
@click.pass_context
def call_tool(ctx, tool_name: str, arguments: str):
    """Call an MCP tool."""
    async def _call_tool():
        await cli_client.setup(ctx.obj['server_command'], ctx.obj['server_args'])
        try:
            import json
            args_dict = json.loads(arguments) if arguments else {}
            result = await cli_client.client.call_tool(tool_name, args_dict)
            click.echo(result)
        finally:
            await cli_client.cleanup()
    
    asyncio.run(_call_tool())

if __name__ == '__main__':
    cli()
```

## Error Handling and Resilience

### Robust Connection Management

```python
import asyncio
from typing import Optional
import time

class ResilientMCPClient(MCPClient):
    """MCP client with automatic reconnection and retry logic."""
    
    def __init__(self, server_command: str, server_args: List[str], 
                 max_retries: int = 3, retry_delay: float = 1.0):
        super().__init__(server_command, server_args)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connected = False
    
    async def connect_with_retry(self) -> None:
        """Connect with automatic retry."""
        for attempt in range(self.max_retries):
            try:
                await self.connect()
                self.connected = True
                return
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise
    
    async def call_tool_with_retry(self, name: str, arguments: Dict) -> Optional[str]:
        """Call tool with automatic retry on connection failure."""
        for attempt in range(self.max_retries):
            try:
                if not self.connected:
                    await self.connect_with_retry()
                
                return await self.call_tool(name, arguments)
            
            except Exception as e:
                logger.warning(f"Tool call attempt {attempt + 1} failed: {e}")
                self.connected = False
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise
    
    async def health_check(self) -> bool:
        """Check if the connection is healthy."""
        try:
            await self.list_tools()
            return True
        except Exception:
            self.connected = False
            return False

# Usage with health monitoring
async def monitored_client_example():
    """Example with health monitoring."""
    client = ResilientMCPClient("python", ["../first-server/src/server.py"])
    
    try:
        await client.connect_with_retry()
        
        # Periodic health check
        while True:
            if not await client.health_check():
                logger.warning("Health check failed, attempting reconnection...")
                await client.connect_with_retry()
            
            # Do work
            result = await client.call_tool_with_retry("calculate", {"expression": "1 + 1"})
            print(f"Result: {result}")
            
            await asyncio.sleep(10)  # Check every 10 seconds
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await client.disconnect()
```

## Configuration Management

### Configuration-Driven Client

```python
import yaml
from pathlib import Path
from typing import Dict, List, Any

@dataclass
class ServerConfig:
    """Configuration for an MCP server."""
    name: str
    command: str
    args: List[str]
    disabled: bool = False
    auto_approve: List[str] = None
    env: Dict[str, str] = None

class ConfigurableMCPClient:
    """MCP client that loads configuration from files."""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.servers: Dict[str, ServerConfig] = {}
        self.clients: Dict[str, MCPClient] = {}
    
    def load_config(self) -> None:
        """Load server configuration from file."""
        with open(self.config_path) as f:
            config_data = yaml.safe_load(f)
        
        for name, server_data in config_data.get('mcpServers', {}).items():
            if not server_data.get('disabled', False):
                self.servers[name] = ServerConfig(
                    name=name,
                    command=server_data['command'],
                    args=server_data.get('args', []),
                    disabled=server_data.get('disabled', False),
                    auto_approve=server_data.get('autoApprove', []),
                    env=server_data.get('env', {})
                )
    
    async def connect_all(self) -> None:
        """Connect to all configured servers."""
        for name, config in self.servers.items():
            try:
                client = MCPClient(config.command, config.args)
                await client.connect()
                self.clients[name] = client
                logger.info(f"Connected to server: {name}")
            except Exception as e:
                logger.error(f"Failed to connect to {name}: {e}")
    
    async def disconnect_all(self) -> None:
        """Disconnect from all servers."""
        for name, client in self.clients.items():
            try:
                await client.disconnect()
                logger.info(f"Disconnected from server: {name}")
            except Exception as e:
                logger.error(f"Error disconnecting from {name}: {e}")
        
        self.clients.clear()

# Example configuration file (config.yaml)
config_yaml = """
mcpServers:
  personal-assistant:
    command: python
    args: ["../first-server/src/server.py"]
    disabled: false
    autoApprove: ["calculate"]
    env:
      LOG_LEVEL: "INFO"
  
  weather:
    command: uvx
    args: ["weather-mcp-server"]
    disabled: false
    autoApprove: []
"""

# Usage
async def config_example():
    """Example using configuration-driven client."""
    # Save example config
    with open("mcp-config.yaml", "w") as f:
        f.write(config_yaml)
    
    client = ConfigurableMCPClient(Path("mcp-config.yaml"))
    client.load_config()
    
    try:
        await client.connect_all()
        
        # Use the connected servers
        if "personal-assistant" in client.clients:
            result = await client.clients["personal-assistant"].call_tool(
                "calculate", {"expression": "42 * 2"}
            )
            print(f"Calculation: {result}")
    
    finally:
        await client.disconnect_all()
```

## Best Practices

### 1. Connection Management
- Always use context managers or try/finally blocks
- Implement connection pooling for multiple servers
- Add health checks and automatic reconnection
- Handle server startup/shutdown gracefully

### 2. Error Handling
- Catch and log all exceptions
- Provide meaningful error messages to users
- Implement retry logic with exponential backoff
- Validate server responses

### 3. Performance
- Use async/await for all I/O operations
- Implement connection pooling
- Cache tool and resource lists when appropriate
- Batch operations when possible

### 4. Security
- Validate all server responses
- Implement permission checks for tool calls
- Use secure communication channels
- Never trust server data without validation

### 5. User Experience
- Provide clear feedback on operations
- Handle long-running operations gracefully
- Implement progress indicators
- Offer offline capabilities when possible

## Testing Your Client

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_client_connection():
    """Test client connection."""
    with patch('mcp.ClientSession') as mock_session:
        mock_session.return_value.__aenter__ = AsyncMock()
        mock_session.return_value.initialize = AsyncMock()
        
        client = MCPClient("python", ["server.py"])
        await client.connect()
        
        assert client.session is not None

@pytest.mark.asyncio
async def test_tool_call():
    """Test tool calling."""
    client = MCPClient("python", ["server.py"])
    client.session = AsyncMock()
    
    # Mock tool call response
    mock_result = AsyncMock()
    mock_result.content = [AsyncMock()]
    mock_result.content[0].text = "42"
    client.session.call_tool.return_value = mock_result
    
    result = await client.call_tool("calculate", {"expression": "6 * 7"})
    assert result == "42"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_integration():
    """Test full client-server integration."""
    client = MCPClient("python", ["../first-server/src/server.py"])
    
    try:
        await client.connect()
        
        # Test tool listing
        tools = await client.list_tools()
        assert "calculate" in tools
        
        # Test tool calling
        result = await client.call_tool("calculate", {"expression": "2 + 2"})
        assert "4" in result
        
        # Test resource listing
        resources = await client.list_resources()
        assert len(resources) > 0
    
    finally:
        await client.disconnect()
```

## Next Steps

### Advanced Topics
1. **Custom Transport**: Implement HTTP or WebSocket transport
2. **Streaming**: Handle real-time data streams
3. **Authentication**: Add security and user management
4. **Caching**: Implement intelligent caching strategies
5. **Monitoring**: Add metrics and observability

### Real-World Applications
1. **AI Assistant Integration**: Build MCP into AI applications
2. **Workflow Automation**: Create automation tools
3. **Data Pipeline**: Build data processing workflows
4. **API Gateway**: Create MCP-to-REST bridges
5. **Monitoring Dashboard**: Build server management tools

### Community Contribution
1. **Share your clients**: Contribute to the MCP ecosystem
2. **Write tutorials**: Help others learn
3. **Report issues**: Improve the MCP specification
4. **Build tools**: Create developer utilities

## Congratulations! 🎉

You now know how to:
- Build MCP clients from scratch
- Handle connections and errors robustly
- Integrate MCP into various application types
- Follow best practices for client development
- Test and debug your client implementations

You're ready to build powerful applications that leverage the MCP ecosystem!