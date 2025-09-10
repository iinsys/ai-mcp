# File System Navigator MCP Server

A TypeScript MCP server that provides intelligent file system operations for AI assistants.

## Features

### Tools
- `search_files` - Fuzzy search for files across directory structures
- `read_directory` - List directory contents with metadata
- `get_file_info` - Get detailed file information (size, permissions, dates)
- `read_file_content` - Read file contents with proper encoding detection

### Resources
- `file://` - Access to file contents
- `directory://` - Directory structure and metadata

## Installation

### Using uvx (Recommended)
```bash
uvx filesystem-navigator-mcp
```

### From Source
```bash
git clone https://github.com/iinsys/ai-mcp.git
cd ai-mcp/projects/mcp-servers/filesystem-navigator
npm install
npm run build
npm start
```

## Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "filesystem-navigator": {
      "command": "uvx",
      "args": ["filesystem-navigator-mcp"],
      "env": {
        "FS_ROOT_PATH": "/path/to/allowed/directory",
        "FS_MAX_DEPTH": "10",
        "FS_MAX_FILE_SIZE": "10485760"
      },
      "disabled": false
    }
  }
}
```

## Environment Variables

- `FS_ROOT_PATH` - Root directory to restrict access (default: current working directory)
- `FS_MAX_DEPTH` - Maximum directory traversal depth (default: 10)
- `FS_MAX_FILE_SIZE` - Maximum file size to read in bytes (default: 10MB)
- `FS_EXCLUDE_PATTERNS` - Comma-separated glob patterns to exclude (default: "node_modules,*.log,.git")

## Security

This server implements several security measures:
- Path traversal protection
- File size limits
- Directory depth limits
- Configurable root path restriction
- Exclude patterns for sensitive directories

## Usage Examples

### Search for TypeScript files
```typescript
// Tool call
{
  "name": "search_files",
  "arguments": {
    "pattern": "*.ts",
    "directory": "./src",
    "maxResults": 20
  }
}
```

### Read directory contents
```typescript
// Tool call
{
  "name": "read_directory",
  "arguments": {
    "path": "./src",
    "includeHidden": false,
    "recursive": false
  }
}
```

### Get file information
```typescript
// Tool call
{
  "name": "get_file_info",
  "arguments": {
    "path": "./package.json"
  }
}
```

## Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build
npm run build

# Test
npm test

# Lint
npm run lint
```

## License

MIT License - see [LICENSE](../../../LICENSE) file for details.