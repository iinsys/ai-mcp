# MCP Basics - Understanding the Model Context Protocol

A beginner-friendly introduction to the Model Context Protocol (MCP) and its core concepts.

## What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI assistants to securely connect to external data sources and tools. Think of it as a bridge between AI models and the real world.

## Why MCP Matters

### Before MCP
- AI assistants were isolated from external data
- Limited to pre-trained knowledge
- Couldn't perform real-world actions
- Required custom integrations for each use case

### With MCP
- AI assistants can access live data
- Perform actions through standardized tools
- Connect to databases, APIs, file systems, and more
- Secure, controlled access to resources

## Core Concepts

### 1. Servers and Clients

```
┌─────────────┐    MCP Protocol    ┌─────────────┐
│   Client    │ ◄─────────────────► │   Server    │
│ (AI Agent)  │                    │ (Data/Tools)│
└─────────────┘                    └─────────────┘
```

- **Client**: The AI assistant (like Claude, Kiro, etc.)
- **Server**: Provides tools and resources to the client
- **Protocol**: JSON-RPC based communication

### 2. Tools

Tools are functions that clients can call to perform actions:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {"type": "string"}
    }
  }
}
```

**Examples of tools**:
- Database queries
- File operations
- API calls
- Calculations
- System commands

### 3. Resources

Resources are data that clients can read:

```json
{
  "uri": "file://documents/report.pdf",
  "name": "Monthly Report",
  "description": "Sales report for January",
  "mimeType": "application/pdf"
}
```

**Examples of resources**:
- Files and documents
- Database records
- API responses
- Configuration data
- Live data feeds

### 4. Communication Flow

```
1. Client connects to Server
2. Client lists available tools/resources
3. Client calls tools or reads resources
4. Server processes requests and returns results
5. Client uses results to help the user
```

## MCP Architecture

### Transport Layer
- **stdio**: Standard input/output (most common)
- **HTTP**: Web-based communication
- **WebSocket**: Real-time bidirectional communication

### Message Types
- **Requests**: Client asks server to do something
- **Responses**: Server replies with results
- **Notifications**: One-way messages (no response expected)

### Security Model
- Servers run in isolated processes
- Clients control which tools to expose
- Input validation and sanitization
- Permission-based access control

## Real-World Example

Let's say you want an AI assistant to help with your project management:

### 1. The Problem
You need to check project status, update tasks, and generate reports.

### 2. The MCP Solution
Create an MCP server that connects to your project management system:

```python
# Tools the server provides
tools = [
    "list_projects",      # Get all projects
    "get_project_status", # Check project progress
    "update_task",        # Modify task details
    "generate_report"     # Create status reports
]

# Resources the server exposes
resources = [
    "project://active-projects",    # List of active projects
    "project://team-members",       # Team information
    "project://recent-updates"      # Latest changes
]
```

### 3. The Interaction
```
User: "What's the status of Project Alpha?"

AI Assistant:
1. Calls get_project_status("Project Alpha")
2. Receives current status data
3. Responds: "Project Alpha is 75% complete, 
   with 3 tasks remaining and deadline in 2 weeks."
```

## Benefits of MCP

### For Developers
- **Standardized**: One protocol for all integrations
- **Reusable**: Servers work with any MCP client
- **Secure**: Built-in security and isolation
- **Flexible**: Support for various data types and operations

### For Users
- **Powerful**: AI assistants can do more
- **Consistent**: Same interface across different tools
- **Safe**: Controlled access to sensitive data
- **Extensible**: Easy to add new capabilities

## MCP vs Other Approaches

### Traditional APIs
- **MCP**: Designed for AI interaction, includes metadata
- **REST APIs**: General purpose, requires custom integration

### Function Calling
- **MCP**: Standardized protocol, persistent connections
- **Function Calling**: Model-specific, stateless

### Plugins
- **MCP**: Cross-platform, secure isolation
- **Plugins**: Platform-specific, shared memory space

## Getting Started

### As a User
1. Install an MCP-compatible client (like Kiro)
2. Configure MCP servers for your needs
3. Start using enhanced AI capabilities

### As a Developer
1. Learn the MCP specification
2. Build servers for your data/tools
3. Test with MCP clients
4. Share with the community

## Common Use Cases

### Data Access
- Database queries
- File system operations
- API integrations
- Cloud storage access

### Automation
- System administration
- Deployment scripts
- Monitoring and alerts
- Workflow automation

### Development Tools
- Code analysis
- Testing automation
- Documentation generation
- Project management

### Business Applications
- CRM integration
- Analytics and reporting
- Customer support
- Content management

## Next Steps

Now that you understand MCP basics:

1. **Try it out**: Use an existing MCP server
2. **Build something**: Create your first MCP server
3. **Explore**: Look at community examples
4. **Contribute**: Share your servers with others

## Key Takeaways

- MCP connects AI assistants to external data and tools
- It uses a client-server architecture with standardized communication
- Tools perform actions, resources provide data
- Security and isolation are built into the protocol
- It's designed specifically for AI interaction patterns

Ready to build your first MCP server? Check out [Your First Server](../first-server/) tutorial!