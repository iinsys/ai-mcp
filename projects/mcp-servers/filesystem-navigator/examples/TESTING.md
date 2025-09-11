# Testing the FileSystem Navigator MCP Server

This guide provides multiple ways to test and interact with the FileSystem Navigator MCP server.

## Prerequisites

1. **Build the server**:
   ```bash
   npm run build
   ```

2. **Install Python MCP client** (if using Python test client):
   ```bash
   pip install mcp
   ```

## Testing Methods

### 1. Unit Tests (Jest)

Run the comprehensive unit test suite:

```bash
npm test
```

This runs all tests including:
- File search functionality
- Directory reading
- File information retrieval
- File content reading
- Security tests (path traversal prevention)
- File size limits

### 2. Python Test Client

Use the provided Python test client for manual testing:

```bash
# Run automated tests
python test-client.py

# Run interactive mode
python test-client.py interactive
```

The interactive mode allows you to manually test commands:
- `search <pattern> [directory]` - Search for files
- `list [path]` - List directory contents  
- `info <path>` - Get file information
- `read <path>` - Read file content
- `resource <uri>` - Access resource
- `quit` - Exit

### 3. Direct Node.js Testing

Test the server directly with Node.js:

```bash
# Start the server
node dist/index.js

# In another terminal, you can send JSON-RPC messages via stdin
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js
```

### 4. MCP Client Integration

Use the MCP configuration file with any MCP-compatible client:

```bash
# Copy the config to your MCP client's config directory
cp mcp-config.json ~/.config/mcp/servers.json
```

## Test Scenarios

### Basic File Operations

1. **Search for files**:
   ```json
   {
     "tool": "search_files",
     "arguments": {
       "pattern": "**/*.ts",
       "directory": ".",
       "maxResults": 10
     }
   }
   ```

2. **List directory**:
   ```json
   {
     "tool": "read_directory", 
     "arguments": {
       "path": ".",
       "includeHidden": false
     }
   }
   ```

3. **Get file info**:
   ```json
   {
     "tool": "get_file_info",
     "arguments": {
       "path": "package.json"
     }
   }
   ```

4. **Read file content**:
   ```json
   {
     "tool": "read_file_content",
     "arguments": {
       "path": "package.json",
       "encoding": "utf8"
     }
   }
   ```

### Security Testing

Test path traversal prevention:
```json
{
  "tool": "get_file_info",
  "arguments": {
    "path": "../../../etc/passwd"
  }
}
```

Expected result: Access denied error.

### Resource Access

Access files via resource URI:
```
Resource URI: file://package.json
```

## Environment Variables

Configure the server behavior with these environment variables:

- `FS_ROOT_PATH`: Root directory for file operations (default: current directory)
- `FS_MAX_DEPTH`: Maximum directory traversal depth (default: 5)
- `FS_MAX_FILE_SIZE`: Maximum file size to read in bytes (default: 1MB)
- `LOG_LEVEL`: Logging level (default: INFO)

## Troubleshooting

### Common Issues

1. **Permission errors**: Ensure the server has read access to the target directory
2. **Path not found**: Check that `FS_ROOT_PATH` is set correctly
3. **File size errors**: Adjust `FS_MAX_FILE_SIZE` for larger files
4. **Connection issues**: Verify the server is built and the path is correct

### Debug Mode

Enable debug logging:
```bash
LOG_LEVEL=DEBUG node dist/index.js
```

### Test Coverage

The test suite covers:
- ✅ File search with various patterns
- ✅ Directory listing (recursive and non-recursive)
- ✅ File information retrieval
- ✅ File content reading with encoding
- ✅ Security measures (path traversal prevention)
- ✅ File size limits
- ✅ Error handling
- ✅ Resource URI access

## Performance Testing

For performance testing, you can:

1. **Test with large directories**:
   ```bash
   # Create a large test directory
   mkdir -p test-dir/{1..100}/{1..100}
   touch test-dir/{1..100}/{1..100}/file.txt
   
   # Test search performance
   python test-client.py
   ```

2. **Monitor memory usage**:
   ```bash
   # Run with memory monitoring
   node --inspect dist/index.js
   ```

## Integration with AI Assistants

The MCP server can be integrated with AI assistants like Claude Desktop:

1. Add the server configuration to your MCP client
2. The AI assistant can then use the filesystem tools to:
   - Search for code files
   - Read project documentation
   - Analyze file structures
   - Access configuration files
   - Navigate project hierarchies

## Example Use Cases

1. **Code Analysis**: Search for all TypeScript files and analyze patterns
2. **Documentation**: Find and read README files across a project
3. **Configuration**: Locate and read config files (package.json, tsconfig.json, etc.)
4. **Project Structure**: Get an overview of directory structure
5. **File Management**: Check file sizes, types, and permissions
