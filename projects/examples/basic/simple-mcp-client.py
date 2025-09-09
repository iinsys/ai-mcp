#!/usr/bin/env python3
"""
Simple MCP Client Example

Demonstrates how to connect to and interact with an MCP server.
"""

import asyncio
import json
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters


async def main():
    """Example MCP client that connects to a server and calls tools."""
    
    # Server parameters - adjust path as needed
    server_params = StdioServerParameters(
        command="python",
        args=["../mcp-servers/template/server.py"],
    )
    
    async with ClientSession(server_params) as session:
        # Initialize the session
        await session.initialize()
        
        print("🚀 Connected to MCP server!")
        
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
        
        # Call the echo tool
        print("\n🔧 Calling echo tool...")
        echo_result = await session.call_tool("echo", {"text": "Hello from MCP client!"})
        print(f"Echo result: {echo_result.content[0].text}")
        
        # Call the calculate tool
        print("\n🧮 Calling calculate tool...")
        calc_result = await session.call_tool("calculate", {"expression": "10 + 5 * 2"})
        print(f"Calculation result: {calc_result.content[0].text}")
        
        # Read a resource
        print("\n📖 Reading server info resource...")
        info_result = await session.read_resource("template://info")
        print(f"Server info:\n{info_result.contents[0].text}")
        
        print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())