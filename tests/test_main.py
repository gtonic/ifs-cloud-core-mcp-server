"""Unit tests for main CLI entry point."""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestCLIArguments:
    """Test command-line argument parsing."""

    def test_version_extraction_from_zip(self):
        """Test version extraction from ZIP file."""
        from ifs_cloud_mcp_server.main import get_version_from_zip
        
        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            get_version_from_zip(Path("/nonexistent.zip"))

    def test_logging_setup(self):
        """Test logging configuration."""
        from ifs_cloud_mcp_server.main import setup_logging
        
        # Should not raise any errors
        setup_logging("INFO")
        setup_logging("DEBUG")
        setup_logging("WARNING")
        setup_logging("ERROR")


class TestDirectoryUtils:
    """Test directory utility functions."""

    def test_get_data_directory(self):
        """Test data directory retrieval."""
        from ifs_cloud_mcp_server.directory_utils import get_data_directory
        
        data_dir = get_data_directory()
        assert isinstance(data_dir, Path)
        assert data_dir.name == "ifs_cloud_mcp_server"

    def test_get_supported_extensions(self):
        """Test supported extensions list."""
        from ifs_cloud_mcp_server.directory_utils import get_supported_extensions
        
        extensions = get_supported_extensions()
        assert isinstance(extensions, set)
        assert ".plsql" in extensions
        assert ".entity" in extensions
        assert ".client" in extensions
        assert ".projection" in extensions
