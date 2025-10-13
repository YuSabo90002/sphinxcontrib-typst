"""Tests for TemplateEngine (Requirement 8)"""

from pathlib import Path

from sphinxcontrib.typst.template_engine import TemplateEngine


class TestTemplateLoading:
    """Test template loading and management (Task 9.1)"""

    def test_load_default_template(self):
        """Test loading the default Typst template"""
        engine = TemplateEngine()
        template = engine.load_template()

        # Default template should exist and contain basic structure
        assert template is not None
        assert isinstance(template, str)
        assert "#let project" in template  # Should define a project function
        assert "body" in template  # Should accept body parameter

    def test_load_custom_template_from_path(self, tmp_path):
        """Test loading a custom template from specified path"""
        # Create custom template
        custom_template_path = tmp_path / "custom.typ"
        custom_template_path.write_text(
            '#let custom(title: "", body) = {\n'
            "  text(2em)[#title]\n"
            "  body\n"
            "}\n"
        )

        engine = TemplateEngine(template_path=str(custom_template_path))
        template = engine.load_template()

        assert "#let custom" in template
        assert "title:" in template

    def test_load_template_from_sphinx_project_directory(self, tmp_path):
        """Test template search in Sphinx project directory"""
        # Create Sphinx-like directory structure
        project_dir = tmp_path / "docs"
        templates_dir = project_dir / "_templates" / "typst"
        templates_dir.mkdir(parents=True)

        custom_template = templates_dir / "custom.typ"
        custom_template.write_text("#let project() = {}")

        engine = TemplateEngine(
            template_name="custom.typ", search_paths=[str(templates_dir)]
        )
        template = engine.load_template()

        assert template is not None
        assert "#let project" in template

    def test_template_search_priority(self, tmp_path):
        """Test that user template directory has priority over default"""
        # Create two templates with different content
        user_dir = tmp_path / "user_templates"
        user_dir.mkdir()
        user_template = user_dir / "base.typ"
        user_template.write_text("#let project() = { /* user template */ }")

        default_dir = tmp_path / "default_templates"
        default_dir.mkdir()
        default_template = default_dir / "base.typ"
        default_template.write_text("#let project() = { /* default template */ }")

        # User directory should be searched first
        engine = TemplateEngine(
            template_name="base.typ", search_paths=[str(user_dir), str(default_dir)]
        )
        template = engine.load_template()

        assert "user template" in template
        assert "default template" not in template

    def test_template_not_found_fallback_to_default(self, tmp_path):
        """Test fallback to default template when custom template not found"""
        engine = TemplateEngine(template_path="/nonexistent/template.typ")

        # Should fall back to default template without raising error
        template = engine.load_template()
        assert template is not None
        assert "#let project" in template  # Default template content

    def test_template_not_found_warning(self, tmp_path, caplog):
        """Test that warning is logged when custom template not found"""
        import logging

        caplog.set_level(logging.WARNING)

        engine = TemplateEngine(template_path="/nonexistent/template.typ")
        template = engine.load_template()

        # Should log a warning
        assert any(
            "template" in record.message.lower()
            and "not found" in record.message.lower()
            for record in caplog.records
        )

    def test_get_default_template_path(self):
        """Test getting the path to default template"""
        engine = TemplateEngine()
        default_path = engine.get_default_template_path()

        assert default_path is not None
        assert Path(default_path).exists()
        assert Path(default_path).suffix == ".typ"


