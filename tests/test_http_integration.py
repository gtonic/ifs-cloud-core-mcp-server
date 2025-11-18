"""Integration tests for HTTP transport."""

import pytest
import asyncio
import httpx
from pathlib import Path
import sys
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestHTTPIntegration:
    """Integration tests for HTTP-based transports."""

    @pytest.fixture
    def mock_version_path(self, tmp_path):
        """Create a mock version path with necessary directories."""
        version_dir = tmp_path / "test_version"
        version_dir.mkdir()
        
        # Create mock directories
        bm25s_dir = version_dir / "bm25s"
        bm25s_dir.mkdir()
        (bm25s_dir / "index.h5").touch()
        
        faiss_dir = version_dir / "faiss"
        faiss_dir.mkdir()
        (faiss_dir / "index.faiss").touch()
        
        # Create mock pagerank file
        (version_dir / "ranked.jsonl").touch()
        
        return version_dir

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_http_server_initialization(self, mock_fastmcp, mock_version_path):
        """Test HTTP server can be initialized."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer(version_path=mock_version_path)
        
        # Verify server can be configured for HTTP
        assert server is not None
        assert server.version_path == mock_version_path

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_http_transport_parameters(self, mock_fastmcp):
        """Test HTTP transport accepts correct parameters."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer()
        
        # Test with custom host and port
        server.run(
            transport_type="streamable-http",
            host="127.0.0.1",
            port=9999
        )
        
        mock_mcp_instance.run.assert_called_once()
        call_kwargs = mock_mcp_instance.run.call_args[1]
        assert call_kwargs["transport"] == "streamable-http"
        assert call_kwargs["host"] == "127.0.0.1"
        assert call_kwargs["port"] == 9999

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_default_http_parameters(self, mock_fastmcp):
        """Test HTTP transport uses default parameters."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        mock_mcp_instance = Mock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        server = IFSCloudMCPServer()
        
        # Test with defaults
        server.run(transport_type="streamable-http")
        
        mock_mcp_instance.run.assert_called_once()
        call_kwargs = mock_mcp_instance.run.call_args[1]
        assert call_kwargs["transport"] == "streamable-http"
        assert call_kwargs["host"] == "0.0.0.0"
        assert call_kwargs["port"] == 8000


class TestSearchIntegration:
    """Integration tests for search functionality."""

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    def test_search_engine_lazy_loading(self, mock_fastmcp):
        """Test search engine is lazy loaded."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        server = IFSCloudMCPServer()
        
        # Initially not initialized
        assert server.search_engine is None
        assert server._search_engine_initialized is False

    @patch("ifs_cloud_mcp_server.server_fastmcp.FastMCP")
    @patch("ifs_cloud_mcp_server.hybrid_search.HybridSearchEngine")
    def test_search_engine_initialization(self, mock_search_engine, mock_fastmcp, tmp_path):
        """Test search engine initialization when FAISS directory exists."""
        from ifs_cloud_mcp_server.server_fastmcp import IFSCloudMCPServer
        
        # Create mock FAISS directory
        faiss_dir = tmp_path / "faiss"
        faiss_dir.mkdir()
        (faiss_dir / "index.faiss").touch()
        
        server = IFSCloudMCPServer(version_path=tmp_path)
        server._initialize_search_engine()
        
        # Should attempt to create search engine
        assert server._search_engine_initialized is True
