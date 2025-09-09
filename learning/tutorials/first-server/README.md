# Your First MCP Server

Build a simple MCP server from scratch and learn the fundamentals through hands-on coding.

## What We'll Build

A "Personal Assistant" MCP server that provides:
- **Tools**: Note-taking, task management, and calculations
- **Resources**: Access to saved notes and task lists
- **Real functionality**: Actually useful for daily work

## Prerequisites

- Python 3.8+ installed
- Basic Python knowledge
- Completed [MCP Basics](../mcp-basics/) tutorial

## Step 1: Project Setup

### Create Project Structure
```bash
mkdir my-first-mcp-server
cd my-first-mcp-server

# Create the basic structure
mkdir src tests
touch src/server.py
touch requirements.txt
touch README.md
```

### Install Dependencies
```bash
# Create requirements.txt
echo "mcp>=0.1.0" > requirements.txt
echo "pydantic>=2.0.0" >> requirements.txt

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Basic Server Structure

Create `src/server.py`:

```python
#!/usr/bin/env python3
"""
My First MCP Server - Personal Assistant

A simple MCP server for note-taking and task management.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.models import InitializationOptions
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
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("personal-assistant")

# Data storage (in a real app, use a proper database)
notes_file = Path("notes.json")
tasks_file = Path("tasks.json")

def load_data(file_path: Path) -> List[Dict]:
    """Load data from JSON file."""
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return []

def save_data(file_path: Path, data: List[Dict]) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

# We'll add the MCP handlers next...
```

## Step 3: Define Tools

Add tool definitions to your server:

```python
@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="add_note",
            description="Add a new note",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Note title"
                    },
                    "content": {
                        "type": "string", 
                        "description": "Note content"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="add_task",
            description="Add a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority"
                    }
                },
                "required": ["task"]
            }
        ),
        Tool(
            name="calculate",
            description="Perform basic calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression (e.g., '2 + 2 * 3')"
                    }
                },
                "required": ["expression"]
            }
        )
    ]
```

## Step 4: Implement Tool Handlers

Add the tool execution logic:

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "add_note":
            return await add_note(arguments)
        elif name == "add_task":
            return await add_task(arguments)
        elif name == "calculate":
            return await calculate(arguments)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )

async def add_note(arguments: Dict[str, Any]) -> CallToolResult:
    """Add a new note."""
    title = arguments["title"]
    content = arguments["content"]
    
    # Load existing notes
    notes = load_data(notes_file)
    
    # Create new note
    new_note = {
        "id": len(notes) + 1,
        "title": title,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    # Save note
    notes.append(new_note)
    save_data(notes_file, notes)
    
    return CallToolResult(
        content=[TextContent(
            type="text", 
            text=f"Note '{title}' added successfully! (ID: {new_note['id']})"
        )]
    )

async def add_task(arguments: Dict[str, Any]) -> CallToolResult:
    """Add a new task."""
    task_description = arguments["task"]
    priority = arguments.get("priority", "medium")
    
    # Load existing tasks
    tasks = load_data(tasks_file)
    
    # Create new task
    new_task = {
        "id": len(tasks) + 1,
        "task": task_description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    # Save task
    tasks.append(new_task)
    save_data(tasks_file, tasks)
    
    return CallToolResult(
        content=[TextContent(
            type="text",
            text=f"Task added: '{task_description}' (Priority: {priority}, ID: {new_task['id']})"
        )]
    )

async def calculate(arguments: Dict[str, Any]) -> CallToolResult:
    """Perform calculation."""
    expression = arguments["expression"]
    
    try:
        # Simple evaluation (in production, use a safer approach)
        result = eval(expression)
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"{expression} = {result}"
            )]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Calculation error: {str(e)}"
            )]
        )
```

## Step 5: Add Resources

Now add resource handling:

```python
@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="assistant://notes",
            name="My Notes",
            description="All saved notes",
            mimeType="application/json"
        ),
        Resource(
            uri="assistant://tasks",
            name="My Tasks", 
            description="All tasks and their status",
            mimeType="application/json"
        ),
        Resource(
            uri="assistant://summary",
            name="Daily Summary",
            description="Summary of notes and tasks",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> ReadResourceResult:
    """Handle resource reading."""
    try:
        if uri == "assistant://notes":
            notes = load_data(notes_file)
            return ReadResourceResult(
                contents=[TextContent(
                    type="text",
                    text=json.dumps(notes, indent=2)
                )]
            )
        
        elif uri == "assistant://tasks":
            tasks = load_data(tasks_file)
            return ReadResourceResult(
                contents=[TextContent(
                    type="text", 
                    text=json.dumps(tasks, indent=2)
                )]
            )
        
        elif uri == "assistant://summary":
            summary = generate_summary()
            return ReadResourceResult(
                contents=[TextContent(
                    type="text",
                    text=summary
                )]
            )
        
        else:
            return ReadResourceResult(
                contents=[TextContent(
                    type="text",
                    text=f"Resource not found: {uri}"
                )]
            )
    
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return ReadResourceResult(
            contents=[TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        )

def generate_summary() -> str:
    """Generate a summary of notes and tasks."""
    notes = load_data(notes_file)
    tasks = load_data(tasks_file)
    
    # Count tasks by status
    completed_tasks = sum(1 for task in tasks if task.get("completed", False))
    pending_tasks = len(tasks) - completed_tasks
    
    # Count tasks by priority
    high_priority = sum(1 for task in tasks if task.get("priority") == "high" and not task.get("completed", False))
    
    summary = f"""Personal Assistant Summary
