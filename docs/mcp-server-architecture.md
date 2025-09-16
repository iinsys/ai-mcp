# Building MCP Servers: Understanding Transport Layers and Core Components

In my [previous article](https://dev.to/bansikah/mcp-basics-understanding-the-model-context-protocol-566g), we explored what the Model Context Protocol (MCP) is and why it's revolutionizing how AI models interact with external systems. Now that we understand MCP's potential, let's dive deep into the implementation details—how to actually build MCP servers that are robust, scalable, and secure.

Building effective MCP servers requires mastering two key areas: the transport mechanisms that enable communication between clients and servers, and the core components (tools, resources, and prompts) that define your server's functionality. Let's explore each in detail.

## Transport Mechanisms: How MCP Connects

Think of transport mechanisms as the "delivery methods" for messages between AI models and your MCP server. Just like choosing how to send a package—hand delivery for urgent local items, postal service for standard shipping, or express courier for time-sensitive deliveries—MCP offers different transport options optimized for specific scenarios.

Imagine you're running a restaurant (your MCP server) and customers (AI models) want to place orders. You could take orders through:
- **Direct conversation** (STDIO) - fastest, but only one customer at a time
- **Phone calls** (HTTP) - can handle multiple customers, works remotely
- **Live updates on a screen** (SSE) - great for showing order status in real-time

The transport layer handles all the communication logistics—message formatting, delivery confirmation, error handling—so you can focus on cooking (your server's business logic) rather than managing the ordering system.

### STDIO Transport: Direct Process Communication

STDIO transport is like having a private, dedicated phone line between the AI model and your server. When Claude Desktop wants to use your MCP server, it's like hiring a personal assistant (spawning your server process) who sits right next to them and communicates through simple notes passed back and forth.

Think of it as the difference between shouting across a crowded room versus having a quiet, one-on-one conversation. There's no network noise, no interference from other conversations, and no delay—just direct, immediate communication. This is why STDIO is perfect for desktop applications where speed and reliability matter most.

```typescript
// Server setup with STDIO transport
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0',
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Technical Details:**
- **Protocol**: JSON-RPC over stdin/stdout streams
- **Process Model**: Client spawns server as child process
- **Latency**: Ultra-low (~1ms) - no network overhead
- **Concurrency**: Single client per server instance
- **Connection**: Automatic cleanup when client terminates

**When to Use STDIO:**
- Building tools for Claude Desktop or similar local AI apps
- Creating development utilities that need fast response times
- When you want simple deployment (just an executable file)
- For personal productivity tools on your local machine

**Example Scenario:** You're building a code analysis tool for developers. Using STDIO transport means Claude Desktop can spawn your server instantly when needed, analyze code with minimal delay, and automatically clean up when done.

### HTTP Transport: Web-Scale Communication

HTTP transport is like turning your MCP server into a popular restaurant that takes phone orders. Instead of having one dedicated assistant (STDIO), you now have a phone system that can handle multiple customers calling simultaneously from anywhere in the world.

Just like a restaurant can serve customers who call from different locations, HTTP transport allows multiple AI clients to connect to your server over the internet. You can set up security (like requiring a password to place orders), handle busy periods with load balancing (multiple phone lines), and even serve customers in different time zones. The trade-off is slightly slower service due to the "phone call overhead," but you gain the ability to serve many more customers.

```typescript
// HTTP server implementation
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { HttpServerTransport } from '@modelcontextprotocol/sdk/server/http.js';

const server = new Server({
  name: 'web-mcp-server',
  version: '1.0.0',
});

const transport = new HttpServerTransport({
  port: 3000,
  host: 'localhost'
});

await server.connect(transport);
```

**Technical Details:**
- **Protocol**: JSON-RPC over HTTP/HTTPS
- **Connection Model**: Stateless request-response
- **Latency**: Network-dependent (typically 10-100ms+ depending on distance)
- **Concurrency**: Handles multiple simultaneous clients
- **Scaling**: Can use load balancers, reverse proxies, clustering

**When to Use HTTP:**
- **Remote Access**: Server and client are on different machines
- **Web Integration**: Embedding MCP functionality in web applications
- **Team Sharing**: Multiple developers need access to the same server
- **Cloud Deployment**: Running servers on AWS, Google Cloud, etc.
- **Production Systems**: Need monitoring, logging, and enterprise features

**Example Scenario:** Your team needs a shared database query tool. Deploy it as an HTTP MCP server on your cloud infrastructure, and multiple team members can access it remotely through their AI clients. Add authentication headers to control access and use HTTPS for secure communication.

### Server-Sent Events (SSE): Real-Time Streaming

SSE transport is like having a live sports commentator giving play-by-play updates. Instead of the AI having to repeatedly ask "Are you done yet?" (like checking order status every few minutes), your server can actively broadcast updates as things happen.

Imagine you're processing a large dataset—with SSE, you can send updates like "10% complete... 25% complete... found interesting pattern... 75% complete..." This keeps the AI informed and engaged, rather than leaving it waiting in silence. It's perfect for long-running tasks where you want to show progress, like a pizza tracker showing when your order is being prepared, baked, and out for delivery.

```typescript
// SSE transport for real-time updates
import { SseServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';

const transport = new SseServerTransport({
  endpoint: '/events',
  port: 3000
});

// Stream real-time updates
transport.sendEvent({
  type: 'progress',
  data: { completed: 75, total: 100 }
});
```

**Technical Details:**
- **Protocol**: Server-Sent Events over HTTP
- **Connection Model**: Long-lived, server-to-client streaming
- **Latency**: Near real-time (typically <100ms for event delivery)
- **Concurrency**: Multiple clients can subscribe to event streams
- **Reliability**: Built-in reconnection and event ID tracking

**When to Use SSE:**
- **Long Operations**: File processing, data analysis, model training
- **Live Updates**: Real-time dashboards, monitoring systems
- **Progress Tracking**: Show completion status for multi-step workflows
- **Event Notifications**: Alert clients about system changes or updates

**Example Scenario:** You're building an AI-powered data processing pipeline. Use SSE to stream progress updates as files are processed, allowing the AI client to provide real-time feedback to users and make decisions based on intermediate results.

## Transport Selection Guide

| Transport | Latency | Scalability | Deployment | Security | Best For |
|-----------|---------|-------------|------------|----------|----------|
| **STDIO** | ~1ms | Single client | Executable file | Process isolation | Local tools, Claude Desktop |
| **HTTP** | 10-100ms+ | High (load balancing) | Web server + networking | HTTPS + auth headers | Remote access, web apps |
| **SSE** | <100ms | Medium (connection limits) | Web server + event handling | HTTP security + validation | Real-time updates, monitoring |

### Decision Framework

**Choose STDIO when:**
- Your server will run on the same machine as the AI client
- You need the fastest possible response times
- You want simple deployment (single executable)
- Building for Claude Desktop or similar local applications

**Choose HTTP when:**
- You need remote access (server and client on different machines)
- Multiple clients need to use the same server simultaneously  
- You're integrating with web applications or cloud services
- You need enterprise features like load balancing and monitoring

**Choose SSE when:**
- Your operations take significant time and need progress updates
- You're building real-time monitoring or dashboard systems
- You need to push notifications or alerts to clients
- Your workflow involves streaming data or continuous updates

## Core Components: The Building Blocks

Think of MCP servers like a Swiss Army knife for AI models. Just as a Swiss Army knife has different tools for different tasks, MCP servers have three types of components that give AI models different capabilities. Understanding these components is like learning what each tool in the knife does and when to use it.

### Tools: Executable Actions

Tools are like the power tools in a workshop—they're what allow the AI to actually *do* things in the real world. Just as a carpenter has different tools for different jobs (saw for cutting, drill for holes, sander for smoothing), your MCP server provides different tools for different actions.

Think of tools as the AI's "hands"—they extend the AI's capabilities beyond just thinking and talking. Want to search through files? There's a tool for that. Need to send an email? Another tool. Process an image? Yet another tool.

The magic happens when you design tools like a good craftsperson organizes their workshop: each tool has a clear purpose, is reliable when used correctly, and comes with clear instructions (documentation) so even a novice can use it safely and effectively.

```typescript
// Tool definition with comprehensive validation
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'search_files',
      description: 'Search for files using glob patterns',
      inputSchema: {
        type: 'object',
        properties: {
          pattern: {
            type: 'string',
            description: 'Glob pattern (e.g., "*.ts", "**/*.json")',
            pattern: '^[^/\\\\:*?"<>|]+$' // Security: prevent path traversal
          },
          maxResults: {
            type: 'number',
            minimum: 1,
            maximum: 100,
            default: 50
          }
        },
        required: ['pattern']
      }
    }
  ]
}));

