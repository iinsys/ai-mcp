# File System Navigator Usage Examples

This document provides practical examples of using the File System Navigator MCP server.

## Basic File Search

### Search for TypeScript files
```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "*.ts",
    "directory": "./src",
    "maxResults": 10
  }
}
```

### Search for configuration files
```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "*.{json,yaml,yml,toml}",
    "directory": ".",
    "includeHidden": true
  }
}
```

### Recursive search for test files
```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "**/*.test.{ts,js}",
    "directory": "./tests",
    "maxResults": 50
  }
}
```

## Directory Operations

### List current directory
```json
{
  "tool": "read_directory",
  "arguments": {
    "path": ".",
    "includeHidden": false
  }
}
```

### Recursive directory listing
```json
{
  "tool": "read_directory",
  "arguments": {
    "path": "./src",
    "recursive": true,
    "maxDepth": 3,
    "includeHidden": false
  }
}
```

## File Information

### Get detailed file info
```json
{
  "tool": "get_file_info",
  "arguments": {
    "path": "./package.json"
  }
}
```

### Check directory info
```json
{
  "tool": "get_file_info",
  "arguments": {
    "path": "./src"
  }
}
```

## File Content Reading

### Read a configuration file
```json
{
  "tool": "read_file_content",
  "arguments": {
    "path": "./tsconfig.json",
    "encoding": "utf8"
  }
}
```

### Read with size limit
```json
{
  "tool": "read_file_content",
  "arguments": {
    "path": "./large-file.txt",
    "maxSize": 1048576
  }
}
```

## Resource Access

### Access file via resource URI
```
Resource URI: file://src/server.ts
```

This will return the file content with appropriate MIME type detection.

## Common Use Cases

### 1. Code Analysis
Search for all TypeScript files, then read their contents to analyze code patterns:

```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "**/*.ts",
    "directory": "./src"
  }
}
```

### 2. Configuration Discovery
Find all configuration files in a project:

```json
{
  "tool": "search_files",
  "arguments": {
    "pattern": "{package.json,tsconfig.json,*.config.{js,ts,json}}",
    "directory": ".",
    "includeHidden": true
  }
}
```

### 3. Project Structure Analysis
Get a complete overview of project structure:

```json
{
  "tool": "read_directory",
  "arguments": {
    "path": ".",
    "recursive": true,
    "maxDepth": 4,
    "includeHidden": false
  }
}
```

### 4. File Size Analysis
Check file sizes to identify large files:

```json
{
  "tool": "get_file_info",
  "arguments": {
    "path": "./dist/bundle.js"
  }
}
```

## Error Handling

The server handles various error conditions gracefully:

- **Path traversal attempts**: Returns access denied error
- **File size limits**: Returns size exceeded error
- **Permission issues**: Skips inaccessible files
- **Invalid paths**: Returns file not found error

## Security Considerations

- All paths are resolved relative to the configured root directory
- Path traversal attacks are prevented
- File size limits prevent memory exhaustion
- Exclude patterns prevent access to sensitive directories
- Hidden files are excluded by default