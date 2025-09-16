#!/usr/bin/env python3
"""
Test Client for Simple Calculator MCP Server

This client demonstrates how to interact with the Simple Calculator MCP server.
It shows various ways to test the server's functionality and can be used for
development and learning purposes.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List

from mcp import ClientSession, StdioServerParameters


class CalculatorTestClient:
    """Test client for the Simple Calculator MCP server."""
    
    def __init__(self):
        self.session = None
    
    async def connect(self, server_path: str = "server.py"):
        """Connect to the MCP server."""
        print(f"🔌 Connecting to Simple Calculator MCP Server...")
        
        # Set up server parameters
        server_params = StdioServerParameters(
            command="python",
            args=[server_path]
        )
        
        # Create client session
        self.session = ClientSession(server_params)
        
        # Initialize the session
        await self.session.initialize()
        print("✅ Connected successfully!")
    
    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.session:
            await self.session.close()
            print("🔌 Disconnected from server")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        print("\n📋 Listing available tools...")
        
        result = await self.session.list_tools()
        tools = result.tools
        
        print(f"Found {len(tools)} tools:")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name}: {tool.description}")
        
        return tools
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources."""
        print("\n📚 Listing available resources...")
        
        result = await self.session.list_resources()
        resources = result.resources
        
        print(f"Found {len(resources)} resources:")
        for i, resource in enumerate(resources, 1):
            print(f"  {i}. {resource.name}: {resource.description}")
        
        return resources
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool with the given arguments."""
        print(f"\n🔧 Calling tool: {name}")
        print(f"   Arguments: {json.dumps(arguments, indent=2)}")
        
        result = await self.session.call_tool(name, arguments)
        
        # Extract text content
        if result.content:
            content = result.content[0].text
            print(f"   Result: {content}")
            return content
        else:
            print("   Result: No content returned")
            return ""
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource by URI."""
        print(f"\n📖 Reading resource: {uri}")
        
        result = await self.session.read_resource(uri)
        
        if result.contents:
            content = result.contents[0].text
            print(f"   Content preview: {content[:100]}...")
            return content
        else:
            print("   No content found")
            return ""
    
    async def run_basic_tests(self):
        """Run basic functionality tests."""
        print("\n🧪 Running basic functionality tests...")
        
        # Test basic arithmetic
        await self.call_tool("add", {"a": 5, "b": 3})
        await self.call_tool("subtract", {"a": 10, "b": 4})
        await self.call_tool("multiply", {"a": 6, "b": 7})
        await self.call_tool("divide", {"a": 15, "b": 3})
        
        # Test advanced operations
        await self.call_tool("power", {"base": 2, "exponent": 8})
        await self.call_tool("square_root", {"number": 64})
        await self.call_tool("factorial", {"number": 5})
        await self.call_tool("random_number", {"min": 1, "max": 10})
    
    async def run_error_tests(self):
        """Run error handling tests."""
        print("\n⚠️  Running error handling tests...")
        
        # Test division by zero
        await self.call_tool("divide", {"a": 10, "b": 0})
        
        # Test negative square root
        await self.call_tool("square_root", {"number": -4})
        
        # Test negative factorial
        await self.call_tool("factorial", {"number": -1})
        
        # Test invalid random range
        await self.call_tool("random_number", {"min": 10, "max": 5})
        
        # Test unknown tool
        await self.call_tool("unknown_tool", {"test": "value"})
    
    async def run_interactive_demo(self):
        """Run an interactive demonstration."""
        print("\n🎮 Interactive Calculator Demo")
        print("=" * 50)
        
        # Show available tools
        tools = await self.list_tools()
        
        # Demo some calculations
        print("\n🔢 Let's do some calculations:")
        
        # Basic arithmetic demo
        print("\n📊 Basic Arithmetic:")
        await self.call_tool("add", {"a": 25, "b": 17})
        await self.call_tool("multiply", {"a": 12, "b": 8})
        
        # Advanced operations demo
        print("\n🚀 Advanced Operations:")
        await self.call_tool("power", {"base": 3, "exponent": 4})
        await self.call_tool("square_root", {"number": 121})
        await self.call_tool("factorial", {"number": 6})
        
        # Random number demo
        print("\n🎲 Random Numbers:")
        for i in range(3):
            await self.call_tool("random_number", {"min": 1, "max": 100})
    
    async def run_comprehensive_test(self):
        """Run a comprehensive test suite."""
        print("\n🔬 Running Comprehensive Test Suite")
        print("=" * 60)
        
        # List tools and resources
        await self.list_tools()
        await self.list_resources()
        
        # Read help documentation
        await self.read_resource("calculator://help")
        
        # Run functionality tests
        await self.run_basic_tests()
        
        # Run error tests
        await self.run_error_tests()
        
        # Interactive demo
        await self.run_interactive_demo()
        
        print("\n✅ Comprehensive test completed!")


async def main():
    """Main function to run the test client."""
    print("🧮 Simple Calculator MCP Server - Test Client")
    print("=" * 60)
    
    client = CalculatorTestClient()
    
    try:
        # Connect to server
        await client.connect()
        
        # Check command line arguments for test type
        if len(sys.argv) > 1:
            test_type = sys.argv[1].lower()
            
            if test_type == "basic":
                await client.run_basic_tests()
            elif test_type == "errors":
                await client.run_error_tests()
            elif test_type == "interactive":
                await client.run_interactive_demo()
            elif test_type == "help":
                await client.read_resource("calculator://help")
            elif test_type == "info":
                await client.read_resource("calculator://info")
            elif test_type == "examples":
                await client.read_resource("calculator://examples")
            else:
                print(f"Unknown test type: {test_type}")
                print("Available options: basic, errors, interactive, help, info, examples")
        else:
            # Run comprehensive test by default
            await client.run_comprehensive_test()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Always disconnect
        await client.disconnect()


if __name__ == "__main__":
    # Check if server.py exists
    import os
    if not os.path.exists("server.py"):
        print("❌ Error: server.py not found in current directory")
        print("Please run this script from the simple-calculator directory")
        sys.exit(1)
    
    # Run the test client
    asyncio.run(main())