// Tool execution with error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      case 'search_files':
        return await handleSearchFiles(validateArgs(args));
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.message}`
      }],
      isError: true
    };
  }
});
```

**Tool Design Principles:**

1. **Single Responsibility**: Each tool should do one thing well
   - ✅ Good: `search_files` - searches for files using patterns
   - ❌ Bad: `file_manager` - searches, creates, deletes, and modifies files

2. **Input Validation**: Always validate and sanitize inputs
   ```typescript
   // Validate file patterns to prevent security issues
   if (!/^[a-zA-Z0-9*.\-_/]+$/.test(pattern)) {
     throw new Error('Invalid pattern: contains unsafe characters');
   }
   ```

3. **Error Handling**: Provide clear, actionable error messages
   ```typescript
   // Instead of: "Error occurred"
   // Use: "File not found: /path/to/file.txt. Check the path and permissions."
   ```

4. **Rich Documentation**: Help AI models understand when and how to use tools
   ```typescript
   description: 'Search for files using glob patterns. Use * for wildcards, ** for recursive search. Example: "**/*.js" finds all JavaScript files recursively.'
   ```

**Technical Implementation Details:**
- Tools use JSON Schema for input validation, providing type safety and automatic validation
- The `inputSchema` property defines exactly what parameters the tool accepts
- Return values should always include a `content` array with structured responses
- Use the `isError` flag to indicate when operations fail

