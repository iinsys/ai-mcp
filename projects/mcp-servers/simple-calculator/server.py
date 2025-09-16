#!/usr/bin/env python3
"""
Simple Calculator MCP Server

A beginner-friendly MCP server that demonstrates basic concepts through
simple mathematical operations and utility functions. This server is designed
to be educational and easy to understand for those learning MCP development.
"""

import asyncio
import logging
import math
import random
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    TextResourceContents,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server instance
server = Server("simple-calculator")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools - this is where we define what our server can do."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to add",
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number to add",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract second number from first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Number to subtract from",
                    },
                    "b": {
                        "type": "number",
                        "description": "Number to subtract",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to multiply",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number to multiply",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Dividend (number to be divided)",
                    },
                    "b": {
                        "type": "number",
                        "description": "Divisor (number to divide by)",
                    }
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="power",
            description="Raise first number to the power of second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "base": {
                        "type": "number",
                        "description": "Base number",
                    },
                    "exponent": {
                        "type": "number",
                        "description": "Exponent (power)",
                    }
                },
                "required": ["base", "exponent"],
            },
        ),
        Tool(
            name="square_root",
            description="Calculate the square root of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "number",
                        "description": "Number to find square root of",
                    }
                },
                "required": ["number"],
            },
        ),
        Tool(
            name="random_number",
            description="Generate a random number between min and max (inclusive)",
            inputSchema={
                "type": "object",
                "properties": {
                    "min": {
                        "type": "number",
                        "description": "Minimum value (inclusive)",
                        "default": 0
                    },
                    "max": {
                        "type": "number",
                        "description": "Maximum value (inclusive)",
                        "default": 100
                    }
                },
                "required": [],
            },
        ),
        Tool(
            name="factorial",
            description="Calculate the factorial of a number (n!)",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "Number to calculate factorial for (must be non-negative)",
                    }
                },
                "required": ["number"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls - this is where the actual work happens."""
    try:
        if name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return CallToolResult(
                content=[TextContent(type="text", text=f"{a} + {b} = {result}")]
            )
        
        elif name == "subtract":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a - b
            return CallToolResult(
                content=[TextContent(type="text", text=f"{a} - {b} = {result}")]
            )
        
        elif name == "multiply":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a * b
            return CallToolResult(
                content=[TextContent(type="text", text=f"{a} × {b} = {result}")]
            )
        
        elif name == "divide":
            a = arguments.get("a", 0)
            b = arguments.get("b", 1)
            if b == 0:
                return CallToolResult(
                    content=[TextContent(type="text", text="Error: Division by zero is not allowed")]
                )
            result = a / b
            return CallToolResult(
                content=[TextContent(type="text", text=f"{a} ÷ {b} = {result}")]
            )
        
        elif name == "power":
            base = arguments.get("base", 0)
            exponent = arguments.get("exponent", 1)
            result = base ** exponent
            return CallToolResult(
                content=[TextContent(type="text", text=f"{base}^{exponent} = {result}")]
            )
        
        elif name == "square_root":
            number = arguments.get("number", 0)
            if number < 0:
                return CallToolResult(
                    content=[TextContent(type="text", text="Error: Cannot calculate square root of negative number")]
                )
            result = math.sqrt(number)
            return CallToolResult(
                content=[TextContent(type="text", text=f"√{number} = {result}")]
            )
        
        elif name == "random_number":
            min_val = arguments.get("min", 0)
            max_val = arguments.get("max", 100)
            if min_val > max_val:
                return CallToolResult(
                    content=[TextContent(type="text", text="Error: Minimum value cannot be greater than maximum value")]
                )
            result = random.randint(int(min_val), int(max_val))
            return CallToolResult(
                content=[TextContent(type="text", text=f"Random number between {min_val} and {max_val}: {result}")]
            )
        
        elif name == "factorial":
            number = arguments.get("number", 0)
            if number < 0:
                return CallToolResult(
                    content=[TextContent(type="text", text="Error: Factorial is not defined for negative numbers")]
                )
            if number > 170:  # Prevent overflow
                return CallToolResult(
                    content=[TextContent(type="text", text="Error: Number too large for factorial calculation")]
                )
            result = math.factorial(int(number))
            return CallToolResult(
                content=[TextContent(type="text", text=f"{number}! = {result}")]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    
    except Exception as e:
        logger.error(f"Error in tool call {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources - these provide information about our server."""
    return [
        Resource(
            uri="calculator://info",
            name="Calculator Information",
            description="Information about this simple calculator server",
            mimeType="text/plain",
        ),
        Resource(
            uri="calculator://help",
            name="Help Documentation",
            description="Detailed help and usage examples",
            mimeType="text/markdown",
        ),
        Resource(
            uri="calculator://examples",
            name="Usage Examples",
            description="Example calculations and tool usage",
            mimeType="text/markdown",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> ReadResourceResult:
    """Handle resource reading - provide information when requested."""
    try:
        if uri == "calculator://info":
            info = """
Simple Calculator MCP Server
============================

This is an educational MCP server that demonstrates:
- Basic tool implementation
- Input validation and error handling
- Mathematical operations
- Resource management
- Logging and debugging

Version: 1.0.0
Author: MCP Learning Project

Available Tools:
- add: Add two numbers
- subtract: Subtract two numbers  
- multiply: Multiply two numbers
- divide: Divide two numbers
- power: Raise to power
- square_root: Calculate square root
- random_number: Generate random number
- factorial: Calculate factorial
"""
            return ReadResourceResult(
                contents=[TextResourceContents(type="text", text=info, uri=uri)]
            )
        
        elif uri == "calculator://help":
            help_text = """
# Simple Calculator MCP Server Help

## Available Tools

### Basic Arithmetic

#### add
Add two numbers together.

**Parameters:**
- `a` (number): First number to add
- `b` (number): Second number to add

**Example:**
```json
{
  "a": 5,
  "b": 3
}
```
**Result:** `5 + 3 = 8`

#### subtract
Subtract second number from first number.

**Parameters:**
- `a` (number): Number to subtract from
- `b` (number): Number to subtract

**Example:**
```json
{
  "a": 10,
  "b": 4
}
```
**Result:** `10 - 4 = 6`

#### multiply
Multiply two numbers.

**Parameters:**
- `a` (number): First number to multiply
- `b` (number): Second number to multiply

**Example:**
```json
{
  "a": 6,
  "b": 7
}
```
**Result:** `6 × 7 = 42`

#### divide
Divide first number by second number.

**Parameters:**
- `a` (number): Dividend (number to be divided)
- `b` (number): Divisor (number to divide by)

**Example:**
```json
{
  "a": 15,
  "b": 3
}
```
**Result:** `15 ÷ 3 = 5`

**Note:** Division by zero will return an error.

### Advanced Operations

#### power
Raise first number to the power of second number.

**Parameters:**
- `base` (number): Base number
- `exponent` (number): Exponent (power)

**Example:**
```json
{
  "base": 2,
  "exponent": 8
}
```
**Result:** `2^8 = 256`

#### square_root
Calculate the square root of a number.

**Parameters:**
- `number` (number): Number to find square root of

**Example:**
```json
{
  "number": 64
}
```
**Result:** `√64 = 8.0`

**Note:** Negative numbers will return an error.

#### factorial
Calculate the factorial of a number (n!).

**Parameters:**
- `number` (integer): Number to calculate factorial for

**Example:**
```json
{
  "number": 5
}
```
**Result:** `5! = 120`

**Note:** Only non-negative integers are supported.

#### random_number
Generate a random number between min and max (inclusive).

**Parameters:**
- `min` (number, optional): Minimum value (default: 0)
- `max` (number, optional): Maximum value (default: 100)

**Example:**
```json
{
  "min": 1,
  "max": 10
}
```
**Result:** `Random number between 1 and 10: 7`

## Available Resources

- `calculator://info` - Server information
- `calculator://help` - This help documentation  
- `calculator://examples` - Usage examples

## Error Handling

This server includes comprehensive error handling for:
- Division by zero
- Square root of negative numbers
- Factorial of negative numbers
- Invalid input ranges
- Unknown tool names

## Usage

Configure this server in your MCP client and start performing calculations!
"""
            return ReadResourceResult(
                contents=[TextResourceContents(type="text", text=help_text, uri=uri)]
            )
        
        elif uri == "calculator://examples":
            examples = """
# Calculator Usage Examples

## Basic Arithmetic Examples

### Addition
```json
{"tool": "add", "arguments": {"a": 25, "b": 17}}
```
Result: `25 + 17 = 42`

### Subtraction  
```json
{"tool": "subtract", "arguments": {"a": 100, "b": 23}}
```
Result: `100 - 23 = 77`

### Multiplication
```json
{"tool": "multiply", "arguments": {"a": 12, "b": 8}}
```
Result: `12 × 8 = 96`

### Division
```json
{"tool": "divide", "arguments": {"a": 144, "b": 12}}
```
Result: `144 ÷ 12 = 12.0`

## Advanced Examples

### Powers
```json
{"tool": "power", "arguments": {"base": 3, "exponent": 4}}
```
Result: `3^4 = 81`

### Square Roots
```json
{"tool": "square_root", "arguments": {"number": 121}}
```
Result: `√121 = 11.0`

### Factorials
```json
{"tool": "factorial", "arguments": {"number": 6}}
```
Result: `6! = 720`

### Random Numbers
```json
{"tool": "random_number", "arguments": {"min": 1, "max": 20}}
```
Result: `Random number between 1 and 20: 13`

## Error Examples

### Division by Zero
```json
{"tool": "divide", "arguments": {"a": 10, "b": 0}}
```
Result: `Error: Division by zero is not allowed`

### Negative Square Root
```json
{"tool": "square_root", "arguments": {"number": -4}}
```
Result: `Error: Cannot calculate square root of negative number`

### Negative Factorial
```json
{"tool": "factorial", "arguments": {"number": -1}}
```
Result: `Error: Factorial is not defined for negative numbers`

## Learning Notes

This server demonstrates several important MCP concepts:

1. **Tool Definition**: Each tool has a clear name, description, and input schema
2. **Input Validation**: The server checks for valid inputs and handles errors gracefully
3. **Error Handling**: Comprehensive error messages help users understand what went wrong
4. **Resource Management**: The server provides helpful documentation as resources
5. **Logging**: All operations are logged for debugging purposes

Try experimenting with different values and see how the server responds!
"""
            return ReadResourceResult(
                contents=[TextResourceContents(type="text", text=examples, uri=uri)]
            )
        
        else:
            return ReadResourceResult(
                contents=[TextResourceContents(type="text", text=f"Resource not found: {uri}", uri=uri)]
            )
    
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return ReadResourceResult(
            contents=[TextResourceContents(type="text", text=f"Error: {str(e)}", uri=uri)]
        )


async def main():
    """Main server entry point - this starts our MCP server."""
    logger.info("Starting Simple Calculator MCP Server...")
    
    # Run the server with stdio transport
    async with stdio_server(server):
        await asyncio.Future()  # Keep the server running


if __name__ == "__main__":
    asyncio.run(main())
