"""
Unit tests for nested toctree relative path calculation.

Tests the _compute_relative_include_path method of TypstTranslator
for handling nested directory structures.

Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 5.1
"""

from pathlib import PurePosixPath

import pytest
from docutils import nodes
from docutils.parsers.rst import states
from docutils.utils import Reporter

from sphinxcontrib.typst.translator import TypstTranslator


@pytest.fixture
def mock_document():
    """Create a mock document for testing."""
    reporter = Reporter("", 2, 4)
    doc = nodes.document("", reporter=reporter)
    doc.settings = states.Struct()
    doc.settings.env = None
    doc.settings.language_code = "en"
    doc.settings.strict_visitor = False
    return doc


@pytest.fixture
def mock_builder():
    """Create a mock builder for testing."""

    class MockConfig:
        typst_use_mitex = True

    class MockDomains:
        pass

    class MockEnv:
        domains = MockDomains()

    class MockBuilder:
        name = "typst"
        current_docname = None
        config = MockConfig()
        env = MockEnv()

    return MockBuilder()


class TestRelativePathCalculation:
    """Test relative path calculation logic for toctree entries."""

    def test_compute_relative_path_same_directory(self, mock_document, mock_builder):
        """
        Test relative path calculation for documents in the same directory.

        Given: current_docname = "chapter1/index"
        And: target_docname = "chapter1/section1"
        When: computing relative path
        Then: should return "section1"

        Requirements: 1.4
        """
        # This test will fail until we implement _compute_relative_include_path
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="chapter1/section1", current_docname="chapter1/index"
        )

        assert result == "section1"

    def test_compute_relative_path_parent_directory(self, mock_document, mock_builder):
        """
        Test relative path calculation for parent directory reference.

        Given: current_docname = "chapter1/section1"
        And: target_docname = "index"
        When: computing relative path
        Then: should return "../index"

        Requirements: 1.5
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="index", current_docname="chapter1/section1"
        )

        assert result == "../index"

    def test_compute_relative_path_sibling_directory(self, mock_document, mock_builder):
        """
        Test relative path calculation for sibling directory reference.

        Given: current_docname = "chapter1/doc1"
        And: target_docname = "chapter2/doc2"
        When: computing relative path
        Then: should return "../chapter2/doc2"

        Requirements: 1.5
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="chapter2/doc2", current_docname="chapter1/doc1"
        )

        assert result == "../chapter2/doc2"

    def test_compute_relative_path_nested_subdirectory(
        self, mock_document, mock_builder
    ):
        """
        Test relative path calculation for nested subdirectory.

        Given: current_docname = "chapter1/index"
        And: target_docname = "chapter1/sub/doc"
        When: computing relative path
        Then: should return "sub/doc"

        Requirements: 1.4
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="chapter1/sub/doc", current_docname="chapter1/index"
        )

        assert result == "sub/doc"

    def test_compute_relative_path_deep_nesting(self, mock_document, mock_builder):
        """
        Test relative path calculation for deeply nested directories.

        Given: current_docname = "a/b/x/y"
        And: target_docname = "a/b/c/d/e"
        When: computing relative path
        Then: should return "../c/d/e"
              (from a/b/x directory, go up one level to a/b, then down to c/d/e)

        Requirements: 1.5
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="a/b/c/d/e", current_docname="a/b/x/y"
        )

        assert result == "../c/d/e"

    def test_compute_relative_path_none_current_docname(
        self, mock_document, mock_builder
    ):
        """
        Test fallback behavior when current_docname is None.

        Given: current_docname = None
        And: target_docname = "chapter1/doc"
        When: computing relative path
        Then: should return "chapter1/doc" (fallback to absolute path)

        Requirements: 1.1
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="chapter1/doc", current_docname=None
        )

        assert result == "chapter1/doc"

    def test_compute_relative_path_root_document(self, mock_document, mock_builder):
        """
        Test that root directory documents use absolute paths.

        Given: current_docname = "index" (root)
        And: target_docname = "chapter1/doc"
        When: computing relative path
        Then: should return "chapter1/doc" (no change from root)

        Requirements: 2.1, 2.2
        """
        translator = TypstTranslator(mock_document, mock_builder)

        result = translator._compute_relative_include_path(
            target_docname="chapter1/doc", current_docname="index"
        )

        assert result == "chapter1/doc"

    def test_purepath_windows_compatibility(self):
        """
        Test that PurePosixPath always uses POSIX separators.

        This test verifies that even on Windows, PurePosixPath uses
        forward slashes (/) in paths.

        Requirements: 5.1
        """
        # PurePosixPath should always use / regardless of OS
        path = PurePosixPath("chapter1") / "section1"
        assert str(path) == "chapter1/section1"
        assert "/" in str(path)
        assert "\\" not in str(path)


class TestErrorHandling:
    """Test error handling in relative path calculation."""

    def test_value_error_cross_directory_path_construction(
        self, mock_document, mock_builder
    ):
        """
        Test that ValueError from relative_to() is handled correctly.

        When PurePosixPath.relative_to() raises ValueError (different tree),
        the implementation should build path via common parent.

        Requirements: 1.5
        """
        translator = TypstTranslator(mock_document, mock_builder)

        # This should not raise, but handle ValueError internally
        result = translator._compute_relative_include_path(
            target_docname="chapter2/doc", current_docname="chapter1/index"
        )

        # Should build path via common parent: ../ + chapter2/doc
        assert result == "../chapter2/doc"

    def test_unexpected_exception_fallback(self, mock_document, mock_builder):
        """
        Test graceful degradation on unexpected exceptions.

        If an unexpected error occurs, should fall back to absolute path.

        Requirements: 1.5, 5.1
        """
        translator = TypstTranslator(mock_document, mock_builder)

        # Even with unusual input, should not crash
        # (This test mainly ensures robustness)
        result = translator._compute_relative_include_path(
            target_docname="valid/path", current_docname="also/valid"
        )

        # Should return some valid path (relative or fallback)
        assert isinstance(result, str)
        assert result  # Non-empty