### Resources: Accessible Data

Resources are like a well-organized library that the AI can browse and read from. Just as a library has books, magazines, DVDs, and digital resources all organized with a clear cataloging system (like the Dewey Decimal System), MCP resources use URI patterns to organize different types of information.

Think of resources as the AI's "reference materials." When a student needs to write a research paper, they don't just need tools (pen, computer, printer)—they need access to information (books, articles, databases). Similarly, AI models need both tools to take actions AND resources to understand context and make informed decisions.

The URI system works like library call numbers: `file://documents/readme.md` is like saying "go to the Documents section, find the README file," while `api://users/123/profile` means "check the User Records section, look up person #123's profile." This consistent addressing system helps the AI quickly find exactly what it needs.

```typescript
// Resource listing with metadata
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: 'file://documents/readme.md',
      name: 'Project README',
      description: 'Main project documentation',
      mimeType: 'text/markdown'
    },
    {
      uri: 'api://users/profile',
      name: 'User Profile',
      description: 'Current user profile data',
      mimeType: 'application/json'
    }
  ]
}));

// Resource reading with content negotiation
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  
  if (uri.startsWith('file://')) {
    const filePath = uri.slice(7);
    const content = await fs.readFile(filePath, 'utf8');
    
    return {
      contents: [{
        uri,
        mimeType: mime.lookup(filePath) || 'text/plain',
        text: content
      }]
    };
  }
  
  throw new Error(`Unsupported resource URI: ${uri}`);
});
```

**Resource Design Patterns:**

1. **URI Schemes**: Create consistent, hierarchical patterns
   ```typescript
   // File system resources
   'file://documents/readme.md'
   'file://logs/2024/january/app.log'
   
   // API resources  
   'api://users/123/profile'
   'api://orders/456/items'
   
   // Database resources
   'db://customers/active'
   'db://products/category/electronics'
   ```

2. **MIME Types**: Enable proper content handling
   ```typescript
   // Let AI clients know what type of data they're getting
   mimeType: 'application/json'     // Structured data
   mimeType: 'text/markdown'        // Documentation
   mimeType: 'text/csv'            // Tabular data
   mimeType: 'image/png'           // Binary content
   ```

3. **Caching Strategy**: Implement efficient updates
   ```typescript
   // Use ETags to avoid re-reading unchanged resources
   const etag = generateETag(content);
   if (request.headers['if-none-match'] === etag) {
     return { status: 304 }; // Not modified
   }
   ```

4. **Security Considerations**: Always validate access
   ```typescript
   // Prevent path traversal attacks
   const safePath = path.resolve(SAFE_ROOT, requestedPath);
   if (!safePath.startsWith(SAFE_ROOT)) {
     throw new Error('Access denied: path outside allowed directory');
   }
   ```

**Technical Implementation:**
- Resources are read-only from the AI client's perspective
- Use the `ListResourcesRequestSchema` to advertise available resources
- Implement `ReadResourceRequestSchema` to serve resource content
- Support content negotiation through MIME types for optimal AI processing

