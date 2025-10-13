"""
Tests for Requirement 13: 複数ドキュメントの統合と toctree 処理

This module tests the toctree → #include() conversion functionality
as specified in Requirement 13 of the design document.
"""

import pytest
from docutils import nodes
from docutils.parsers.rst import states
from docutils.utils import Reporter
from sphinx import addnodes


@pytest.fixture
def simple_document():
    """Create a simple document for testing."""
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
        pass

    class MockDomains:
        pass

    class MockEnv:
        domains = MockDomains()

    class MockBuilder:
        config = MockConfig()
        env = MockEnv()

    return MockBuilder()


def test_toctree_generates_include_directives(simple_document, mock_builder):
    """
    Test that toctree generates #include() directives instead of #outline().

    Requirement 13.2: WHEN `addnodes.toctree` ノードが TypstTranslator で処理される
    THEN 参照された各ドキュメントに対して `#include("relative/path/to/doc.typ")`
    SHALL 生成される
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a toctree node with entries
    toctree = addnodes.toctree()
    toctree["entries"] = [
        ("Introduction", "intro"),
        ("Getting Started", "getting_started"),
        ("API Reference", "api"),
    ]

    # Visit the toctree node
    try:
        translator.visit_toctree(toctree)
    except nodes.SkipNode:
        pass  # Expected behavior

    output = translator.astext()

    # Should generate #include() directives, NOT #outline()
    assert "#include(" in output
    assert '#include("intro.typ")' in output
    assert '#include("getting_started.typ")' in output
    assert '#include("api.typ")' in output
    assert "#outline()" not in output


def test_toctree_with_heading_offset(simple_document, mock_builder):
    """
    Test that toctree generates #include() with heading offset.

    Requirement 13.14: WHEN `#include()` を生成する際に見出しレベルを調整
    THEN Typst SHALL `#[ #set heading(offset: 1); #include("doc.typ") ]` のように
    コンテンツブロック内で `#set heading(offset: 1)` を適用する
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    toctree = addnodes.toctree()
    toctree["entries"] = [
        ("Chapter 1", "chapter1"),
    ]

    try:
        translator.visit_toctree(toctree)
    except nodes.SkipNode:
        pass

    output = translator.astext()

    # Should generate heading offset content block with #[...]
    assert "#set heading(offset: 1)" in output
    assert "#[\n" in output or "#[" in output
    assert "]\n" in output or "]" in output


def test_toctree_with_nested_path(simple_document, mock_builder):
    """
    Test that toctree handles nested document paths correctly.

    Requirement 13.5: WHEN `toctree` で参照されたドキュメントパスが
    "chapter1/section" の場合 THEN Typst SHALL
    `#include("chapter1/section.typ")` を生成する
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    toctree = addnodes.toctree()
    toctree["entries"] = [
        ("Chapter 1 Section", "chapter1/section"),
        ("Chapter 2 Subsection", "chapter2/sub/content"),
    ]

    try:
        translator.visit_toctree(toctree)
    except nodes.SkipNode:
        pass

    output = translator.astext()

    # Should generate nested paths with .typ extension
    assert '#include("chapter1/section.typ")' in output
    assert '#include("chapter2/sub/content.typ")' in output


def test_toctree_empty_entries(simple_document, mock_builder):
    """
    Test that toctree with no entries generates no output.
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    toctree = addnodes.toctree()
    toctree["entries"] = []

    try:
        translator.visit_toctree(toctree)
    except nodes.SkipNode:
        pass

    output = translator.astext()

    # Should generate nothing for empty toctree
    assert output == "" or output.strip() == ""


def test_toctree_skip_node_raised(simple_document, mock_builder):
    """
    Test that visit_toctree raises SkipNode.

    Requirement 13.11: WHEN `toctree` ノード処理時に
    `addnodes.toctree` ノードが `raise nodes.SkipNode` を実行
    THEN 子ノードの処理 SHALL スキップされる
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    toctree = addnodes.toctree()
    toctree["entries"] = [("Test", "test")]

    # Should raise SkipNode
    with pytest.raises(nodes.SkipNode):
        translator.visit_toctree(toctree)
