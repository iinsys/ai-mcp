# Troubleshooting Guide

Common issues and solutions for AI and MCP development.

## MCP Server Issues

### Server Won't Start

**Problem**: Server fails to start or crashes immediately.

**Common Causes & Solutions**:

1. **Missing Dependencies**
   ```bash
   # Check if MCP is installed
   pip list | grep mcp
   
   # Install missing dependencies
   pip install mcp
   ```

2. **Python Version Issues**
   ```bash
   # Check Python version (requires 3.8+)
   python --version
   
   # Use correct Python version
   python3.8 server.py
   ```

3. **Import Errors**
   ```python
   # Check for circular imports or missing modules
   import sys
   print(sys.path)
   ```

4. **Port Already in Use**
   ```bash
   # Find process using the port
   lsof -i :8000
   
   # Kill the process or use different port
   kill -9 <PID>
   ```

### Connection Issues

**Problem**: Client can't connect to MCP server.

**Solutions**:

1. **Check Server Status**
   ```bash
   # Verify server is running
   ps aux | grep python
   
   # Check server logs
   tail -f server.log
   ```

2. **Validate Configuration**
   ```json
   {
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["path/to/server.py"],
         "disabled": false
       }
     }
   }
   ```

3. **Test with Simple Client**
   ```python
   # Use the basic client example to test
   python examples/basic/simple-mcp-client.py
   ```

### Tool Call Failures

**Problem**: Tools are listed but fail when called.

**Debugging Steps**:

1. **Check Tool Implementation**
   ```python
   @server.call_tool()
   async def handle_call_tool(name: str, arguments: dict):
       logger.info(f"Tool called: {name} with args: {arguments}")
       try:
           # Your tool logic
           pass
       except Exception as e:
           logger.error(f"Tool {name} failed: {e}")
           raise
   ```

2. **Validate Input Schema**
   ```python
   # Ensure arguments match the schema
   inputSchema = {
       "type": "object",
       "properties": {
           "required_param": {"type": "string"}
       },
       "required": ["required_param"]
   }
   ```

3. **Test Tool Individually**
   ```python
   # Test tool logic outside of MCP
   result = your_tool_function(test_arguments)
   print(result)
   ```

## AI Development Issues

### Memory Problems

**Problem**: Out of memory errors during AI operations.

**Solutions**:

1. **Process Data in Chunks**
   ```python
   def process_large_dataset(data, chunk_size=1000):
       for i in range(0, len(data), chunk_size):
           chunk = data[i:i + chunk_size]
           yield process_chunk(chunk)
   ```

2. **Use Generators**
   ```python
   def read_large_file(file_path):
       with open(file_path) as f:
           for line in f:
               yield process_line(line)
   ```

3. **Clear Variables**
   ```python
   # Explicitly delete large objects
   del large_model
   import gc
   gc.collect()
   ```

### Model Loading Issues

**Problem**: AI models fail to load or perform poorly.

**Solutions**:

1. **Check Model Path**
   ```python
   from pathlib import Path
   
   model_path = Path("models/my_model.pkl")
   if not model_path.exists():
       raise FileNotFoundError(f"Model not found: {model_path}")
   ```

2. **Verify Model Format**
   ```python
   # Check model file integrity
   import pickle
   
   try:
       with open(model_path, 'rb') as f:
           model = pickle.load(f)
   except Exception as e:
       print(f"Model loading failed: {e}")
   ```

3. **Check Dependencies**
   ```python
   # Ensure all model dependencies are available
   import torch  # or tensorflow, sklearn, etc.
   print(torch.__version__)
   ```

### API Integration Problems

**Problem**: External API calls fail or timeout.

**Solutions**:

1. **Add Retry Logic**
   ```python
   import httpx
   from tenacity import retry, stop_after_attempt
   
   @retry(stop=stop_after_attempt(3))
   async def api_call(url, data):
       async with httpx.AsyncClient() as client:
           response = await client.post(url, json=data, timeout=30)
           response.raise_for_status()
           return response.json()
   ```

2. **Check API Keys**
   ```python
   import os
   
   api_key = os.getenv("API_KEY")
   if not api_key:
       raise ValueError("API_KEY environment variable not set")
   ```

3. **Validate Request Format**
   ```python
   # Log request details for debugging
   logger.info(f"Making request to {url} with data: {data}")
   ```

