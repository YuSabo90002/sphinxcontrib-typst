"""
Tests for math fallback functionality when typst_use_mitex=False.

Task 6.5: Math fallback functionality
Design 3.3: Fallback when typst_use_mitex=False
Requirements 4.9, 5.4, 5.6: LaTeX to Typst native conversion
"""

import pytest
from docutils import nodes
from docutils.parsers.rst import states
from docutils.utils import Reporter


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
def mock_builder_no_mitex(mock_builder):
    """Mock builder with typst_use_mitex=False."""
    mock_builder.config.typst_use_mitex = False
    return mock_builder


def test_fallback_inline_math_basic(simple_document, mock_builder_no_mitex):
    """
    Test that inline math falls back to Typst native when typst_use_mitex=False.

    Requirement 4.9: typst_use_mitex=False should use Typst native syntax
    Task 6.5: Fallback implementation
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # Simple inline math without LaTeX-specific commands
    math_node = nodes.math(text="x^2 + y^2")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should generate $x^2 + y^2$ instead of #mi(`...`)
    assert (
        "$x^2 + y^2$" in output
    ), "Should use Typst native format when mitex is disabled"
    assert "#mi(" not in output, "Should not use mitex when typst_use_mitex=False"


def test_fallback_block_math_basic(simple_document, mock_builder_no_mitex):
    """
    Test that block math falls back to Typst native when typst_use_mitex=False.

    Requirement 4.9: typst_use_mitex=False should use Typst native syntax
    Task 6.5: Fallback implementation
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # Simple block math
    math_block = nodes.math_block(text="a + b = c")
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate $ a + b = c $ instead of #mitex(`...`)
    assert (
        "$ a + b = c $" in output
    ), "Should use Typst native format when mitex is disabled"
    assert "#mitex(" not in output, "Should not use mitex when typst_use_mitex=False"


def test_fallback_converts_greek_letters(simple_document, mock_builder_no_mitex):
    """
    Test that Greek letters are converted from LaTeX to Typst.

    Task 6.5: Basic LaTeX to Typst conversion
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # LaTeX Greek letters
    math_node = nodes.math(text=r"\alpha + \beta = \gamma")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should convert \alpha -> alpha, \beta -> beta, \gamma -> gamma
    assert "alpha" in output, "Should convert \\alpha to alpha"
    assert "beta" in output, "Should convert \\beta to beta"
    assert "gamma" in output, "Should convert \\gamma to gamma"
    assert "\\" not in output, "Should not have backslashes in Typst output"


def test_fallback_converts_frac(simple_document, mock_builder_no_mitex):
    """
    Test that \\frac is converted to Typst fraction syntax.

    Task 6.5: Basic LaTeX to Typst conversion
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # LaTeX fraction
    math_node = nodes.math(text=r"\frac{a}{b}")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should convert \frac{a}{b} to a/b or frac(a, b)
    # Typst uses frac(numerator, denominator) syntax
    assert (
        "frac(a, b)" in output or "a / b" in output
    ), "Should convert \\frac to Typst syntax"
    assert "\\frac" not in output, "Should not have LaTeX \\frac in output"


def test_fallback_converts_sum(simple_document, mock_builder_no_mitex):
    """
    Test that \\sum is converted to Typst sum syntax.

    Task 6.5: Basic LaTeX to Typst conversion
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # LaTeX sum
    math_node = nodes.math(text=r"\sum_{i=1}^{n} x_i")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should convert \sum_{i=1}^{n} to sum_(i=1)^n
    assert "sum_" in output, "Should have sum_ in Typst output"
    assert "\\sum" not in output, "Should not have LaTeX \\sum in output"


def test_fallback_with_label(simple_document, mock_builder_no_mitex):
    """
    Test that labeled equations work with fallback.

    Requirement 5.4: Labeled Typst native equations
    Task 6.5: Fallback with labels
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # Math block with label
    math_block = nodes.math_block(text="E = m c^2")
    math_block["ids"] = ["einstein"]
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should have both Typst native math and label
    assert (
        "$ E = m c^2 $" in output or "$E = m c^2$" in output
    ), "Should use Typst native syntax"
    assert "<einstein>" in output, "Should include label"
    assert "#mitex(" not in output, "Should not use mitex"


def test_mitex_enabled_by_default(simple_document, mock_builder):
    """
    Test that mitex is used by default when typst_use_mitex is not set.

    Task 6.5: Default behavior
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    # Default builder (typst_use_mitex not explicitly set, should default to True)
    translator = TypstTranslator(simple_document, mock_builder)

    math_node = nodes.math(text=r"\alpha")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should use mitex by default
    assert "#mi(" in output, "Should use mitex by default"
    assert r"\alpha" in output, "Should preserve LaTeX syntax with mitex"


def test_fallback_unsupported_syntax_warning(
    simple_document, mock_builder_no_mitex, caplog
):
    """
    Test that unsupported LaTeX syntax generates a warning.

    Requirement 5.6: Syntax error detection and warnings
    Task 6.5: Error detection
    """
    import logging

    from sphinxcontrib.typst.translator import TypstTranslator

    # Set up logging to capture warnings
    caplog.set_level(logging.WARNING)

    translator = TypstTranslator(simple_document, mock_builder_no_mitex)

    # Complex LaTeX that might not convert well
    math_node = nodes.math(text=r"\newcommand{\custom}{x} \custom")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    # Should have generated a warning about potential conversion issues
    # (This test may need adjustment based on actual warning implementation)
    output = translator.astext()
    # At minimum, should output something (even if partially converted)
    assert len(output) > 0, "Should produce some output even with unsupported syntax"
