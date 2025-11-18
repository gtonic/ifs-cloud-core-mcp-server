# Examples

This directory contains example scripts demonstrating various features of the IFS Cloud MCP Server.

## test_http_server.py

A simple script that demonstrates the HTTP transport configuration capabilities of the server.

**Usage:**
```bash
python examples/test_http_server.py
```

This script tests:
- Stdio transport configuration
- Streamable-HTTP transport configuration  
- SSE transport configuration

**Output:**
The script verifies that the server can be configured with different transport modes and shows what command would be used to start each mode.

## Running the Actual Server

### Stdio Mode (for local MCP clients)
```bash
python -m ifs_cloud_mcp_server.main server --version 25.1.0
```

### HTTP Streaming Mode (for server-side deployment)
```bash
python -m ifs_cloud_mcp_server.main server \
  --version 25.1.0 \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000
```

### SSE Mode (Server-Sent Events)
```bash
python -m ifs_cloud_mcp_server.main server \
  --version 25.1.0 \
  --transport sse \
  --host 0.0.0.0 \
  --port 8000
```

## Docker Examples

See [../DOCKER.md](../DOCKER.md) for comprehensive Docker deployment examples.

### Quick Docker Start
```bash
# Using docker-compose
docker-compose up -d

# Using docker directly
docker build -t ifs-cloud-mcp-server .
docker run -p 8000:8000 -e VERSION=25.1.0 ifs-cloud-mcp-server
```

## Using Taskfile

The project includes a Taskfile for common operations:

```bash
# Start server in HTTP mode
task server-http

# Start server in SSE mode
task server-sse

# Run Docker container
task docker-run

# Run all tests
task test
```