## Installation Issues

### Package Installation Failures

**Problem**: pip install fails or packages conflict.

**Solutions**:

1. **Use Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Update pip**
   ```bash
   pip install --upgrade pip
   ```

3. **Clear pip Cache**
   ```bash
   pip cache purge
   pip install --no-cache-dir package-name
   ```

4. **Check for Conflicts**
   ```bash
   pip check
   pip list --outdated
   ```

### uv Installation Issues

**Problem**: uv package manager not working.

**Solutions**:

1. **Install uv**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Update PATH**
   ```bash
   export PATH="$HOME/.cargo/bin:$PATH"
   source ~/.bashrc  # or ~/.zshrc
   ```

3. **Verify Installation**
   ```bash
   uv --version
   uvx --help
   ```

## Configuration Issues

### Environment Variables

**Problem**: Configuration not loading correctly.

**Solutions**:

1. **Check Environment Variables**
   ```bash
   env | grep API_KEY
   echo $API_KEY
   ```

2. **Use .env Files**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv("API_KEY")
   ```

3. **Validate Configuration**
   ```python
   import yaml
   
   with open("config.yaml") as f:
       config = yaml.safe_load(f)
   
   # Validate required keys
   required_keys = ["api_key", "model_path"]
   for key in required_keys:
       if key not in config:
           raise ValueError(f"Missing required config: {key}")
   ```

### File Permissions

**Problem**: Permission denied errors.

**Solutions**:

1. **Check File Permissions**
   ```bash
   ls -la file.py
   chmod +x script.sh
   ```

2. **Fix Directory Permissions**
   ```bash
   chmod -R 755 project_directory/
   ```

3. **Run with Correct User**
   ```bash
   sudo chown -R $USER:$USER project_directory/
   ```

## Performance Issues

### Slow Response Times

**Problem**: Tools or API calls are too slow.

**Solutions**:

1. **Add Profiling**
   ```python
   import time
   import cProfile
   
   def profile_function(func):
       def wrapper(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           end = time.time()
           print(f"{func.__name__} took {end - start:.2f}s")
           return result
       return wrapper
   ```

2. **Use Async Operations**
   ```python
   import asyncio
   
   async def parallel_operations():
       tasks = [
           asyncio.create_task(operation1()),
           asyncio.create_task(operation2()),
           asyncio.create_task(operation3())
       ]
       results = await asyncio.gather(*tasks)
       return results
   ```

3. **Implement Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def expensive_operation(input_data):
       # Expensive computation
       return result
   ```

### High Memory Usage

**Problem**: Application uses too much memory.

**Solutions**:

1. **Monitor Memory Usage**
   ```python
   import psutil
   import os
   
   process = psutil.Process(os.getpid())
   memory_mb = process.memory_info().rss / 1024 / 1024
   print(f"Memory usage: {memory_mb:.2f} MB")
   ```

2. **Use Memory Profiling**
   ```bash
   pip install memory-profiler
   python -m memory_profiler script.py
   ```

3. **Optimize Data Structures**
   ```python
   # Use generators instead of lists for large datasets
   def process_data():
       for item in large_dataset:
           yield process_item(item)
   ```

## Debugging Techniques

### Enable Debug Logging

```python
import logging

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Use Python Debugger

```python
import pdb

def problematic_function():
    pdb.set_trace()  # Debugger will stop here
    # Your code here
```

### Add Detailed Error Messages

```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed with input {input_data}: {e}")
    logger.error(f"Stack trace:", exc_info=True)
    raise
```

## Getting Help

### Before Asking for Help

1. **Check the logs** for error messages
2. **Search existing issues** in the repository
3. **Try the minimal reproduction** case
4. **Check your configuration** against examples

### When Reporting Issues

Include:
- **Error messages** (full stack trace)
- **Environment details** (OS, Python version, package versions)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Minimal code example** that demonstrates the problem

### Useful Commands for Debugging

```bash
# System information
python --version
pip list
uv --version

# Process information
ps aux | grep python
lsof -i :8000

# Log files
tail -f ~/.kiro/logs/mcp.log
journalctl -f -u your-service

# Network debugging
curl -v http://localhost:8000/health
netstat -tulpn | grep :8000
```

Remember: Most issues have simple solutions. Start with the basics (dependencies, configuration, permissions) before diving into complex debugging.