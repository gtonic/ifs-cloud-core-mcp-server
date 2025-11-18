"""Unit tests for IFS Cloud MCP Server."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestIFSCloudMCPServer:
    """Test IFS Cloud MCP Server initialization and configuration."""

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_initialization(self, mock_fastmcp):
        """Test server initializes correctly."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        server = IFSCloudMCPServer(
            version_path=Path("/tmp/test"),
            name="test-server"
        )
        
        assert server.version_path == Path("/tmp/test")
        assert server.search_engine is None
        assert server._search_engine_initialized is False
        mock_fastmcp.assert_called_once()

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_stdio_transport(self, mock_fastmcp):
        """Test server runs with stdio transport."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer()
        server.run(transport_type="stdio")
        
        mock_mcp_instance.run.assert_called_once_with(transport="stdio")

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_http_transport(self, mock_fastmcp):
        """Test server runs with HTTP transport."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer()
        server.run(transport_type="streamable-http", host="localhost", port=9000)
        
        mock_mcp_instance.run.assert_called_once_with(
            transport="streamable-http", 
            host="localhost", 
            port=9000
        )

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_sse_transport(self, mock_fastmcp):
        """Test server runs with SSE transport."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer()
        server.run(transport_type="sse", host="0.0.0.0", port=8000)
        
        mock_mcp_instance.run.assert_called_once_with(
            transport="sse", 
            host="0.0.0.0", 
            port=8000
        )

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_unsupported_transport(self, mock_fastmcp):
        """Test server raises error for unsupported transport."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        server = IFSCloudMCPServer()
        
        with pytest.raises(ValueError, match="Unsupported transport type"):
            server.run(transport_type="invalid")

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_server_cleanup(self, mock_fastmcp):
        """Test server cleanup method."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        server = IFSCloudMCPServer()
        # Should not raise any errors
        server.cleanup()
