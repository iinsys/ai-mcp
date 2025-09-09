# MCP Server Template

A basic template for creating new MCP servers.

## Features

- Basic server structure
- Example tools and resources
- Configuration handling
- Error handling and logging
- Type hints and documentation

## Quick Start

1. Copy this template directory:
   ```bash
   cp -r mcp-servers/template mcp-servers/your-server-name
   ```

2. Update the server details:
   - Modify `server.py` with your functionality
   - Update `pyproject.toml` with your server details
   - Customize this README

3. Install dependencies:
   ```bash
   cd mcp-servers/your-server-name
   pip install -e .
   ```

4. Test your server:
   ```bash
   python server.py
   ```

## Configuration

Configure in your MCP client:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "python",
      "args": ["path/to/your-server-name/server.py"],
      "disabled": false
    }
  }
}
```

## Development

- Follow MCP specification guidelines
- Include comprehensive error handling
- Add type hints for better development experience
- Document all tools and resources
- Include examples of usage