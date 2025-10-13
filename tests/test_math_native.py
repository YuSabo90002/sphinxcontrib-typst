"""
Tests for Typst native math support.

Task 6.4: Typst native math support
Design 3.3: Support both mitex and Typst native math
Requirements 5.1, 5.2, 5.3, 5.5: Typst native math syntax
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


def test_inline_typst_native_math(simple_document, mock_builder):
    """
    Test that inline math with typst-native class uses $ ... $ syntax.

    Requirement 5.2: Inline math should use $...$ format
    Task 6.4: Typst native math識別
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create inline math node with typst-native class
    math_node = nodes.math(text="x^2 + y^2")
    math_node["classes"] = ["typst-native"]
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should generate $x^2 + y^2$ instead of #mi(`...`)
    assert "$x^2 + y^2$" in output, "Should use Typst native inline math syntax"
    assert "#mi(" not in output, "Should not use mitex for typst-native math"


def test_block_typst_native_math(simple_document, mock_builder):
    """
    Test that block math with typst-native class uses $ ... $ syntax.

    Requirement 5.2: Block math should use $ ... $ format
    Task 6.4: Typst native math識別
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create block math node with typst-native class
    math_block = nodes.math_block(text="sum_(i=1)^n x_i")
    math_block["classes"] = ["typst-native"]
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate $ sum_(i=1)^n x_i $ instead of #mitex(`...`)
    assert "$ sum_(i=1)^n x_i $" in output, "Should use Typst native block math syntax"
    assert "#mitex(" not in output, "Should not use mitex for typst-native math"


def test_typst_native_math_with_label(simple_document, mock_builder):
    """
    Test that Typst native math with label generates $ ... $ <label> format.

    Requirement 5.4: Typst native math with labels
    Task 6.4: Label support for native math
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create block math node with typst-native class and label
    math_block = nodes.math_block(text="E = m c^2")
    math_block["classes"] = ["typst-native"]
    math_block["ids"] = ["energy-equation"]
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate $ E = m c^2 $ <energy-equation>
    assert "$ E = m c^2 $" in output, "Should use Typst native block math"
    assert "<energy-equation>" in output, "Should include label"


def test_typst_native_special_functions(simple_document, mock_builder):
    """
    Test that Typst-specific math functions are preserved.

    Requirement 5.3: Typst特有の数式機能の保持
    Task 6.4: Typst native math features
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Typst native functions like cal, bb, attach
    math_block = nodes.math_block(text="cal(A) subset.eq bb(R)^n")
    math_block["classes"] = ["typst-native"]
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should preserve Typst-specific syntax
    assert "cal(A)" in output, "Should preserve cal() function"
    assert "bb(R)" in output, "Should preserve bb() function"
    assert "subset.eq" in output, "Should preserve Typst symbols"


def test_mixed_latex_and_typst_native_math(simple_document, mock_builder):
    """
    Test that LaTeX and Typst native math can coexist.

    Requirement 5.5: LaTeX数式とTypstネイティブ数式の混在対応
    Task 6.4: Mixed math support
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # LaTeX math (default, no typst-native class)
    latex_math = nodes.math(text=r"\alpha + \beta")
    try:
        translator.visit_math(latex_math)
    except nodes.SkipNode:
        pass
    translator.depart_math(latex_math)

    # Add some text
    translator.add_text(" and ")

    # Typst native math
    typst_math = nodes.math(text="alpha + beta")
    typst_math["classes"] = ["typst-native"]
    try:
        translator.visit_math(typst_math)
    except nodes.SkipNode:
        pass
    translator.depart_math(typst_math)

    output = translator.astext()
    # Should have both formats
    assert "#mi(" in output, "Should use mitex for LaTeX math"
    assert r"\alpha + \beta" in output, "Should preserve LaTeX syntax"
    assert "$alpha + beta$" in output, "Should use Typst native for marked math"


def test_latex_math_without_typst_native_class(simple_document, mock_builder):
    """
    Test that math without typst-native class still uses mitex (backward compatibility).

    Task 6.4: Default behavior preservation
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Math node without typst-native class (default LaTeX)
    math_node = nodes.math(text=r"\frac{a}{b}")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should still use mitex by default
    assert "#mi(" in output, "Should use mitex for default math"
    assert r"\frac{a}{b}" in output, "Should preserve LaTeX content"
    assert "$" not in output.replace(
        "`", ""
    ), "Should not use Typst native syntax by default"
