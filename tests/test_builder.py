"""
Tests for TypstBuilder class.
"""

from sphinx.builders import Builder


def test_typst_builder_can_be_imported():
    """Test that TypstBuilder can be imported."""
    from sphinxcontrib.typst.builder import TypstBuilder

    assert TypstBuilder is not None
    assert issubclass(TypstBuilder, Builder)


def test_typst_builder_has_correct_attributes():
    """Test that TypstBuilder has the correct class attributes."""
    from sphinxcontrib.typst.builder import TypstBuilder

    assert TypstBuilder.name == "typst"
    assert TypstBuilder.format == "typst"
    assert TypstBuilder.out_suffix == ".typ"


def test_typst_builder_has_required_methods():
    """Test that TypstBuilder implements required methods."""
    from sphinxcontrib.typst.builder import TypstBuilder

    # Check that required methods exist
    assert hasattr(TypstBuilder, "init")
    assert hasattr(TypstBuilder, "get_outdated_docs")
    assert hasattr(TypstBuilder, "get_target_uri")
    assert hasattr(TypstBuilder, "prepare_writing")
    assert hasattr(TypstBuilder, "write_doc")
    assert hasattr(TypstBuilder, "finish")


def test_typst_builder_registration(temp_sphinx_app):
    """Test that TypstBuilder can be registered with Sphinx."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app

    # Builder should already be registered by the extension setup
    # Check that the builder is registered
    assert "typst" in app.registry.builders
    assert app.registry.builders["typst"] == TypstBuilder


def test_typst_builder_initialization(temp_sphinx_app):
    """Test that TypstBuilder can be initialized."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app

    # Create a builder instance with app and env
    builder = TypstBuilder(app, app.env)

    assert builder is not None
    assert builder.name == "typst"
    assert builder.app == app


def test_get_outdated_docs_returns_iterator(temp_sphinx_app):
    """Test that get_outdated_docs returns an iterator."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)

    # Initialize builder
    builder.init()

    # get_outdated_docs should return an iterator
    result = builder.get_outdated_docs()
    assert hasattr(result, "__iter__")


def test_get_target_uri_returns_string(temp_sphinx_app):
    """Test that get_target_uri returns a string."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)

    builder.init()

    # get_target_uri should return a string
    uri = builder.get_target_uri("index")
    assert isinstance(uri, str)
    assert uri.endswith(".typ")


def test_prepare_writing_accepts_docnames(temp_sphinx_app):
    """Test that prepare_writing can be called with a set of docnames."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)
    builder.init()

    # prepare_writing should accept a set of document names
    docnames = {"index", "page1", "page2"}
    builder.prepare_writing(docnames)

    # After prepare_writing, writer should be initialized
    assert hasattr(builder, "writer")
    assert builder.writer is not None


def test_write_doc_creates_output_file(temp_sphinx_app, sample_doctree):
    """Test that write_doc creates an output file."""
    from pathlib import Path

    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)
    builder.init()

    docnames = {"index"}
    builder.prepare_writing(docnames)

    # Write a document
    builder.write_doc("index", sample_doctree)

    # Check that output file was created
    output_file = Path(builder.outdir) / "index.typ"
    assert output_file.exists()
    assert output_file.is_file()


def test_write_doc_generates_typst_content(temp_sphinx_app, sample_doctree):
    """Test that write_doc generates Typst content."""
    from pathlib import Path

    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)
    builder.init()

    docnames = {"index"}
    builder.prepare_writing(docnames)

    # Write a document
    builder.write_doc("index", sample_doctree)

    # Check that output file contains Typst content
    output_file = Path(builder.outdir) / "index.typ"
    content = output_file.read_text()

    # Should contain basic Typst markup
    assert len(content) > 0
    # Should contain the title from sample_doctree
    assert "Test Section" in content


def test_finish_completes_build(temp_sphinx_app, sample_doctree):
    """Test that finish completes the build process."""
    from sphinxcontrib.typst.builder import TypstBuilder

    app = temp_sphinx_app
    builder = TypstBuilder(app, app.env)
    builder.init()

    docnames = {"index"}
    builder.prepare_writing(docnames)
    builder.write_doc("index", sample_doctree)

    # finish should complete without errors
    builder.finish()

    # After finish, build should be complete
    # (no specific assertion needed, just checking it doesn't raise)