### Prompts: Conversation Templates

Prompts are like having a collection of conversation scripts or templates that help guide interactions. Think of them as the "Mad Libs" of AI conversations—you create a template with blanks to fill in, and the AI can use these templates to start productive conversations.

Imagine you're a manager who frequently needs to conduct different types of meetings. Instead of improvising each time, you might have templates: "Performance Review Template," "Project Kickoff Template," "Problem-Solving Template." Each template has a structure and key questions, but you fill in the specific details for each situation.

MCP prompts work the same way—they provide proven conversation patterns that AI models can use as starting points, customized with specific context for each situation.

**Technical Architecture:**
- Prompts use template variables for dynamic content generation
- They return complete conversation contexts with role-based messages
- Parameters enable customization without changing the core template
- The AI client invokes prompts to establish structured conversation flows

**When to Use Prompts:**
- **Standardizing Workflows**: Create consistent approaches to common tasks
- **Domain Expertise**: Embed specialized knowledge into conversation starters
- **Complex Processes**: Guide AI through multi-step procedures
- **Quality Control**: Ensure AI interactions follow best practices

```typescript
// Prompt definition with variables
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: 'code_review',
      description: 'Generate code review comments',
      arguments: [
        {
          name: 'language',
          description: 'Programming language',
          required: true
        },
        {
          name: 'focus_areas',
          description: 'Areas to focus on (security, performance, etc.)',
          required: false
        }
      ]
    }
  ]
}));

// Prompt rendering with context injection
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'code_review') {
    const language = args?.language || 'javascript';
    const focusAreas = args?.focus_areas || 'general best practices';
    
    return {
      description: `Code review for ${language}`,
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Please review this ${language} code focusing on ${focusAreas}. 
                   Provide specific, actionable feedback with examples.`
          }
        }
      ]
    };
  }
  
  throw new Error(`Unknown prompt: ${name}`);
});
```

## Integration Patterns: Making Components Work Together

The real power of MCP comes from how these components work together, like instruments in an orchestra. Each component has its role, but the magic happens when they're coordinated to create something greater than the sum of their parts.

### Tool-Resource Synergy

Think of the relationship between tools and resources like a detective and evidence. The detective (AI) uses tools (investigation methods) to gather and analyze resources (evidence, witness statements, documents). Sometimes using a tool creates new evidence that becomes a resource for further investigation.

Tools and resources work together to create powerful workflows:

```typescript
// Tool that creates resources dynamically
async function handleAnalyzeCode(args: { filePath: string }) {
  // Tool action: analyze the code
  const analysis = await analyzeCodeFile(args.filePath);
  
  // Create a resource with results
  const resourceUri = `analysis://reports/${Date.now()}`;
  resourceCache.set(resourceUri, {
    content: JSON.stringify(analysis, null, 2),
    mimeType: 'application/json',
    timestamp: new Date()
  });
  
  return {
    content: [{
      type: 'text',
      text: `Analysis complete. View results at: ${resourceUri}`
    }]
  };
}
```

**Real-World Example:**
Imagine building a code review assistant. The AI uses the `analyze_code` tool to examine a file, which creates an analysis resource. Then it uses the `read_resource` capability to access the detailed analysis, and finally uses a `generate_report` tool to create a formatted review document. Each step builds on the previous one, creating a powerful workflow.

### Prompt-Driven Workflows

Prompts act like a GPS for complex tasks—they provide step-by-step directions to help the AI navigate from problem to solution. Just as GPS breaks down a long journey into manageable turns ("In 500 feet, turn left, then continue straight for 2 miles"), prompts break down complex workflows into clear, actionable steps.

Prompts can guide AI models through complex multi-step processes:

```typescript
// Multi-step workflow prompt
const workflowPrompt = {
  name: 'debug_issue',
  arguments: [
    { name: 'error_message', required: true },
    { name: 'component', required: false }
  ],
  messages: [
    {
      role: 'system',
      content: {
        type: 'text',
        text: 'You are a debugging expert. Follow systematic troubleshooting procedures.'
      }
    },
    {
      role: 'user',
      content: {
        type: 'text',
        text: `Debug this ${component || 'system'} issue: "${error_message}"
               
               Follow this systematic approach:
               1. Use search_files to find relevant code files
               2. Use read_file to examine the problematic code
               3. Use get_logs to check for related errors
               4. Use check_dependencies to verify system state
               5. Provide a diagnosis with specific fix recommendations`
      }
    }
  ]
};
```

**Practical Application:**
When a developer encounters a bug, they can invoke the `debug_issue` prompt with the error message. The AI follows the structured workflow, systematically using different tools to investigate, and provides a comprehensive diagnosis. This ensures consistent, thorough debugging every time.

## Performance and Security: Building for the Real World

Building an MCP server is like constructing a building—you need both a solid foundation (security) and efficient systems (performance) to handle real-world usage. Just as architects consider both structural integrity and energy efficiency, MCP developers must balance security and performance.

### Performance Optimization

Performance optimization is like organizing your kitchen for efficiency. Just as a chef keeps frequently used ingredients within easy reach and pre-prepares common components, your MCP server should cache expensive operations and optimize for common use patterns.

```typescript
// Implement caching for expensive operations
const cache = new Map<string, { data: any; timestamp: number }>();

