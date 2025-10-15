"""
Integration tests for nested toctree relative path generation (Issue #5).

Tests the complete build process with nested directory structures,
verifying that relative paths in #include() directives are correctly generated.

Requirements: 3.1, 3.2, 3.3, 5.1, 5.2
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir():
    """Return the path to tests/fixtures/ directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def nested_toctree_dir(fixtures_dir):
    """Return the path to integration_nested_toctree test project."""
    return fixtures_dir / "integration_nested_toctree"


@pytest.fixture
def multi_level_dir(fixtures_dir):
    """Return the path to integration_multi_level test project."""
    return fixtures_dir / "integration_multi_level"


@pytest.fixture
def sibling_dir(fixtures_dir):
    """Return the path to integration_sibling test project."""
    return fixtures_dir / "integration_sibling"


@pytest.fixture
def temp_build_dir(tmp_path):
    """Provide a temporary directory for build output."""
    return tmp_path / "_build"


class TestNestedToctreeIntegration:
    """Test nested toctree with relative path generation (Task 4.1, Issue #5)."""

    def test_nested_toctree_fixture_exists(self, nested_toctree_dir):
        """Test that the nested toctree fixture has required files."""
        assert (nested_toctree_dir / "conf.py").exists()
        assert (nested_toctree_dir / "index.rst").exists()
        assert (nested_toctree_dir / "chapter1" / "index.rst").exists()
        assert (nested_toctree_dir / "chapter1" / "section1.rst").exists()
        assert (nested_toctree_dir / "chapter1" / "section2.rst").exists()

    def test_sphinx_build_succeeds(self, nested_toctree_dir, temp_build_dir):
        """Test that sphinx-build succeeds for nested toctree project."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(nested_toctree_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build failed:\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    def test_chapter1_index_has_relative_includes(
        self, nested_toctree_dir, temp_build_dir
    ):
        """
        Test that chapter1/index.typ uses relative paths for same-directory files.

        Expected: #include("section1.typ") and #include("section2.typ")
        NOT: #include("chapter1/section1.typ")

        Requirements: 3.1
        """
        # Build the project
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(nested_toctree_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
        )

        # Read generated chapter1/index.typ
        chapter1_index = temp_build_dir / "chapter1" / "index.typ"
        assert chapter1_index.exists(), "chapter1/index.typ was not generated"

        content = chapter1_index.read_text()

        # Verify relative paths (same directory - no "chapter1/" prefix)
        assert (
            '#include("section1.typ")' in content
        ), "Expected relative path #include(\"section1.typ\") not found"
        assert (
            '#include("section2.typ")' in content
        ), "Expected relative path #include(\"section2.typ\") not found"

        # Ensure absolute paths are NOT used
        assert (
            '#include("chapter1/section1.typ")' not in content
        ), "Unexpected absolute path found (should be relative)"
        assert (
            '#include("chapter1/section2.typ")' not in content
        ), "Unexpected absolute path found (should be relative)"

    def test_root_index_has_correct_include(self, nested_toctree_dir, temp_build_dir):
        """
        Test that index.typ correctly includes chapter1/index.typ.

        Requirements: 3.3
        """
        # Build the project
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(nested_toctree_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
        )

        # Read generated index.typ
        index_typ = temp_build_dir / "index.typ"
        assert index_typ.exists(), "index.typ was not generated"

        content = index_typ.read_text()

        # Root directory should use subdirectory path
        assert (
            '#include("chapter1/index.typ")' in content
        ), "Expected #include(\"chapter1/index.typ\") not found in root index"


class TestMultiLevelNestedToctree:
    """Test 3-level nested toctree (Task 4.2)."""

    def test_multi_level_fixture_exists(self, multi_level_dir):
        """Test that the multi-level fixture has required files."""
        assert (multi_level_dir / "conf.py").exists()
        assert (multi_level_dir / "index.rst").exists()
        assert (multi_level_dir / "part1" / "index.rst").exists()
        assert (multi_level_dir / "part1" / "chapter1" / "index.rst").exists()

    def test_sphinx_build_succeeds(self, multi_level_dir, temp_build_dir):
        """Test that sphinx-build succeeds for multi-level nested project."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(multi_level_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build failed:\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    def test_deep_nested_relative_paths(self, multi_level_dir, temp_build_dir):
        """
        Test that part1/chapter1/index.typ uses relative paths for sections.

        Requirements: 3.2
        """
        # Build the project
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(multi_level_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
        )

        # Read generated part1/chapter1/index.typ
        chapter1_index = temp_build_dir / "part1" / "chapter1" / "index.typ"
        assert chapter1_index.exists(), "part1/chapter1/index.typ was not generated"

        content = chapter1_index.read_text()

        # Verify relative paths (same directory)
        assert (
            '#include("section1.typ")' in content
        ), "Expected relative path #include(\"section1.typ\") not found"
        assert (
            '#include("section2.typ")' in content
        ), "Expected relative path #include(\"section2.typ\") not found"


class TestSiblingDirectoryReferences:
    """Test cross-directory toctree references (Task 4.3)."""

    def test_sibling_fixture_exists(self, sibling_dir):
        """Test that the sibling directory fixture has required files."""
        assert (sibling_dir / "conf.py").exists()
        assert (sibling_dir / "index.rst").exists()
        assert (sibling_dir / "chapter1" / "doc1.rst").exists()
        assert (sibling_dir / "chapter2" / "doc2.rst").exists()

    def test_sphinx_build_succeeds(self, sibling_dir, temp_build_dir):
        """Test that sphinx-build succeeds for sibling directory project."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(sibling_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build failed:\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    def test_cross_directory_relative_path(self, sibling_dir, temp_build_dir):
        """
        Test that chapter1/doc1.typ uses "../chapter2/doc2.typ" for sibling reference.

        Requirements: 3.2, 3.3
        """
        # Build the project
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(sibling_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
        )

        # Read generated chapter1/doc1.typ
        doc1_typ = temp_build_dir / "chapter1" / "doc1.typ"
        assert doc1_typ.exists(), "chapter1/doc1.typ was not generated"

        content = doc1_typ.read_text()

        # Verify cross-directory relative path
        assert (
            '#include("../chapter2/doc2.typ")' in content
        ), "Expected relative path #include(\"../chapter2/doc2.typ\") not found"
