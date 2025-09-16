# Simple Calculator MCP Server

A beginner-friendly Model Context Protocol (MCP) server that demonstrates basic MCP concepts through simple mathematical operations.

## Features

- **8 Mathematical Tools**: Add, subtract, multiply, divide, power, square root, factorial, random numbers
- **3 Educational Resources**: Server info, help documentation, usage examples
- **Comprehensive Error Handling**: Clear error messages for invalid operations
- **Educational Design**: Well-commented code perfect for learning MCP development

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `add` | Add two numbers | `5 + 3 = 8` |
| `subtract` | Subtract two numbers | `10 - 4 = 6` |
| `multiply` | Multiply two numbers | `6 × 7 = 42` |
| `divide` | Divide two numbers | `15 ÷ 3 = 5` |
| `power` | Raise to power | `2^8 = 256` |
| `square_root` | Calculate square root | `√64 = 8.0` |
| `random_number` | Generate random number | `Random between 1-10: 7` |
| `factorial` | Calculate factorial | `5! = 120` |

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install mcp
   ```

## Running the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
python server.py
```

The server will start and wait for MCP requests via stdio. Press Ctrl+C to stop.

## Testing

### Quick Test
```bash
# Activate virtual environment first
source venv/bin/activate

# Test server functionality
python -c "
import asyncio
import server

async def test():
    # Test tools
    tools = await server.handle_list_tools()
    print(f'✅ Found {len(tools)} tools')
    
    # Test basic operation
    result = await server.handle_call_tool('add', {'a': 5, 'b': 3})
    print(f'✅ 5 + 3 = {result.content[0].text}')
    
    # Test resources
    resources = await server.handle_list_resources()
    print(f'✅ Found {len(resources)} resources')

asyncio.run(test())
"
```

### Full Test Suite
```bash
# Activate virtual environment
source venv/bin/activate

# Run the test client (if MCP client API is working)
python test-client.py

# Run specific test types
python test-client.py basic      # Basic arithmetic tests
python test-client.py errors     # Error handling tests
python test-client.py interactive # Interactive demo
```

## Configuration

### For Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "/absolute/path/to/simple-calculator/venv/bin/python",
      "args": ["/absolute/path/to/simple-calculator/server.py"],
      "disabled": false
    }
  }
}
```

**Note:** Use the full path to the Python executable in your virtual environment and the full path to server.py.

## Usage Examples

### Basic Arithmetic
```json
{"tool": "add", "arguments": {"a": 5, "b": 3}}
// Result: 5 + 3 = 8

{"tool": "multiply", "arguments": {"a": 12, "b": 8}}
// Result: 12 × 8 = 96
```

### Advanced Operations
```json
{"tool": "power", "arguments": {"base": 2, "exponent": 8}}
// Result: 2^8 = 256

{"tool": "factorial", "arguments": {"number": 6}}
// Result: 6! = 720
```

### Error Handling
```json
{"tool": "divide", "arguments": {"a": 10, "b": 0}}
// Result: Error: Division by zero is not allowed
```

## Project Structure

```
simple-calculator/
├── server.py          # Main server implementation (625 lines)
├── test-client.py     # Test client (244 lines)
├── pyproject.toml     # Project configuration
├── README.md          # This documentation
└── venv/              # Virtual environment (created during setup)
```

**Note:** The `venv/` directory is created when you run the installation steps. It contains the MCP library and other dependencies.

## Learning Objectives

This server demonstrates:
- MCP server structure and implementation
- Tool definition and input validation
- Error handling and user feedback
- Resource management for documentation
- Logging and debugging practices

## Troubleshooting

### Common Issues

1. **"externally-managed-environment" error:**
   ```
   error: externally-managed-environment
   ```
   **Solution:** Use a virtual environment as shown in the installation steps.

2. **"ModuleNotFoundError: No module named 'mcp'":**
   **Solution:** Make sure you've activated the virtual environment and installed the MCP library.

3. **Server won't start:**
   **Solution:** Check that you're using the correct Python path in your Claude Desktop configuration.

4. **Test client errors:**
   **Solution:** The test client may have compatibility issues with newer MCP versions. Use the quick test method instead.

### Getting Help

If you encounter issues:
1. Make sure your virtual environment is activated
2. Verify the MCP library is installed: `pip list | grep mcp`
3. Test the server import: `python -c "import server; print('OK')"`
4. Check the server logs for error messages

## License

MIT License