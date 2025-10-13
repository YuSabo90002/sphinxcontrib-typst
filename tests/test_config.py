"""
Tests for configuration handling.
"""


def test_default_typst_documents_config(temp_sphinx_app):
    """Test that default typst_documents configuration is set."""
    app = temp_sphinx_app

    # Check that typst_documents config exists
    assert hasattr(app.config, "typst_documents")


def test_typst_documents_config_structure(temp_sphinx_app):
    """Test that typst_documents has the correct structure."""
    app = temp_sphinx_app

    # typst_documents should be a list
    assert isinstance(app.config.typst_documents, list)


def test_custom_typst_documents_config(tmp_path):
    """Test that custom typst_documents configuration is loaded."""
    from sphinx.testing.util import SphinxTestApp

    srcdir = tmp_path / "source"
    srcdir.mkdir()

    # Create conf.py with custom typst_documents
    conf_py = srcdir / "conf.py"
    conf_py.write_text(
        "extensions = ['sphinxcontrib.typst']\n"
        "project = 'Test Project'\n"
        "author = 'Test Author'\n"
        "typst_documents = [\n"
        "    ('index', 'output.typ', 'Test Document', 'Test Author'),\n"
        "]\n"
    )

    # Create minimal index.rst
    index_rst = srcdir / "index.rst"
    index_rst.write_text(
        "Test Document\n" "=============\n" "\n" "This is a test document.\n"
    )

    builddir = tmp_path / "build"

    app = SphinxTestApp(
        srcdir=srcdir,
        builddir=builddir,
    )

    # Check that custom typst_documents is loaded
    assert len(app.config.typst_documents) == 1
    assert app.config.typst_documents[0][0] == "index"
    assert app.config.typst_documents[0][1] == "output.typ"
    assert app.config.typst_documents[0][2] == "Test Document"
    assert app.config.typst_documents[0][3] == "Test Author"


def test_typst_template_config(temp_sphinx_app):
    """Test that typst_template configuration exists."""
    app = temp_sphinx_app

    # Check that typst_template config exists
    assert hasattr(app.config, "typst_template")


def test_typst_use_mitex_config(temp_sphinx_app):
    """Test that typst_use_mitex configuration exists."""
    app = temp_sphinx_app

    # Check that typst_use_mitex config exists
    assert hasattr(app.config, "typst_use_mitex")
    # Default should be True
    assert app.config.typst_use_mitex is True


def test_custom_typst_use_mitex_config(tmp_path):
    """Test that custom typst_use_mitex configuration is loaded."""
    from sphinx.testing.util import SphinxTestApp

    srcdir = tmp_path / "source"
    srcdir.mkdir()

    # Create conf.py with custom typst_use_mitex
    conf_py = srcdir / "conf.py"
    conf_py.write_text(
        "extensions = ['sphinxcontrib.typst']\n"
        "project = 'Test Project'\n"
        "author = 'Test Author'\n"
        "typst_use_mitex = False\n"
    )

    # Create minimal index.rst
    index_rst = srcdir / "index.rst"
    index_rst.write_text(
        "Test Document\n" "=============\n" "\n" "This is a test document.\n"
    )

    builddir = tmp_path / "build"

    app = SphinxTestApp(
        srcdir=srcdir,
        builddir=builddir,
    )

    # Check that custom typst_use_mitex is loaded
    assert app.config.typst_use_mitex is False


def test_typst_elements_config(temp_sphinx_app):
    """Test that typst_elements configuration exists."""
    app = temp_sphinx_app

    # Check that typst_elements config exists
    assert hasattr(app.config, "typst_elements")
    # Default should be an empty dict
    assert isinstance(app.config.typst_elements, dict)


def test_custom_typst_elements_config(tmp_path):
    """Test that custom typst_elements configuration is loaded."""
    from sphinx.testing.util import SphinxTestApp

    srcdir = tmp_path / "source"
    srcdir.mkdir()

    # Create conf.py with custom typst_elements
    conf_py = srcdir / "conf.py"
    conf_py.write_text(
        "extensions = ['sphinxcontrib.typst']\n"
        "project = 'Test Project'\n"
        "author = 'Test Author'\n"
        "typst_elements = {\n"
        "    'papersize': 'a4',\n"
        "    'fontsize': '11pt',\n"
        "}\n"
    )

    # Create minimal index.rst
    index_rst = srcdir / "index.rst"
    index_rst.write_text(
        "Test Document\n" "=============\n" "\n" "This is a test document.\n"
    )

    builddir = tmp_path / "build"

    app = SphinxTestApp(
        srcdir=srcdir,
        builddir=builddir,
    )

    # Check that custom typst_elements is loaded
    assert app.config.typst_elements["papersize"] == "a4"
    assert app.config.typst_elements["fontsize"] == "11pt"
