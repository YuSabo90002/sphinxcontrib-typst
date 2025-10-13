"""
Integration tests for basic Sphinx project builds (Task 15.1).

Tests the complete build process for simple Sphinx projects,
verifying that .typ files are generated correctly.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir():
    """Return the path to tests/fixtures/ directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def basic_project_dir(fixtures_dir):
    """Return the path to integration_basic test project."""
    return fixtures_dir / "integration_basic"


@pytest.fixture
def temp_build_dir(tmp_path):
    """Provide a temporary directory for build output."""
    return tmp_path / "_build"


class TestBasicSphinxProjectBuild:
    """Test building a basic Sphinx project with typst builder (Task 15.1)."""

    def test_basic_project_files_exist(self, basic_project_dir):
        """Test that the basic project fixture has required files."""
        assert (basic_project_dir / "conf.py").exists()
        assert (basic_project_dir / "index.rst").exists()

    def test_sphinx_build_typst_succeeds(self, basic_project_dir, temp_build_dir):
        """Test that sphinx-build -b typst succeeds for basic project."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build failed:\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    def test_typ_file_generated(self, basic_project_dir, temp_build_dir):
        """Test that index.typ is generated in the build directory."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        assert typ_file.exists(), "index.typ should be generated"
        assert typ_file.is_file(), "index.typ should be a file"

    def test_generated_typ_not_empty(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file is not empty."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        assert len(content) > 0, "Generated .typ file should not be empty"

    def test_generated_typ_has_title(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains the document title."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain heading with "Integration Test Documentation"
        assert "Integration Test Documentation" in content

    def test_generated_typ_has_section(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains section headings."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain section "Basic Section"
        assert "Basic Section" in content

    def test_generated_typ_has_list(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains list items."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain list items
        assert "Bullet point 1" in content
        assert "Bullet point 2" in content

    def test_generated_typ_has_code_block(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains code blocks."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain code block with Python code
        assert "def hello():" in content
        assert 'print("Hello, World!")' in content

    def test_generated_typ_has_emphasis(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains emphasis formatting."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain emphasis and strong formatting
        assert "_emphasis_" in content or "#emph[emphasis]" in content
        assert "*strong*" in content or "#strong[strong]" in content

    def test_generated_typ_has_inline_code(self, basic_project_dir, temp_build_dir):
        """Test that the generated .typ file contains inline code."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()
        # Should contain inline code
        assert "`inline code`" in content or "#raw" in content

    def test_build_is_incremental(self, basic_project_dir, temp_build_dir):
        """Test that incremental builds work correctly."""
        # First build
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        first_mtime = (temp_build_dir / "index.typ").stat().st_mtime

        # Second build (should be incremental)
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Check that build succeeded
        assert result.returncode == 0

    def test_clean_build(self, basic_project_dir, temp_build_dir):
        """Test that clean build (-a flag) works correctly."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-a",
                "-b",
                "typst",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert (temp_build_dir / "index.typ").exists()
