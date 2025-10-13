"""
Tests for LaTeX math conversion using mitex.

Task 6.2: LaTeX math conversion (mitex)
Design 3.3: mitex for LaTeX math support
Requirements 4.2, 4.3, 4.4, 4.5: math/math_block node conversion
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


def test_inline_math_conversion(simple_document, mock_builder):
    """
    Test that inline math nodes are converted to #mi() format.

    Requirement 4.3: Inline math should use #mi(`...`) format
    Design 3.3: mitex for LaTeX math compatibility
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an inline math node with LaTeX content
    math_node = nodes.math(text=r"\frac{a}{b}")
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should generate #mi(`\frac{a}{b}`)
    assert "#mi(" in output, "Should use #mi() for inline math"
    assert r"\frac{a}{b}" in output, "Should preserve LaTeX content"
    assert "`" in output, "Should use backticks for raw string"


def test_block_math_conversion(simple_document, mock_builder):
    """
    Test that math_block nodes are converted to #mitex() format.

    Requirement 4.2: Block math should use #mitex(`...`) or #mimath(`...`)
    Design 3.3: mitex for LaTeX math compatibility
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a block math node with LaTeX content
    math_block = nodes.math_block(text=r"\sum_{i=1}^{n} x_i")
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate #mitex(`\sum_{i=1}^{n} x_i`)
    assert "#mitex(" in output, "Should use #mitex() for block math"
    assert r"\sum_{i=1}^{n} x_i" in output, "Should preserve LaTeX content"
    assert "`" in output, "Should use backticks for raw string"


def test_math_with_complex_latex(simple_document, mock_builder):
    """
    Test math conversion with complex LaTeX commands.

    Requirement 4.4: LaTeX commands should be preserved
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Complex LaTeX with multiple commands
    complex_latex = r"\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
    math_block = nodes.math_block(text=complex_latex)
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should preserve all LaTeX commands
    assert r"\int" in output, "Should preserve \\int command"
    assert r"\infty" in output, "Should preserve \\infty command"
    assert r"\frac" in output, "Should preserve \\frac command"
    assert r"\sqrt{\pi}" in output, "Should preserve nested commands"


def test_math_with_greek_letters(simple_document, mock_builder):
    """
    Test math conversion with Greek letters.

    Requirement 4.4: Greek letters in LaTeX should be preserved
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    greek_latex = r"\alpha + \beta = \gamma"
    math_node = nodes.math(text=greek_latex)
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    assert r"\alpha" in output, "Should preserve \\alpha"
    assert r"\beta" in output, "Should preserve \\beta"
    assert r"\gamma" in output, "Should preserve \\gamma"


def test_multiple_math_nodes(simple_document, mock_builder):
    """
    Test handling multiple math nodes in a document.
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # First inline math
    math1 = nodes.math(text="x^2")
    try:
        translator.visit_math(math1)
    except nodes.SkipNode:
        pass
    translator.depart_math(math1)

    # Some text
    translator.visit_Text(nodes.Text(" and "))
    translator.depart_Text(nodes.Text(" and "))

    # Second inline math
    math2 = nodes.math(text="y^2")
    try:
        translator.visit_math(math2)
    except nodes.SkipNode:
        pass
    translator.depart_math(math2)

    output = translator.astext()
    # Should have two separate #mi() calls
    assert output.count("#mi(") == 2, "Should have two inline math conversions"
    assert "x^2" in output and "y^2" in output, "Should preserve both math contents"


def test_math_block_with_label(simple_document, mock_builder):
    """
    Test that math_block with label generates Typst <label> syntax.

    Task 6.3: Labeled equations
    Requirement 4.7: Labeled equations should generate <eq:label> format
    Design 3.3: Labels should be appended after #mitex()
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a block math node with label
    math_block = nodes.math_block(text=r"E = mc^2")
    math_block["ids"] = ["einstein-energy"]
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate #mitex(`E = mc^2`) <einstein-energy>
    assert "#mitex(" in output, "Should use #mitex() for block math"
    assert r"E = mc^2" in output, "Should preserve LaTeX content"
    assert "<einstein-energy>" in output, "Should add Typst label format"


def test_math_block_with_number(simple_document, mock_builder):
    """
    Test that numbered math blocks generate appropriate Typst format.

    Task 6.3: Numbered equations
    Requirement 4.8: Numbered equations support
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a numbered math block
    math_block = nodes.math_block(text=r"\int_0^1 x^2 dx", number=1)
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should generate #mitex(`\int_0^1 x^2 dx`)
    assert "#mitex(" in output, "Should use #mitex() for numbered math"
    assert r"\int_0^1 x^2 dx" in output, "Should preserve LaTeX content"


def test_math_with_aligned_environment(simple_document, mock_builder):
    """
    Test that LaTeX environments like aligned are passed through to mitex.

    Task 6.3: Math environments
    Requirement 4.6: LaTeX environments should be preserved
    Design 3.3: mitex handles LaTeX environments natively
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create math block with aligned environment
    aligned_latex = r"\begin{aligned} x &= y + z \\ a &= b + c \end{aligned}"
    math_block = nodes.math_block(text=aligned_latex)
    try:
        translator.visit_math_block(math_block)
    except nodes.SkipNode:
        pass
    translator.depart_math_block(math_block)

    output = translator.astext()
    # Should preserve the entire LaTeX environment
    assert r"\begin{aligned}" in output, "Should preserve \\begin{aligned}"
    assert r"\end{aligned}" in output, "Should preserve \\end{aligned}"
    assert r"&=" in output, "Should preserve alignment markers"


def test_inline_math_with_label(simple_document, mock_builder):
    """
    Test that inline math with label generates Typst <label> syntax.

    Task 6.3: Labeled inline math (edge case)
    Note: This is an edge case - inline math rarely has labels
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an inline math node with label
    math_node = nodes.math(text=r"\alpha")
    math_node["ids"] = ["alpha-symbol"]
    try:
        translator.visit_math(math_node)
    except nodes.SkipNode:
        pass
    translator.depart_math(math_node)

    output = translator.astext()
    # Should generate #mi(`\alpha`) <alpha-symbol>
    assert "#mi(" in output, "Should use #mi() for inline math"
    assert r"\alpha" in output, "Should preserve LaTeX content"
    assert "<alpha-symbol>" in output, "Should add Typst label format"
