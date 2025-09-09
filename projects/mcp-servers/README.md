# MCP Servers

This directory contains Model Context Protocol (MCP) server implementations.

## Available Servers

Each server is in its own subdirectory with:
- `README.md` - Server documentation and usage
- `server.py` or equivalent - Main server implementation
- `requirements.txt` or `pyproject.toml` - Dependencies
- `config.json` - Example configuration

## Quick Start

1. Install uv (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Run a server:
   ```bash
   uvx [server-package-name]
   ```

3. Configure in your MCP client (like Kiro):
   ```json
   {
     "mcpServers": {
       "server-name": {
         "command": "uvx",
         "args": ["server-package-name"],
         "disabled": false
       }
     }
   }
   ```

## Development

To create a new MCP server:

1. Create a new directory: `mkdir mcp-servers/your-server-name`
2. Follow the MCP server template structure
3. Include proper documentation and examples
4. Test with a compatible MCP client

## Server Template

See `template/` directory for a basic server structure to get started.