#!/bin/bash
set -e

# Default VERSION if not set
VERSION="${VERSION:-25.1.0}"

# Data directory
DATA_DIR="/home/mcp/.local/share/ifs_cloud_mcp_server/versions/${VERSION}"

# Check if version directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "❌ Version directory not found: $DATA_DIR"
    echo ""
    echo "To use this container, you need to:"
    echo "1. Mount a volume with pre-imported IFS Cloud files:"
    echo "   docker run -v /path/to/data:/home/mcp/.local/share/ifs_cloud_mcp_server -p 8000:8000 ifs-cloud-mcp-server"
    echo ""
    echo "2. Or import files and generate indexes on your host machine first:"
    echo "   python -m src.ifs_cloud_mcp_server.main import <zip_file>"
    echo "   python -m src.ifs_cloud_mcp_server.main download --version ${VERSION}"
    echo ""
    echo "3. Then mount that data directory into the container"
    exit 1
fi

# Check if indexes exist
BM25S_DIR="$DATA_DIR/bm25s"
PAGERANK_FILE="$DATA_DIR/ranked.jsonl"

if [ ! -d "$BM25S_DIR" ] || [ ! -f "$PAGERANK_FILE" ]; then
    echo "⚠️  Version $VERSION found but missing search indexes"
    echo ""
    
    # Check if AUTO_GENERATE_INDEXES is set
    if [ "$AUTO_GENERATE_INDEXES" = "true" ]; then
        echo "🔄 AUTO_GENERATE_INDEXES=true, generating indexes..."
        echo "⚠️  This may take a long time depending on the size of your IFS Cloud installation"
        echo ""
        
        # Run the download command which now generates indexes locally
        python3 -m ifs_cloud_mcp_server.main download --version "$VERSION"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Indexes generated successfully!"
        else
            echo ""
            echo "❌ Failed to generate indexes"
            exit 1
        fi
    else
        echo "To generate indexes, you have two options:"
        echo ""
        echo "Option 1: Set AUTO_GENERATE_INDEXES=true to generate on container start (slow):"
        echo "   docker run -e AUTO_GENERATE_INDEXES=true -e VERSION=${VERSION} -p 8000:8000 ifs-cloud-mcp-server"
        echo ""
        echo "Option 2: Generate indexes on your host machine first (recommended):"
        echo "   python -m src.ifs_cloud_mcp_server.main download --version ${VERSION}"
        echo "   Then mount the data directory into the container"
        exit 1
    fi
fi

# All checks passed, start the server
echo "✅ Starting IFS Cloud MCP Server"
echo "   Version: $VERSION"
echo "   Transport: ${TRANSPORT:-streamable-http}"
echo "   Host: ${HOST:-0.0.0.0}"
echo "   Port: ${PORT:-8000}"
echo ""

# If the first argument is python3 and contains "server" command, inject --version
if [ "$1" = "python3" ] && echo "$*" | grep -q "server"; then
    # Check if --version is already in the arguments
    if ! echo "$*" | grep -q "\--version"; then
        # Find the position to insert --version (after "server")
        shift  # Remove python3
        shift  # Remove -m
        shift  # Remove ifs_cloud_mcp_server.main
        shift  # Remove server
        
        # Execute with version injected
        exec python3 -m ifs_cloud_mcp_server.main server --version "$VERSION" "$@"
    else
        # Version already specified, execute as-is
        exec "$@"
    fi
else
    # Not the default server command, execute as-is
    exec "$@"
fi
