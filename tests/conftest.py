"""Pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """Create a temporary directory for test data."""
    return tmp_path_factory.mktemp("test_data")


@pytest.fixture
def mock_version_dir(tmp_path):
    """Create a mock version directory structure."""
    version_dir = tmp_path / "versions" / "test_version"
    version_dir.mkdir(parents=True)
    
    # Create required subdirectories
    source_dir = version_dir / "source"
    source_dir.mkdir()
    
    analysis_dir = version_dir / "analysis"
    analysis_dir.mkdir()
    
    bm25s_dir = version_dir / "bm25s"
    bm25s_dir.mkdir()
    
    faiss_dir = version_dir / "faiss"
    faiss_dir.mkdir()
    
    return version_dir


@pytest.fixture
def sample_plsql_file(tmp_path):
    """Create a sample PLSQL file for testing."""
    plsql_file = tmp_path / "test.plsql"
    plsql_file.write_text("""
-- Sample PLSQL file
PROCEDURE Test_Procedure___ IS
BEGIN
   NULL;
END Test_Procedure___;
""")
    return plsql_file