async function cachedOperation(key: string, operation: () => Promise<any>) {
  const cached = cache.get(key);
  const now = Date.now();
  
  if (cached && (now - cached.timestamp) < 300000) { // 5 min cache
    return cached.data;
  }
  
  const data = await operation();
  cache.set(key, { data, timestamp: now });
  return data;
}
```

### Security Best Practices

Security in MCP servers is like being a careful bouncer at an exclusive club. You need to check IDs (validate inputs), ensure people don't wander into restricted areas (prevent path traversal), and maintain order while still providing good service to legitimate guests.

```typescript
// Input validation and sanitization
function validateFilePath(path: string): string {
  // Prevent path traversal
  const normalized = path.normalize(path);
  if (normalized.includes('..') || normalized.startsWith('/')) {
    throw new Error('Invalid path: path traversal detected');
  }
  
  // Ensure path is within allowed directory
  const resolved = path.resolve(ALLOWED_ROOT, normalized);
  if (!resolved.startsWith(ALLOWED_ROOT)) {
    throw new Error('Access denied: path outside allowed directory');
  }
  
  return resolved;
}
```

## Putting It All Together: A Practical Example

Let's walk through building a complete MCP server for a development team's needs:

**Scenario**: Your team needs an AI assistant that can help with code reviews, manage project documentation, and monitor system health.

**Transport Decision**: 
- Use **HTTP transport** because multiple developers need access
- Deploy on your internal cloud infrastructure
- Enable HTTPS with team authentication

**Component Design**:

1. **Tools** (Actions the AI can perform):
   ```typescript
   // Code analysis
   'analyze_code' - examines code quality and security
   'run_tests' - executes test suites
   'deploy_staging' - deploys to staging environment
   
   // Documentation
   'update_docs' - modifies project documentation
   'generate_changelog' - creates release notes
   
   // Monitoring  
   'check_system_health' - monitors server status
   'get_error_logs' - retrieves recent error logs
   ```

2. **Resources** (Information the AI can access):
   ```typescript
   // Code and documentation
   'file://src/**/*.ts' - source code files
   'file://docs/**/*.md' - documentation files
   
   // System data
   'api://monitoring/metrics' - performance metrics
   'api://logs/errors/recent' - recent error logs
   'db://deployments/history' - deployment history
   ```

3. **Prompts** (Structured workflows):
   ```typescript
   'code_review_checklist' - systematic code review process
   'incident_response' - structured incident handling
   'release_preparation' - pre-release validation steps
   ```

**Result**: Developers can ask the AI to "review this pull request" (uses code_review_checklist prompt), "check if the system is healthy" (uses monitoring tools and resources), or "prepare for release" (follows release_preparation workflow).

## Conclusion

Building effective MCP servers is like designing a well-equipped workshop—you need the right tools for the job, organized materials you can easily find, and proven procedures for complex tasks. 

**Key Takeaways:**
- **Transport choice matters**: STDIO for local speed, HTTP for remote access, SSE for real-time updates
- **Design for clarity**: Each tool should have a single, clear purpose
- **Organize systematically**: Use consistent URI patterns for resources
- **Guide with prompts**: Provide structured workflows for complex tasks
- **Secure by default**: Always validate inputs and control access
- **Optimize for real use**: Cache expensive operations and monitor performance

Start simple with a few essential tools and resources, then expand based on actual usage patterns. The best MCP servers solve real problems elegantly rather than trying to do everything at once.