"""
Tests for codly package integration in templates.

Task 4.2.1: Template codly integration (forced usage)
Design: design.md 3.5 - codly forced usage for all code blocks
Requirement 7.4: codly package integration for code highlighting
"""

from pathlib import Path

import pytest


class TestTemplateCodelyIntegration:
    """Test codly integration in base template."""

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

    def test_template_imports_codly(self, template_content):
        """
        Test that base template imports codly package.

        Requirement 7.4: Template must import codly from Typst Universe
        Design 3.5: codly is mandatory for all code blocks
        """
        assert (
            '#import "@preview/codly' in template_content
        ), "Template should import codly package from Typst Universe"

        # Verify version specification (1.3.0)
        assert (
            "codly:1.3.0" in template_content
        ), "codly import should specify version 1.3.0"

    def test_template_imports_codly_languages(self, template_content):
        """
        Test that base template imports codly-languages package.

        Requirement 7.4: Template must import codly-languages for language definitions
        Design 3.5: codly-languages provides comprehensive language support
        """
        assert (
            '#import "@preview/codly-languages' in template_content
        ), "Template should import codly-languages package from Typst Universe"

        # Verify version specification (0.1.1)
        assert (
            "codly-languages:0.1.1" in template_content
        ), "codly-languages import should specify version 0.1.1"

    def test_template_initializes_codly(self, template_content):
        """
        Test that base template initializes codly.

        Requirement 7.4: Template must initialize codly with #show rule
        Design 3.5: codly-init must be called before code blocks
        """
        assert (
            "#show: codly-init" in template_content
        ), "Template should initialize codly with #show: codly-init"

    def test_template_configures_codly(self, template_content):
        """
        Test that base template configures codly.

        Requirement 7.4: Template should configure codly settings
        Design 3.5: Default configuration with codly-languages
        """
        # codly() configuration should exist
        assert (
            "#codly(" in template_content
        ), "Template should configure codly with #codly()"

        # Verify codly-languages is used in configuration
        assert (
            "languages: codly-languages" in template_content
        ), "codly configuration should use codly-languages for language definitions"

    def test_codly_setup_before_body(self, template_content):
        """
        Test that codly setup occurs before document body.

        Requirement 7.4: codly must be imported and initialized before body content
        This ensures all code blocks in the body are processed by codly
        """
        # Find positions
        import_pos = template_content.find('#import "@preview/codly')
        init_pos = template_content.find("#show: codly-init")
        # Look for the body content section (after all setup)
        project_func_pos = template_content.find("#let project(")

        assert import_pos != -1, "codly import should exist"
        assert init_pos != -1, "codly init should exist"
        assert project_func_pos != -1, "project function should exist"

        # Verify order: import → init → project function
        # codly setup must be complete before the template function is defined
        assert import_pos < init_pos, "codly import should appear before codly-init"
        assert (
            init_pos < project_func_pos
        ), "codly-init should appear before project function definition"

    def test_codly_configuration_order(self, template_content):
        """
        Test that codly configuration appears in correct order.

        Order should be:
        1. #import "@preview/codly:1.3.0"
        2. #import "@preview/codly-languages:0.1.1"
        3. #show: codly-init.with()
        4. #codly(languages: codly-languages)
        5. body content
        """
        codly_import_pos = template_content.find('#import "@preview/codly:1.3.0')
        languages_import_pos = template_content.find(
            '#import "@preview/codly-languages:0.1.1'
        )
        init_pos = template_content.find("#show: codly-init")
        config_pos = template_content.find("#codly(languages: codly-languages)")

        assert codly_import_pos != -1, "codly import should exist"
        assert languages_import_pos != -1, "codly-languages import should exist"
        assert init_pos != -1, "codly-init should exist"
        assert config_pos != -1, "codly configuration should exist"

        # Verify order
        assert (
            codly_import_pos < languages_import_pos
        ), "codly import must appear before codly-languages import"
        assert (
            languages_import_pos < init_pos
        ), "codly-languages import must appear before codly-init"
        assert (
            init_pos < config_pos
        ), "codly-init must appear before codly configuration"