========================

Notes: {len(notes)} total
Tasks: {len(tasks)} total
  - Completed: {completed_tasks}
  - Pending: {pending_tasks}
  - High Priority Pending: {high_priority}

Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return summary
```

## Step 6: Add Main Function

Complete the server with the main function:

```python
async def main():
    """Main server entry point."""
    logger.info("Starting Personal Assistant MCP Server...")
    
    # Run the server
    async with server.run_stdio() as streams:
        await server.run(
            streams[0], 
            streams[1], 
            InitializationOptions(
                server_name="personal-assistant",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 7: Test Your Server

### Create a Test Client

Create `test_client.py`:

```python
#!/usr/bin/env python3
"""
Test client for our MCP server.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters

async def test_server():
    """Test our MCP server."""
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["src/server.py"]
    )
    
    async with ClientSession(server_params) as session:
        # Initialize
        await session.initialize()
        print("✅ Connected to server!")
        
        # List tools
        tools = await session.list_tools()
        print(f"\n📋 Available tools: {len(tools.tools)}")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test adding a note
        print("\n📝 Adding a note...")
        result = await session.call_tool("add_note", {
            "title": "My First Note",
            "content": "This is a test note from my MCP server!"
        })
        print(f"Result: {result.content[0].text}")
        
        # Test adding a task
        print("\n✅ Adding a task...")
        result = await session.call_tool("add_task", {
            "task": "Learn MCP development",
            "priority": "high"
        })
        print(f"Result: {result.content[0].text}")
        
        # Test calculation
        print("\n🧮 Testing calculation...")
        result = await session.call_tool("calculate", {
            "expression": "10 + 5 * 2"
        })
        print(f"Result: {result.content[0].text}")
        
        # Read resources
        print("\n📚 Reading summary resource...")
        summary = await session.read_resource("assistant://summary")
        print(f"Summary:\n{summary.contents[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

### Run the Test

```bash
# Run the test client
python test_client.py
```

You should see output like:
```
✅ Connected to server!

📋 Available tools: 3
  - add_note: Add a new note
  - add_task: Add a new task
  - calculate: Perform basic calculations

📝 Adding a note...
Result: Note 'My First Note' added successfully! (ID: 1)

✅ Adding a task...
Result: Task added: 'Learn MCP development' (Priority: high, ID: 1)

🧮 Testing calculation...
Result: 10 + 5 * 2 = 20

📚 Reading summary resource...
Summary:
Personal Assistant Summary
========================

Notes: 1 total
Tasks: 1 total
  - Completed: 0
  - Pending: 1
  - High Priority Pending: 1

Last Updated: 2024-01-15 14:30:22
```

## Step 8: Use with an MCP Client

### Configure for Kiro

Create `mcp-config.json`:

```json
{
  "mcpServers": {
    "personal-assistant": {
      "command": "python",
      "args": ["path/to/your/src/server.py"],
      "disabled": false,
      "autoApprove": ["calculate"]
    }
  }
}
```

### Test with Kiro

1. Add the server to your Kiro MCP configuration
2. Restart Kiro or reconnect MCP servers
3. Try asking Kiro to:
   - "Add a note about today's meeting"
   - "Create a high priority task to review the code"
   - "Calculate 15% of 240"
   - "Show me my task summary"

## What You've Learned

### Core MCP Concepts
- **Server structure**: How to organize an MCP server
- **Tools**: Functions that perform actions
- **Resources**: Data that can be read
- **Error handling**: Proper exception management
- **Data persistence**: Saving and loading data

### Python Skills
- **Async programming**: Using async/await
- **JSON handling**: Loading and saving data
- **Type hints**: Better code documentation
- **Logging**: Debugging and monitoring

### MCP Protocol
- **Tool schemas**: Defining input requirements
- **Resource URIs**: Unique resource identifiers
- **Content types**: Different data formats
- **Client-server communication**: Request/response patterns

## Next Steps

### Enhance Your Server
1. **Add more tools**: Delete notes, complete tasks, search functionality
2. **Improve data storage**: Use SQLite or a proper database
3. **Add validation**: Better input checking and error messages
4. **Security**: Input sanitization and access controls

### Advanced Features
1. **Real-time updates**: Notify clients of changes
2. **File operations**: Read/write files on the system
3. **API integration**: Connect to external services
4. **Configuration**: Make the server configurable

### Share Your Work
1. **Package it**: Create a proper Python package
2. **Document it**: Write comprehensive documentation
3. **Test it**: Add unit and integration tests
4. **Publish it**: Share with the MCP community

## Troubleshooting

### Common Issues

**Server won't start**:
- Check Python version (3.8+)
- Verify MCP package is installed
- Look for syntax errors in your code

**Tools not working**:
- Check tool schemas match your arguments
- Add logging to see what's happening
- Test tool functions individually

**Client can't connect**:
- Verify server path in configuration
- Check server is executable
- Look at client logs for error messages

### Debugging Tips

```python
# Add more logging
logger.debug(f"Tool called: {name} with args: {arguments}")

# Test functions individually
if __name__ == "__main__":
    # Test your functions here
    result = add_note({"title": "test", "content": "test"})
    print(result)
```

## Congratulations! 🎉

You've built your first MCP server! You now understand:
- How MCP servers work
- The basic structure and patterns
- How to implement tools and resources
- How to test and debug your server

Ready for more advanced topics? Check out [Client Integration](../client-integration/) to learn how to build MCP clients!