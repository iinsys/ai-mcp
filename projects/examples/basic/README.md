# Basic MCP Examples

Simple examples to get started with MCP development.

## Files

- `simple-mcp-client.py` - Basic MCP client that connects to a server
- `config-example.json` - Example MCP configuration for clients like Kiro

## Running the Examples

1. Make sure you have the MCP dependencies installed:
   ```bash
   pip install mcp
   ```

2. Start the template server (in another terminal):
   ```bash
   cd mcp-servers/template
   python server.py
   ```

3. Run the client example:
   ```bash
   python simple-mcp-client.py
   ```

## Configuration Example

To use the template server with Kiro or another MCP client, add this to your MCP configuration:

```json
{
  "mcpServers": {
    "template": {
      "command": "python",
      "args": ["path/to/mcp-servers/template/server.py"],
      "disabled": false,
      "autoApprove": ["echo", "calculate"]
    }
  }
}
```

## What You'll Learn

- How to connect to an MCP server
- How to list available tools and resources
- How to call tools with parameters
- How to read resources from the server
- Basic error handling patterns