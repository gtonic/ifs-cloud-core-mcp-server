#!/usr/bin/env python3
"""
Simple test script to verify HTTP server functionality.

This script tests that the server can be initialized with different
transport modes without actually starting the server.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_server_configurations():
    """Test that server can be configured with different transports."""
    from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
    
    print("🧪 Testing IFS Cloud MCP Server Configurations\n")
    
    # Test 1: Stdio transport
    print("1. Testing stdio transport configuration...")
    with patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP") as mock_fastmcp:
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        
        server = IFSCloudMCPServer(name="test-stdio")
        # Don't actually run, just verify it would be called correctly
        print("   ✅ Stdio server created successfully\n")
    
    # Test 2: HTTP (streamable-http) transport
    print("2. Testing streamable-http transport configuration...")
    with patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP") as mock_fastmcp:
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        
        server = IFSCloudMCPServer(name="test-http")
        # Simulate what would happen when run() is called
        try:
            # Mock the run method to prevent actual server start
            mock_mcp.run = Mock()
            server.run(transport_type="streamable-http", host="0.0.0.0", port=8000)
            
            # Verify run was called with correct parameters
            mock_mcp.run.assert_called_once()
            call_kwargs = mock_mcp.run.call_args[1]
            assert call_kwargs["transport"] == "streamable-http"
            assert call_kwargs["host"] == "0.0.0.0"
            assert call_kwargs["port"] == 8000
            print("   ✅ HTTP server would start on 0.0.0.0:8000\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            return False
    
    # Test 3: SSE transport
    print("3. Testing SSE transport configuration...")
    with patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP") as mock_fastmcp:
        mock_mcp = Mock()
        mock_fastmcp.return_value = mock_mcp
        
        server = IFSCloudMCPServer(name="test-sse")
        try:
            mock_mcp.run = Mock()
            server.run(transport_type="sse", host="127.0.0.1", port=9000)
            
            call_kwargs = mock_mcp.run.call_args[1]
            assert call_kwargs["transport"] == "sse"
            assert call_kwargs["host"] == "127.0.0.1"
            assert call_kwargs["port"] == 9000
            print("   ✅ SSE server would start on 127.0.0.1:9000\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            return False
    
    print("=" * 60)
    print("✨ All server configurations tested successfully!")
    print("=" * 60)
    print("\nTo actually start the server, use:")
    print("  python -m ifs_cloud_mcp_server.main server \\")
    print("    --version 25.1.0 \\")
    print("    --transport streamable-http \\")
    print("    --host 0.0.0.0 \\")
    print("    --port 8000")
    
    return True


if __name__ == "__main__":
    success = test_server_configurations()
    sys.exit(0 if success else 1)
