# Multi-stage Dockerfile for IFS Cloud MCP Server
# Stage 1: Build environment
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY uv.lock* ./
COPY src/ ./src/
COPY README.md ./
COPY LICENSE ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

# Stage 2: Runtime environment
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    mkdir -p /home/mcp/.local/share/ifs_cloud_mcp_server && \
    chown -R mcp:mcp /home/mcp

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY --from=builder /app/src ./src
COPY --from=builder /app/pyproject.toml ./
COPY --from=builder /app/README.md ./
COPY --from=builder /app/LICENSE ./

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER mcp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Expose port for HTTP transport
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Use entrypoint script for validation and setup
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command (can be overridden)
# Usage: docker run -e VERSION=25.1.0 -p 8000:8000 ifs-cloud-mcp-server
CMD ["python3", "-m", "ifs_cloud_mcp_server.main", "server", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
