#!/usr/bin/env python3
"""
Test Client for FileSystem Navigator MCP Server

This script demonstrates how to test and interact with the filesystem navigator MCP server.
"""

import asyncio
import json
import os
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters


async def test_filesystem_navigator():
    """Test the filesystem navigator MCP server with various operations."""
    
    # Server parameters - adjust path as needed
    server_params = StdioServerParameters(
        command="node",
        args=["../dist/index.js"],
        env={
            "FS_ROOT_PATH": os.getcwd(),  # Set root to current directory
            "FS_MAX_DEPTH": "5",
            "FS_MAX_FILE_SIZE": "1048576"  # 1MB
        }
    )
    
    async with ClientSession(server_params) as session:
        # Initialize the session
        await session.initialize()
        
        print("🚀 Connected to FileSystem Navigator MCP server!")
        
        # List available tools
        tools = await session.list_tools()
        print(f"\n📋 Available tools: {len(tools.tools)}")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # List available resources
        resources = await session.list_resources()
        print(f"\n📚 Available resources: {len(resources.resources)}")
        for resource in resources.resources:
            print(f"  - {resource.name}: {resource.description}")
        
        # Test 1: Search for TypeScript files
        print("\n🔍 Test 1: Searching for TypeScript files...")
        try:
            result = await session.call_tool("search_files", {
                "pattern": "**/*.ts",
                "directory": ".",
                "maxResults": 5
            })
            print(f"Found TypeScript files: {result.content[0].text}")
        except Exception as e:
            print(f"Error searching files: {e}")
        
        # Test 2: Read directory contents
        print("\n📁 Test 2: Reading directory contents...")
        try:
            result = await session.call_tool("read_directory", {
                "path": ".",
                "includeHidden": False
            })
            print(f"Directory contents: {result.content[0].text}")
        except Exception as e:
            print(f"Error reading directory: {e}")
        
        # Test 3: Get file information
        print("\n📄 Test 3: Getting file information...")
        try:
            result = await session.call_tool("get_file_info", {
                "path": "package.json"
            })
            print(f"File info: {result.content[0].text}")
        except Exception as e:
            print(f"Error getting file info: {e}")
        
        # Test 4: Read file content
        print("\n📖 Test 4: Reading file content...")
        try:
            result = await session.call_tool("read_file_content", {
                "path": "package.json",
                "encoding": "utf8"
            })
            print(f"File content: {result.content[0].text}")
        except Exception as e:
            print(f"Error reading file: {e}")
        
        # Test 5: Test security - path traversal attempt
        print("\n🔒 Test 5: Testing security (path traversal)...")
        try:
            result = await session.call_tool("get_file_info", {
                "path": "../../../etc/passwd"
            })
            print(f"Security test result: {result.content[0].text}")
        except Exception as e:
            print(f"Security test error: {e}")
        
        # Test 6: Access file via resource URI
        print("\n🔗 Test 6: Accessing file via resource URI...")
        try:
            # Try to read a file via resource URI
            resource_result = await session.read_resource("file://package.json")
            print(f"Resource content: {resource_result.contents[0].text}")
        except Exception as e:
            print(f"Error accessing resource: {e}")
        
        print("\n✅ All tests completed!")


async def interactive_test():
    """Interactive testing mode for manual exploration."""
    
    server_params = StdioServerParameters(
        command="node",
        args=["../dist/index.js"],
        env={
            "FS_ROOT_PATH": os.getcwd(),
            "FS_MAX_DEPTH": "5",
            "FS_MAX_FILE_SIZE": "1048576"
        }
    )
    
    async with ClientSession(server_params) as session:
        await session.initialize()
        
        print("🚀 Interactive FileSystem Navigator Test Mode")
        print("Available commands:")
        print("  search <pattern> [directory] - Search for files")
        print("  list [path] - List directory contents")
        print("  info <path> - Get file information")
        print("  read <path> - Read file content")
        print("  resource <uri> - Access resource")
        print("  quit - Exit")
        
        while True:
            try:
                command = input("\n> ").strip().split()
                if not command:
                    continue
                
                if command[0] == "quit":
                    break
                elif command[0] == "search":
                    pattern = command[1] if len(command) > 1 else "**/*"
                    directory = command[2] if len(command) > 2 else "."
                    result = await session.call_tool("search_files", {
                        "pattern": pattern,
                        "directory": directory,
                        "maxResults": 10
                    })
                    print(result.content[0].text)
                elif command[0] == "list":
                    path = command[1] if len(command) > 1 else "."
                    result = await session.call_tool("read_directory", {
                        "path": path,
                        "includeHidden": False
                    })
                    print(result.content[0].text)
                elif command[0] == "info":
                    if len(command) < 2:
                        print("Usage: info <path>")
                        continue
                    result = await session.call_tool("get_file_info", {
                        "path": command[1]
                    })
                    print(result.content[0].text)
                elif command[0] == "read":
                    if len(command) < 2:
                        print("Usage: read <path>")
                        continue
                    result = await session.call_tool("read_file_content", {
                        "path": command[1],
                        "encoding": "utf8"
                    })
                    print(result.content[0].text)
                elif command[0] == "resource":
                    if len(command) < 2:
                        print("Usage: resource <uri>")
                        continue
                    result = await session.read_resource(command[1])
                    print(result.contents[0].text)
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_test())
    else:
        asyncio.run(test_filesystem_navigator())