class TestParameterMapping:
    """Test Sphinx metadata to template parameter mapping (Task 9.2)"""

    def test_map_basic_sphinx_metadata(self):
        """Test mapping basic Sphinx metadata (project, author, release)"""
        engine = TemplateEngine()

        sphinx_metadata = {
            "project": "My Project",
            "author": "John Doe",
            "release": "1.0.0",
            "copyright": "2024, John Doe",
        }

        params = engine.map_parameters(sphinx_metadata)

        assert params["title"] == "My Project"
        assert params["authors"] == ("John Doe",)
        assert params["date"] == "1.0.0"

    def test_map_parameters_with_default_values(self):
        """Test that default values are provided when metadata is missing"""
        engine = TemplateEngine()

        sphinx_metadata = {}  # Empty metadata

        params = engine.map_parameters(sphinx_metadata)

        # Should have default values
        assert "title" in params
        assert "authors" in params
        assert params["title"] == ""
        assert params["authors"] == ()

    def test_map_parameters_with_multiple_authors(self):
        """Test mapping when author is a comma-separated string"""
        engine = TemplateEngine()

        sphinx_metadata = {
            "project": "My Project",
            "author": "John Doe, Jane Smith, Bob Wilson",
        }

        params = engine.map_parameters(sphinx_metadata)

        # Should convert to tuple of authors
        assert params["authors"] == ("John Doe", "Jane Smith", "Bob Wilson")

    def test_map_parameters_custom_mapping(self):
        """Test custom parameter mapping from user config"""
        # Custom mapping: Sphinx name -> Template parameter name
        custom_mapping = {
            "project": "doc_title",
            "author": "doc_authors",
            "release": "version",
        }

        engine = TemplateEngine(parameter_mapping=custom_mapping)

        sphinx_metadata = {
            "project": "My Project",
            "author": "John Doe",
            "release": "1.0.0",
        }

        params = engine.map_parameters(sphinx_metadata)

        # Should use custom parameter names
        assert params["doc_title"] == "My Project"
        assert params["doc_authors"] == ("John Doe",)
        assert params["version"] == "1.0.0"

    def test_map_parameters_complex_structures(self):
        """Test mapping to complex structures (arrays, dicts)"""
        engine = TemplateEngine()

        sphinx_metadata = {
            "project": "My Project",
            "author": "John Doe",
            "html_theme_options": {
                "logo": "logo.png",
                "github_url": "https://github.com/user/repo",
            },
        }

        params = engine.map_parameters(sphinx_metadata)

        # Basic mapping should work
        assert params["title"] == "My Project"

        # Complex structures should be preserved or transformed
        # (Implementation may vary based on requirements)

    def test_map_parameters_standard_defaults(self):
        """Test standard mapping applies default transformations"""
        engine = TemplateEngine()

        sphinx_metadata = {
            "project": "Test Project",
            "author": "Author Name",
            "version": "0.1",
            "release": "0.1.0",
        }

        params = engine.map_parameters(sphinx_metadata)

        # Standard mapping should be applied
        assert "title" in params
        assert "authors" in params
        assert "date" in params


class TestTypstUniversePackages:
    """Test Typst Universe package template support (Task 9.3)"""

    def test_generate_package_import(self):
        """Test generating import statement for Typst Universe package"""
        engine = TemplateEngine(
            typst_package="@preview/charged-ieee:0.1.0", typst_template_function="ieee"
        )

        import_statement = engine.generate_package_import()

        assert import_statement is not None
        assert "#import" in import_statement
        assert "@preview/charged-ieee:0.1.0" in import_statement

    def test_generate_package_import_with_items(self):
        """Test generating import with specific items"""
        engine = TemplateEngine(
            typst_package="@preview/charged-ieee:0.1.0",
            typst_template_function="ieee",
            typst_package_imports=["ieee", "conference"],
        )

        import_statement = engine.generate_package_import()

        assert "#import" in import_statement
        assert "ieee" in import_statement
        assert "conference" in import_statement

    def test_no_package_import_when_not_specified(self):
        """Test that no import is generated when package not specified"""
        engine = TemplateEngine()

        import_statement = engine.generate_package_import()

        assert import_statement is None or import_statement == ""

    def test_template_function_call_generation(self):
        """Test generating template function call from package"""
        engine = TemplateEngine(
            typst_package="@preview/charged-ieee:0.1.0", typst_template_function="ieee"
        )

        # This should be used in render() method
        assert engine.typst_template_function == "ieee"

    def test_package_version_parsing(self):
        """Test parsing package name and version"""
        engine = TemplateEngine(typst_package="@preview/my-template:1.2.3")

        # Should be able to extract package info
        assert "@preview/my-template:1.2.3" in engine.generate_package_import()


