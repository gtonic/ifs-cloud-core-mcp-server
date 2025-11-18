# 🐳 Docker Deployment Guide

## Overview

The IFS Cloud MCP Server can be deployed as a Docker container with HTTP streaming support, making it easy to run server-side for multiple clients to access.

## Prerequisites

Before running the Docker container, you need to:

1. **Import IFS Cloud source files** into your local data directory
2. **Generate search indexes** for the version you want to use

### Option 1: Prepare Data on Host (Recommended)

This is faster and more reliable:

```bash
# Import IFS Cloud ZIP file
python -m src.ifs_cloud_mcp_server.main import /path/to/ifs-cloud-25.1.0.zip

# Generate search indexes (this will take some time)
python -m src.ifs_cloud_mcp_server.main download --version 25.1.0

# Check the data directory location
ls ~/.local/share/ifs_cloud_mcp_server/versions/25.1.0/
# Should see: bm25s/, faiss/, ranked.jsonl, analysis/
```

### Option 2: Auto-Generate on Container Start

Set `AUTO_GENERATE_INDEXES=true` to generate indexes automatically (slower, but convenient):

```bash
docker run -d \
  -p 8000:8000 \
  -e VERSION=25.1.0 \
  -e AUTO_GENERATE_INDEXES=true \
  -v ifs-mcp-data:/home/mcp/.local/share/ifs_cloud_mcp_server \
  --name ifs-mcp-server \
  ifs-cloud-mcp-server:latest
```

⚠️ **Warning**: Auto-generation can take 30+ minutes for large IFS Cloud installations.

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the server
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

### Using Docker Directly

```bash
# Build the image
docker build -t ifs-cloud-mcp-server:latest .

# Run the container with mounted data directory
docker run -d \
  -p 8000:8000 \
  -e VERSION=25.1.0 \
  -v ~/.local/share/ifs_cloud_mcp_server:/home/mcp/.local/share/ifs_cloud_mcp_server \
  --name ifs-mcp-server \
  ifs-cloud-mcp-server:latest

# View logs
docker logs -f ifs-mcp-server

# Stop the container
docker stop ifs-mcp-server
```

## Configuration

### Environment Variables

- `VERSION`: IFS Cloud version to use (default: `25.1.0`)
- `AUTO_GENERATE_INDEXES`: Set to `true` to generate indexes on startup if missing (default: `false`)
- `PYTHONUNBUFFERED`: Set to `1` for real-time logging

### Volume Mounts

**Important**: The server requires data in `/home/mcp/.local/share/ifs_cloud_mcp_server`.

#### Mount host directory (recommended):
```bash
docker run -d \
  -p 8000:8000 \
  -v ~/.local/share/ifs_cloud_mcp_server:/home/mcp/.local/share/ifs_cloud_mcp_server \
  ifs-cloud-mcp-server:latest
```

#### Use Docker volume:
```bash
docker run -d \
  -p 8000:8000 \
  -v ifs-mcp-data:/home/mcp/.local/share/ifs_cloud_mcp_server \
  ifs-cloud-mcp-server:latest
```

### Custom Port

Change the exposed port by modifying the port mapping:

```bash
docker run -d \
  -p 9000:8000 \
  ifs-cloud-mcp-server:latest
```

## HTTP Transport Modes

The server supports three transport modes:

### 1. Stdio (Default for CLI)

Standard input/output transport for local MCP clients:

```bash
python -m ifs_cloud_mcp_server.main server --version 25.1.0 --transport stdio
```

### 2. SSE (Server-Sent Events)

HTTP-based streaming for real-time updates:

```bash
python -m ifs_cloud_mcp_server.main server \
  --version 25.1.0 \
  --transport sse \
  --host 0.0.0.0 \
  --port 8000
```

### 3. Streamable HTTP (Recommended for Docker)

HTTP streaming optimized for server-side deployment:

```bash
python -m ifs_cloud_mcp_server.main server \
  --version 25.1.0 \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000
```

## Using Taskfile

The project includes a Taskfile for common operations:

### Install Taskfile

```bash
# On macOS
brew install go-task/tap/go-task

# On Linux
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Or using Go
go install github.com/go-task/task/v3/cmd/task@latest
```

### Common Tasks

```bash
# Build Docker image
task docker-build

# Run Docker container
task docker-run

# Run with custom version
VERSION=24.2.1 task docker-run

# Run in stdio mode (for testing)
task docker-run-stdio

# Open shell in container
task docker-shell

# Clean up Docker resources
task docker-clean

# Run all CI checks
task ci

# Build and test everything
task build-all
```

## Development

### Build Image

```bash
task docker-build
# or
docker build -t ifs-cloud-mcp-server:latest .
```

### Run Tests

```bash
# Install dev dependencies
task install

# Run tests
task test

# Run with coverage
task test-coverage
```

### Code Quality

```bash
# Format code
task format

# Lint code
task lint

# Type checking
task type-check
```

## Production Deployment

### Using Docker Compose with Custom Configuration

Create a `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  ifs-mcp-server:
    environment:
      - VERSION=25.1.0
    ports:
      - "8000:8000"
    volumes:
      - ./data:/home/mcp/.local/share/ifs_cloud_mcp_server
    restart: always
```

Then run:

```bash
docker-compose up -d
```

### Health Checks

The container includes health checks that run every 30 seconds. Check status:

```bash
docker inspect --format='{{.State.Health.Status}}' ifs-mcp-server
```

### Logs

View real-time logs:

```bash
docker logs -f ifs-mcp-server
```

View last 100 lines:

```bash
docker logs --tail 100 ifs-mcp-server
```

## Troubleshooting

### Container Won't Start

Check logs:

```bash
docker logs ifs-mcp-server
```

### Port Already in Use

Change the port mapping:

```bash
docker run -d -p 9000:8000 ifs-cloud-mcp-server:latest
```

### Permission Issues

The container runs as non-root user `mcp` (UID 1000). Ensure mounted volumes have correct permissions:

```bash
chown -R 1000:1000 ./data
```

### Version Not Found

Ensure the version data exists in the mounted volume:

```bash
docker exec ifs-mcp-server ls -la /home/mcp/.local/share/ifs_cloud_mcp_server/versions/
```

## Security Considerations

1. **Non-Root User**: Container runs as user `mcp` (UID 1000)
2. **No Secrets**: Don't include sensitive data in the image
3. **Network Isolation**: Use Docker networks for service isolation
4. **Volume Permissions**: Ensure proper permissions on mounted volumes
5. **Health Checks**: Monitor container health and restart on failure

## Advanced Usage

### Multi-Stage Build

The Dockerfile uses multi-stage builds to minimize image size:

- **Builder stage**: Compiles dependencies
- **Runtime stage**: Only includes necessary runtime files

### Custom Base Image

To use a different Python version, modify the Dockerfile:

```dockerfile
FROM python:3.11-slim AS builder
...
FROM python:3.11-slim
```

### Resource Limits

Set resource limits in docker-compose.yml:

```yaml
services:
  ifs-mcp-server:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Next Steps

- Review the [main README](README.md) for feature documentation
- Check the [CLI API specification](CLI_API_SPECIFICATION.md)
- Explore [Taskfile.yml](Taskfile.yml) for all available tasks
