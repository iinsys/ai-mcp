# FileSystem Navigator MCP Server - Examples

This directory contains example clients and configurations for testing the FileSystem Navigator MCP server.

## Files

- `test-client.js` - Node.js test client using the MCP SDK
- `test-client.py` - Python test client (requires `pip install mcp`)
- `mcp-config.json` - MCP client configuration file
- `README.md` - This file

## Prerequisites

1. **Build the server** (from the parent directory):
   ```bash
   cd ..
   npm run build
   cd examples
   ```

2. **For Python client** (optional):
   ```bash
   pip install mcp
   ```

## Running the Examples

### Node.js Test Client

```bash
node test-client.js
```

This will run a comprehensive test suite that:
- Connects to the MCP server
- Lists available tools and resources
- Tests file search functionality
- Tests directory reading
- Tests file information retrieval
- Tests file content reading
- Tests security features (path traversal prevention)
- Tests resource URI access

### Python Test Client

```bash
# Run automated tests
python3 test-client.py

# Run interactive mode
python3 test-client.py interactive
```

The interactive mode allows you to manually test commands:
- `search <pattern> [directory]` - Search for files
- `list [path]` - List directory contents  
- `info <path>` - Get file information
- `read <path>` - Read file content
- `resource <uri>` - Access resource
- `quit` - Exit

### MCP Client Configuration

Use `mcp-config.json` with any MCP-compatible client:

```bash
# Copy to your MCP client's config directory
cp mcp-config.json ~/.config/mcp/servers.json
```

## Configuration

The examples use these environment variables:

- `FS_ROOT_PATH`: Root directory for file operations (default: current directory)
- `FS_MAX_DEPTH`: Maximum directory traversal depth (default: 5)
- `FS_MAX_FILE_SIZE`: Maximum file size to read in bytes (default: 1MB)
- `LOG_LEVEL`: Logging level (default: INFO)

## Expected Output

When running the test clients, you should see output like:

```
🚀 Starting FileSystem Navigator MCP Server Test...

✅ Connected to MCP server!
✅ Session initialized!

📋 Listing available tools...
Found 4 tools:
  - search_files: Search for files matching a pattern
  - read_directory: Read directory contents
  - get_file_info: Get detailed information about a file or directory
  - read_file_content: Read the content of a file

📚 Listing available resources...
Found 1 resources:
  - file://: Access files via file:// URI

🔍 Test 1: Searching for TypeScript files...
✅ Search result: {"files":[...],"totalFound":5,"returned":5}

📁 Test 2: Reading directory contents...
✅ Directory contents: {"contents":[...]}

📄 Test 3: Getting file information...
✅ File info: {"name":"package.json","isFile":true,...}

📖 Test 4: Reading file content...
✅ File content: {"name": "filesystem-navigator-mcp",...}

🔒 Test 5: Testing security (path traversal)...
✅ Security test result: {"error":"Access denied: Path traversal detected"}

🔗 Test 6: Accessing file via resource URI...
✅ Resource content: {"name": "filesystem-navigator-mcp",...}

✅ All tests completed successfully!
```

## Troubleshooting

### Common Issues

1. **"Cannot find module" errors**: Make sure you've built the server with `npm run build` from the parent directory
2. **Permission errors**: Ensure the server has read access to the target directory
3. **Connection issues**: Verify the server path is correct (should be `../dist/index.js` from examples directory)
4. **Python MCP client not found**: Install with `pip install mcp`

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
LOG_LEVEL=DEBUG node test-client.js
```

## Integration with AI Assistants

The MCP server can be integrated with AI assistants like Claude Desktop by using the `mcp-config.json` file. The AI assistant can then use the filesystem tools to:

- Search for code files
- Read project documentation  
- Analyze file structures
- Access configuration files
- Navigate project hierarchies

## Next Steps

After testing with these examples, you can:

1. Integrate the server with your preferred MCP client
2. Customize the configuration for your specific use case
3. Extend the server with additional tools if needed
4. Use the server in production with appropriate security settings