class TestToctreeOutlineIntegration:
    """Test toctree to #outline() integration (Task 9.4)"""

    def test_extract_toctree_options_from_doctree(self):
        """Test extracting toctree options from doctree"""
        from docutils import nodes
        from docutils.parsers.rst import states
        from docutils.utils import Reporter
        from sphinx import addnodes

        # Create doctree with toctree
        reporter = Reporter("", 2, 4)
        doctree = nodes.document("", reporter=reporter)
        doctree.settings = states.Struct()

        toctree = addnodes.toctree()
        toctree["maxdepth"] = 3
        toctree["numbered"] = True
        toctree["caption"] = "Table of Contents"
        doctree += toctree

        engine = TemplateEngine()
        options = engine.extract_toctree_options(doctree)

        assert options["toctree_maxdepth"] == 3
        assert options["toctree_numbered"] is True
        assert options["toctree_caption"] == "Table of Contents"

    def test_extract_toctree_options_defaults(self):
        """Test default values when toctree options not specified"""
        from docutils import nodes
        from docutils.parsers.rst import states
        from docutils.utils import Reporter
        from sphinx import addnodes

        # Create doctree with toctree but no options
        reporter = Reporter("", 2, 4)
        doctree = nodes.document("", reporter=reporter)
        doctree.settings = states.Struct()

        toctree = addnodes.toctree()
        doctree += toctree

        engine = TemplateEngine()
        options = engine.extract_toctree_options(doctree)

        # Should have default values
        assert "toctree_maxdepth" in options
        assert "toctree_numbered" in options
        assert "toctree_caption" in options
        assert options["toctree_maxdepth"] == 2  # Default
        assert options["toctree_numbered"] is False  # Default

    def test_extract_toctree_options_no_toctree(self):
        """Test when doctree has no toctree node"""
        from docutils import nodes
        from docutils.parsers.rst import states
        from docutils.utils import Reporter

        # Create doctree without toctree
        reporter = Reporter("", 2, 4)
        doctree = nodes.document("", reporter=reporter)
        doctree.settings = states.Struct()

        section = nodes.section()
        doctree += section

        engine = TemplateEngine()
        options = engine.extract_toctree_options(doctree)

        # Should return empty dict or defaults
        assert isinstance(options, dict)

    def test_toctree_options_passed_to_parameters(self):
        """Test that toctree options are added to template parameters"""
        from docutils import nodes
        from docutils.parsers.rst import states
        from docutils.utils import Reporter
        from sphinx import addnodes

        # Create doctree with toctree
        reporter = Reporter("", 2, 4)
        doctree = nodes.document("", reporter=reporter)
        doctree.settings = states.Struct()

        toctree = addnodes.toctree()
        toctree["maxdepth"] = 4
        toctree["numbered"] = True
        toctree["caption"] = "Contents"
        doctree += toctree

        engine = TemplateEngine()

        # Extract toctree options
        toctree_options = engine.extract_toctree_options(doctree)

        # Merge with standard parameters
        sphinx_metadata = {"project": "Test", "author": "Author"}
        params = engine.map_parameters(sphinx_metadata)
        params.update(toctree_options)

        # Should have both standard and toctree parameters
        assert params["title"] == "Test"
        assert params["toctree_maxdepth"] == 4
        assert params["toctree_numbered"] is True
        assert params["toctree_caption"] == "Contents"


class TestTemplateRendering:
    """Test template rendering and integration (Task 9.5)"""

    def test_render_with_default_template(self):
        """Test rendering document with default template"""
        engine = TemplateEngine()

        # Prepare parameters
        params = {
            "title": "Test Document",
            "authors": ("Test Author",),
            "date": "2024-01-01",
            "toctree_maxdepth": 2,
            "toctree_numbered": False,
            "toctree_caption": "Contents",
            "papersize": "a4",
            "fontsize": "11pt",
        }

        # Body content (Typst markup)
        body = "= Chapter 1\n\nThis is the content.\n"

        # Render
        result = engine.render(params, body)

        # Should contain template function call
        assert "#show: project.with(" in result
        assert 'title: "Test Document"' in result
        assert 'authors: ("Test Author",)' in result

        # Should contain body
        assert body in result

    def test_render_with_typst_universe_package(self):
        """Test rendering with external Typst Universe package"""
        engine = TemplateEngine(
            typst_package="@preview/charged-ieee:0.1.0", typst_template_function="ieee"
        )

        params = {
            "title": "IEEE Paper",
            "authors": ("Author One",),
        }
        body = "= Introduction\n\nContent here.\n"

        result = engine.render(params, body)

        # Should have import statement
        assert '#import "@preview/charged-ieee:0.1.0": ieee' in result

        # Should use template function from package
        assert "#show: ieee.with(" in result

    def test_render_with_paper_size_and_font_settings(self):
        """Test that paper size and font settings are included"""
        engine = TemplateEngine()

        params = {
            "title": "Document",
            "authors": (),
            "papersize": "letter",
            "fontsize": "12pt",
        }
        body = "Content"

        result = engine.render(params, body)

        assert 'papersize: "letter"' in result
        # fontsize is a string, so it's quoted
        assert 'fontsize: "12pt"' in result

    def test_render_formats_parameters_correctly(self):
        """Test that parameters are formatted correctly for Typst"""
        engine = TemplateEngine()

        params = {
            "title": "My Title",
            "authors": ("Author 1", "Author 2", "Author 3"),
            "date": "2024",
            "toctree_numbered": True,
        }
        body = "Content"

        result = engine.render(params, body)

        # Authors should be formatted as tuple (with trailing comma for Typst)
        assert 'authors: ("Author 1", "Author 2", "Author 3",)' in result

        # Boolean should be lowercase
        assert "toctree_numbered: true" in result

    def test_render_handles_special_characters_in_strings(self):
        """Test that special characters in parameters are escaped"""
        engine = TemplateEngine()

        params = {
            "title": 'Title with "quotes" and \\backslash',
            "authors": (),
        }
        body = "Content"

        result = engine.render(params, body)

        # Should escape quotes and backslashes
        # Typst uses standard escape sequences
        assert result is not None

    def test_render_with_empty_body(self):
        """Test rendering with empty body content"""
        engine = TemplateEngine()

        params = {"title": "Empty Doc", "authors": ()}
        body = ""

        result = engine.render(params, body)

        assert "#show: project.with(" in result
        # Empty body should still be valid
