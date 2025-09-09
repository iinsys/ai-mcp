# Best Practices

Recommended patterns and approaches for AI and MCP development.

## General Development Principles

### Code Quality
- **Type hints**: Use type annotations for better IDE support and documentation
- **Documentation**: Write clear docstrings and comments
- **Error handling**: Implement comprehensive error handling and logging
- **Testing**: Include unit tests and integration tests
- **Code style**: Follow language-specific style guides (PEP 8 for Python)

### Project Structure
- **Modular design**: Break code into logical, reusable modules
- **Clear naming**: Use descriptive names for functions, classes, and variables
- **Configuration**: Externalize configuration using files or environment variables
- **Dependencies**: Pin dependency versions and use virtual environments

## MCP Development Best Practices

### Server Design
```python
# Good: Clear, focused server with proper error handling
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    try:
        if name == "process_data":
            # Validate input
            if not arguments.get("data"):
                raise ValueError("Data parameter is required")
            
            # Process with clear steps
            result = process_data(arguments["data"])
            
            # Return structured response
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result))]
            )
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )
```

### Input Validation
```python
# Use Pydantic for robust input validation
from pydantic import BaseModel, Field, validator

class ProcessDataInput(BaseModel):
    data: str = Field(..., description="Data to process")
    format: str = Field(default="json", description="Output format")
    
    @validator('format')
    def validate_format(cls, v):
        if v not in ['json', 'csv', 'xml']:
            raise ValueError('Format must be json, csv, or xml')
        return v
```

### Resource Management
```python
# Proper resource cleanup
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

@server.call_tool()
async def handle_database_query(name: str, arguments: dict):
    async with database_connection() as conn:
        # Use connection safely
        result = await conn.execute(query)
        return result
```

## AI Development Best Practices

### Data Handling
```python
# Process data in chunks for memory efficiency
def process_large_dataset(file_path: Path, chunk_size: int = 1000):
    with open(file_path) as f:
        while True:
            chunk = list(itertools.islice(f, chunk_size))
            if not chunk:
                break
            yield process_chunk(chunk)
```

### Model Integration
```python
# Proper model lifecycle management
class ModelManager:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._model = None
    
    def load_model(self):
        if self._model is None:
            self._model = load_model_from_path(self.model_path)
        return self._model
    
    def predict(self, input_data):
        model = self.load_model()
        return model.predict(input_data)
    
    def cleanup(self):
        if self._model:
            del self._model
            self._model = None
```

### API Integration
```python
# Robust API client with retry logic
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def make_request(self, endpoint: str, data: dict):
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
```

## Security Best Practices

### Input Sanitization
```python
# Always validate and sanitize inputs
import re
from pathlib import Path

def validate_file_path(path_str: str) -> Path:
    # Prevent directory traversal
    if '..' in path_str or path_str.startswith('/'):
        raise ValueError("Invalid path")
    
    # Validate characters
    if not re.match(r'^[a-zA-Z0-9._/-]+$', path_str):
        raise ValueError("Path contains invalid characters")
    
    return Path(path_str)
```

### Secrets Management
```python
# Use environment variables for secrets
import os
from typing import Optional

def get_api_key() -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")
    return api_key

# Never log sensitive information
logger.info(f"Connecting to API with key: {'*' * len(api_key)}")
```

### Access Control
```python
# Implement proper access controls
def check_permissions(user_id: str, resource: str, action: str) -> bool:
    # Implement your permission logic
    permissions = get_user_permissions(user_id)
    return f"{resource}:{action}" in permissions

@server.call_tool()
async def handle_protected_tool(name: str, arguments: dict):
    user_id = arguments.get("user_id")
    if not check_permissions(user_id, "data", "read"):
        raise PermissionError("Insufficient permissions")
    
    # Proceed with tool logic
```

## Performance Best Practices

### Async Programming
```python
# Use async/await for I/O operations
import asyncio
import aiofiles

async def process_files(file_paths: list[Path]):
    tasks = []
    for path in file_paths:
        task = asyncio.create_task(process_single_file(path))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

async def process_single_file(path: Path):
    async with aiofiles.open(path) as f:
        content = await f.read()
        return process_content(content)
```

### Caching
```python
# Implement caching for expensive operations
from functools import lru_cache
import asyncio

# Sync caching
@lru_cache(maxsize=128)
def expensive_computation(input_data: str) -> str:
    # Expensive operation here
    return result

# Async caching with TTL
from cachetools import TTLCache
import time

cache = TTLCache(maxsize=100, ttl=300)  # 5 minute TTL

async def cached_api_call(endpoint: str):
    if endpoint in cache:
        return cache[endpoint]
    
    result = await make_api_call(endpoint)
    cache[endpoint] = result
    return result
```

### Memory Management
```python
# Use generators for large datasets
def read_large_file(file_path: Path):
    with open(file_path) as f:
        for line in f:
            yield process_line(line)

# Process in batches
def process_in_batches(items: list, batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield process_batch(batch)
```

## Testing Best Practices

### Unit Testing
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_tool_call():
    # Arrange
    mock_data = {"key": "value"}
    
    # Act
    with patch('your_module.external_api') as mock_api:
        mock_api.return_value = mock_data
        result = await your_tool_function("test_input")
    
    # Assert
    assert result.content[0].text == "expected_output"
    mock_api.assert_called_once_with("test_input")
```

### Integration Testing
```python
@pytest.mark.asyncio
async def test_server_integration():
    # Test full server workflow
    async with test_server() as server:
        # Test tool listing
        tools = await server.list_tools()
        assert len(tools.tools) > 0
        
        # Test tool execution
        result = await server.call_tool("test_tool", {"param": "value"})
        assert "success" in result.content[0].text
```

## Documentation Best Practices

### Code Documentation
```python
def process_data(data: str, format: str = "json") -> dict:
    """
    Process input data and return structured result.
    
    Args:
        data: Raw input data to process
        format: Output format (json, csv, xml)
    
    Returns:
        Processed data as dictionary
    
    Raises:
        ValueError: If data is empty or format is unsupported
        ProcessingError: If data processing fails
    
    Example:
        >>> result = process_data('{"key": "value"}', "json")
        >>> print(result["processed"])
        True
    """
```

### README Structure
```markdown
# Project Name

Brief description of what the project does.

## Features
- Key feature 1
- Key feature 2

## Installation
Step-by-step installation instructions

## Usage
Basic usage examples with code

## Configuration
Configuration options and examples

## API Reference
Detailed API documentation

## Contributing
How to contribute to the project

## License
License information
```

## Monitoring and Logging

### Structured Logging
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        return json.dumps(log_entry)

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Metrics Collection
```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Function {func.__name__} took {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

Remember: These are guidelines, not rigid rules. Adapt them to your specific use case and requirements.