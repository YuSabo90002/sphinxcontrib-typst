"""
Tests for installation documentation.

This test suite verifies that the installation guide exists and contains
all necessary information per Requirement 12.4.
"""

import os
import re


def test_installation_rst_exists():
    """Test that docs/installation.rst file exists."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    assert os.path.exists(installation_file), (
        "docs/installation.rst does not exist. "
        "Installation guide is required per Requirement 12.4"
    )


def test_installation_has_title():
    """Test that installation.rst has a proper title."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Check for reStructuredText title (text followed by === or similar)
    assert re.search(
        r"^.*\n[=]+\n", content, re.MULTILINE
    ), "installation.rst should have a proper reStructuredText title"


def test_installation_mentions_pip_install():
    """Test that installation guide mentions pip install command."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    assert (
        "pip install" in content
    ), "installation.rst should mention 'pip install' command"
    assert (
        "sphinxcontrib-typst" in content
    ), "installation.rst should mention the package name 'sphinxcontrib-typst'"


def test_installation_mentions_dependencies():
    """Test that installation guide mentions key dependencies."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Key dependencies that should be mentioned
    assert (
        "Sphinx" in content or "sphinx" in content
    ), "installation.rst should mention Sphinx as a dependency"
    assert (
        "Python" in content or "python" in content
    ), "installation.rst should mention Python version requirements"


def test_installation_mentions_pdf_generation():
    """Test that installation guide mentions PDF generation optional dependency."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Should mention typst or PDF generation
    assert (
        "typst" in content.lower() or "pdf" in content.lower()
    ), "installation.rst should mention Typst or PDF generation"


def test_installation_has_requirements_section():
    """Test that installation guide has a requirements or prerequisites section."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Check for common section headers
    has_requirements = (
        "Requirements" in content
        or "Prerequisites" in content
        or "依存関係" in content
        or "requirements" in content.lower()
    )

    assert (
        has_requirements
    ), "installation.rst should have a Requirements or Prerequisites section"


def test_installation_has_installation_steps():
    """Test that installation guide has clear installation steps."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Should have some kind of step-by-step structure
    # Check for numbered sections or code blocks
    has_steps = (
        re.search(r"^\d+\.", content, re.MULTILINE)  # Numbered list
        or re.search(r"^::", content, re.MULTILINE)  # Code block
        or ".. code-block::" in content  # Code block directive
    )

    assert has_steps, (
        "installation.rst should have clear installation steps "
        "(numbered list or code blocks)"
    )


def test_installation_is_valid_rst():
    """Test that installation.rst is valid reStructuredText format."""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    installation_file = os.path.join(docs_dir, "installation.rst")

    with open(installation_file, encoding="utf-8") as f:
        content = f.read()

    # Basic validity checks
    assert (
        len(content) > 100
    ), "installation.rst should have substantial content (> 100 characters)"

    # Should not have common Markdown syntax (we want RST)
    assert not re.search(
        r"^# ", content, re.MULTILINE
    ), "installation.rst should use RST syntax, not Markdown headers"
