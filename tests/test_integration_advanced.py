"""
Integration tests for advanced features (Tasks 15.3, 15.4, 15.5).

Tests math, figures, PDF generation, and custom templates.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir():
    """Return the path to tests/fixtures/ directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_build_dir(tmp_path):
    """Provide a temporary directory for build output."""
    return tmp_path / "_build"


class TestMathAndFiguresIntegration:
    """Test integration of math and figures (Task 15.3)."""

    @pytest.fixture
    def math_figures_project_dir(self, fixtures_dir):
        """Return the path to integration_math_figures test project."""
        return fixtures_dir / "integration_math_figures"

    def test_build_with_math_succeeds(self, math_figures_project_dir, temp_build_dir):
        """Test that project with math builds successfully."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(math_figures_project_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build failed:\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    def test_generated_has_inline_math(self, math_figures_project_dir, temp_build_dir):
        """Test that generated output contains inline math."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(math_figures_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()

        # Should contain math content
        assert "E = mc^2" in content or "#mi" in content

    def test_generated_has_block_math(self, math_figures_project_dir, temp_build_dir):
        """Test that generated output contains block math."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(math_figures_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()

        # Should contain integral formula
        assert "\\int" in content or "integral" in content or "#mitex" in content

    def test_generated_has_table(self, math_figures_project_dir, temp_build_dir):
        """Test that generated output contains table."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(math_figures_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()

        # Should contain table content
        assert "Column 1" in content
        assert "Data 1" in content

    def test_generated_has_code_and_math(
        self, math_figures_project_dir, temp_build_dir
    ):
        """Test that code blocks and math can coexist."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typst",
                str(math_figures_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        typ_file = temp_build_dir / "index.typ"
        content = typ_file.read_text()

        # Should contain both code and math
        assert "def integrate" in content
        assert "f(x) = x^2" in content or "f(x)" in content


class TestPDFGenerationIntegration:
    """Test PDF generation integration (Task 15.4)."""

    @pytest.fixture
    def basic_project_dir(self, fixtures_dir):
        """Return the path to integration_basic test project."""
        return fixtures_dir / "integration_basic"

    def test_typstpdf_builder_succeeds(self, basic_project_dir, temp_build_dir):
        """Test that sphinx-build -b typstpdf succeeds."""
        result = subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typstpdf",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"sphinx-build -b typstpdf failed:\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    def test_pdf_file_generated(self, basic_project_dir, temp_build_dir):
        """Test that PDF file is generated."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typstpdf",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        pdf_file = temp_build_dir / "index.pdf"
        assert pdf_file.exists(), "index.pdf should be generated"
        assert pdf_file.is_file(), "index.pdf should be a file"

    def test_pdf_file_not_empty(self, basic_project_dir, temp_build_dir):
        """Test that generated PDF is not empty."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typstpdf",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        pdf_file = temp_build_dir / "index.pdf"
        assert pdf_file.stat().st_size > 0, "PDF file should not be empty"

    def test_pdf_has_magic_number(self, basic_project_dir, temp_build_dir):
        """Test that generated file is a valid PDF."""
        subprocess.run(
            [
                "uv",
                "run",
                "sphinx-build",
                "-b",
                "typstpdf",
                str(basic_project_dir),
                str(temp_build_dir),
            ],
            check=True,
            capture_output=True,
        )

        pdf_file = temp_build_dir / "index.pdf"
        with open(pdf_file, "rb") as f:
            magic = f.read(4)
        assert magic == b"%PDF", "File should start with PDF magic number"


class TestCustomTemplateIntegration:
    """Test custom template integration (Task 15.5)."""

    @pytest.fixture
    def basic_project_dir(self, fixtures_dir):
        """Return the path to integration_basic test project."""
        return fixtures_dir / "integration_basic"

    def test_default_template_works(self, basic_project_dir, temp_build_dir):
        """Test that default template is used when no custom template specified."""
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

        assert result.returncode == 0
        assert (temp_build_dir / "index.typ").exists()

    def test_generated_uses_template(self, basic_project_dir, temp_build_dir):
        """Test that generated output uses template structure."""
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

        # Template should set up document with proper structure
        # Default template doesn't have special markers, but content should be formatted
        assert len(content) > 0
        assert "=" in content  # Should have headings

    def test_template_has_codly_import(self, basic_project_dir, temp_build_dir):
        """Test that template includes codly import (if using default template)."""
        # Note: This test verifies template integration indirectly
        # by checking that code blocks work (which require codly)
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

        # Should have code blocks that work with codly
        assert "def hello():" in content  # Code from fixture
