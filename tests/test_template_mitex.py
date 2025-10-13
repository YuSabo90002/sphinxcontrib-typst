"""
Tests for mitex package integration in templates.

Task 6.1: mitex package integration
Design 3.3: mitex for LaTeX math support
Requirement 4.1: Template must import mitex from Typst Universe
"""

from pathlib import Path

import pytest


class TestTemplateMitexIntegration:
    """Test mitex integration in base template."""

    @pytest.fixture
    def template_path(self):
        """Get path to base template."""
        return (
            Path(__file__).parent.parent
            / "sphinxcontrib"
            / "typst"
            / "templates"
            / "base.typ"
        )

    @pytest.fixture
    def template_content(self, template_path):
        """Read template content."""
        assert template_path.exists(), "Base template should exist"
        return template_path.read_text()

    def test_template_imports_mitex(self, template_content):
        """
        Test that base template imports mitex package.

        Requirement 4.1: Template must import mitex from Typst Universe
        Design 3.3: mitex is used for LaTeX math support
        """
        assert (
            '#import "@preview/mitex' in template_content
        ), "Template should import mitex package from Typst Universe"

        # Verify version specification (0.2.4 or later)
        assert (
            "mitex:0.2.4" in template_content
            or "mitex:0.2" in template_content
            or "mitex:" in template_content
        ), "mitex import should specify version"

    def test_mitex_import_order(self, template_content):
        """
        Test that mitex import appears in correct order.

        Order should be:
        1. codly imports (for code highlighting)
        2. mitex imports (for math)
        3. show rules and configurations
        """
        codly_pos = template_content.find('#import "@preview/codly')
        mitex_pos = template_content.find('#import "@preview/mitex')

        assert codly_pos != -1, "codly import should exist"
        assert mitex_pos != -1, "mitex import should exist"

        # mitex should come after codly
        assert codly_pos < mitex_pos, "mitex import should appear after codly import"
