"""
Tests for Sphinx extension entry point.
"""


def test_setup_function_exists():
    """Test that setup() function is defined in the extension."""
    from sphinxcontrib.typst import setup

    assert callable(setup)


def test_setup_returns_metadata():
    """Test that setup() returns correct extension metadata."""
    from sphinxcontrib.typst import setup

    # Create a mock Sphinx app with add_builder method
    class MockApp:
        def add_builder(self, builder):
            pass

        def add_config_value(self, name, default, rebuild, types):
            pass

    app = MockApp()
    metadata = setup(app)

    # Verify metadata structure
    assert isinstance(metadata, dict)
    assert "version" in metadata
    assert "parallel_read_safe" in metadata
    assert "parallel_write_safe" in metadata


def test_setup_parallel_safety():
    """Test that extension declares parallel processing safety."""
    from sphinxcontrib.typst import setup

    class MockApp:
        def add_builder(self, builder):
            pass

        def add_config_value(self, name, default, rebuild, types):
            pass

    app = MockApp()
    metadata = setup(app)

    # Extension should be safe for parallel processing
    assert metadata["parallel_read_safe"] is True
    assert metadata["parallel_write_safe"] is True


def test_setup_version_matches():
    """Test that setup() returns correct version matching package version."""
    from sphinxcontrib.typst import __version__, setup

    class MockApp:
        def add_builder(self, builder):
            pass

        def add_config_value(self, name, default, rebuild, types):
            pass

    app = MockApp()
    metadata = setup(app)

    assert metadata["version"] == __version__
    assert metadata["version"] == "0.1.0b1"


def test_extension_can_be_loaded(temp_sphinx_app):
    """Test that extension can be loaded by Sphinx."""
    # This test uses our custom temp_sphinx_app fixture
    app = temp_sphinx_app
    assert app is not None
    assert "sphinxcontrib.typst" in app.extensions
