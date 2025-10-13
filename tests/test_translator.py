"""
Tests for TypstTranslator class.
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


def test_translator_state_initialization(simple_document, mock_builder):
    """Test that translator initializes state variables correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Check that state variables are initialized
    assert hasattr(translator, "section_level")
    assert translator.section_level == 0
    assert hasattr(translator, "in_figure")
    assert translator.in_figure is False
    assert hasattr(translator, "in_table")
    assert translator.in_table is False
    assert hasattr(translator, "list_stack")
    assert translator.list_stack == []


def test_translator_section_level_management(simple_document, mock_builder):
    """Test that section_level is managed correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Initial section level should be 0
    assert translator.section_level == 0

    # Visit a section - should increment
    section = nodes.section()
    translator.visit_section(section)
    assert translator.section_level == 1

    # Visit a nested section - should increment again
    nested_section = nodes.section()
    translator.visit_section(nested_section)
    assert translator.section_level == 2

    # Depart nested section - should decrement
    translator.depart_section(nested_section)
    assert translator.section_level == 1

    # Depart section - should decrement
    translator.depart_section(section)
    assert translator.section_level == 0


def test_translator_heading_level_generation(simple_document, mock_builder):
    """Test that heading levels are generated correctly based on section_level."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Level 1 heading (=)
    section1 = nodes.section()
    translator.visit_section(section1)
    title1 = nodes.title(text="Level 1")
    translator.visit_title(title1)
    translator.visit_Text(nodes.Text("Level 1"))
    translator.depart_Text(nodes.Text("Level 1"))
    translator.depart_title(title1)
    output1 = translator.astext()
    assert "= Level 1" in output1

    # Clear output for next test
    translator.body = []

    # Level 2 heading (==)
    section2 = nodes.section()
    translator.visit_section(section2)
    title2 = nodes.title(text="Level 2")
    translator.visit_title(title2)
    translator.visit_Text(nodes.Text("Level 2"))
    translator.depart_Text(nodes.Text("Level 2"))
    translator.depart_title(title2)
    output2 = translator.astext()
    assert "== Level 2" in output2


def test_table_conversion(simple_document, mock_builder):
    """Test that table nodes are converted to Typst #table() syntax."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a simple 2x2 table
    # Table structure: table > tgroup > (colspec, thead, tbody) > row > entry
    table = nodes.table()
    tgroup = nodes.tgroup(cols=2)

    # Add column specifications
    colspec1 = nodes.colspec(colwidth=1)
    colspec2 = nodes.colspec(colwidth=1)
    tgroup += colspec1
    tgroup += colspec2

    # Add header row
    thead = nodes.thead()
    row1 = nodes.row()
    entry1 = nodes.entry()
    entry1 += nodes.paragraph(text="Header 1")
    entry2 = nodes.entry()
    entry2 += nodes.paragraph(text="Header 2")
    row1 += entry1
    row1 += entry2
    thead += row1
    tgroup += thead

    # Add body row
    tbody = nodes.tbody()
    row2 = nodes.row()
    entry3 = nodes.entry()
    entry3 += nodes.paragraph(text="Cell 1")
    entry4 = nodes.entry()
    entry4 += nodes.paragraph(text="Cell 2")
    row2 += entry3
    row2 += entry4
    tbody += row2
    tgroup += tbody

    table += tgroup

    # Visit the table using walkabout (proper doctree traversal)
    table.walkabout(translator)

    output = translator.astext()

    # Debug: print output if test fails
    if "#table(" not in output:
        print(f"DEBUG: Output is: '{output}'")
        print(
            f"DEBUG: Table cells: {translator.table_cells if hasattr(translator, 'table_cells') else 'N/A'}"
        )

    # Check that Typst #table() syntax is generated
    assert "#table(" in output
    assert "columns: 2" in output or "columns: (1fr, 1fr)" in output
    assert "Header 1" in output
    assert "Header 2" in output
    assert "Cell 1" in output
    assert "Cell 2" in output


def test_unknown_visit_handles_unknown_nodes(simple_document, mock_builder):
    """Test that unknown_visit is called for unknown nodes."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a custom unknown node type
    class UnknownNode(nodes.Element):
        pass

    unknown_node = UnknownNode()

    # Should not raise an exception
    translator.unknown_visit(unknown_node)
    translator.unknown_departure(unknown_node)

    # Check that we can still generate output
    output = translator.astext()
    assert isinstance(output, str)


def test_in_figure_state_management(simple_document, mock_builder):
    """Test that in_figure state is managed correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Initially not in figure
    assert translator.in_figure is False

    # Visit a figure
    figure = nodes.figure()
    translator.visit_figure(figure)
    assert translator.in_figure is True

    # Depart figure
    translator.depart_figure(figure)
    assert translator.in_figure is False


def test_in_table_state_management(simple_document, mock_builder):
    """Test that in_table state is managed correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Initially not in table
    assert translator.in_table is False

    # Visit a table
    table = nodes.table()
    translator.visit_table(table)
    assert translator.in_table is True

    # Depart table
    translator.depart_table(table)
    assert translator.in_table is False


def test_subtitle_conversion(simple_document, mock_builder):
    """Test that subtitle nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a section
    section = nodes.section()
    translator.visit_section(section)

    # Visit a subtitle
    subtitle = nodes.subtitle(text="Test Subtitle")
    translator.visit_subtitle(subtitle)
    translator.visit_Text(nodes.Text("Test Subtitle"))
    translator.depart_Text(nodes.Text("Test Subtitle"))
    translator.depart_subtitle(subtitle)

    output = translator.astext()
    # Subtitle should be rendered as emphasized text
    assert "_Test Subtitle_" in output


def test_paragraph_and_text_conversion(simple_document, mock_builder):
    """Test that paragraphs and text are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a paragraph
    para = nodes.paragraph(text="This is a test paragraph.")
    translator.visit_paragraph(para)
    translator.visit_Text(nodes.Text("This is a test paragraph."))
    translator.depart_Text(nodes.Text("This is a test paragraph."))
    translator.depart_paragraph(para)

    output = translator.astext()
    assert "This is a test paragraph." in output
    # Paragraph should end with double newline
    assert "\n\n" in output


def test_multiple_paragraphs_conversion(simple_document, mock_builder):
    """Test that multiple paragraphs are separated correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # First paragraph
    para1 = nodes.paragraph(text="First paragraph.")
    translator.visit_paragraph(para1)
    translator.visit_Text(nodes.Text("First paragraph."))
    translator.depart_Text(nodes.Text("First paragraph."))
    translator.depart_paragraph(para1)

    # Second paragraph
    para2 = nodes.paragraph(text="Second paragraph.")
    translator.visit_paragraph(para2)
    translator.visit_Text(nodes.Text("Second paragraph."))
    translator.depart_Text(nodes.Text("Second paragraph."))
    translator.depart_paragraph(para2)

    output = translator.astext()
    assert "First paragraph." in output
    assert "Second paragraph." in output
    # Paragraphs should be separated by double newline
    assert "First paragraph.\n\nSecond paragraph." in output


def test_emphasis_conversion(simple_document, mock_builder):
    """Test that emphasis (italic) nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit an emphasis node
    emphasis = nodes.emphasis(text="italic text")
    translator.visit_emphasis(emphasis)
    translator.visit_Text(nodes.Text("italic text"))
    translator.depart_Text(nodes.Text("italic text"))
    translator.depart_emphasis(emphasis)

    output = translator.astext()
    # Emphasis should be rendered as _text_
    assert "_italic text_" in output


def test_strong_conversion(simple_document, mock_builder):
    """Test that strong (bold) nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a strong node
    strong = nodes.strong(text="bold text")
    translator.visit_strong(strong)
    translator.visit_Text(nodes.Text("bold text"))
    translator.depart_Text(nodes.Text("bold text"))
    translator.depart_strong(strong)

    output = translator.astext()
    # Strong should be rendered as *text*
    assert "*bold text*" in output


def test_literal_conversion(simple_document, mock_builder):
    """Test that literal (inline code) nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a literal node
    literal = nodes.literal(text="code")
    translator.visit_literal(literal)
    translator.visit_Text(nodes.Text("code"))
    translator.depart_Text(nodes.Text("code"))
    translator.depart_literal(literal)

    output = translator.astext()
    # Literal should be rendered as `code`
    assert "`code`" in output


def test_subscript_conversion(simple_document, mock_builder):
    """Test that subscript nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a subscript node
    subscript = nodes.subscript(text="2")
    translator.visit_subscript(subscript)
    translator.visit_Text(nodes.Text("2"))
    translator.depart_Text(nodes.Text("2"))
    translator.depart_subscript(subscript)

    output = translator.astext()
    # Subscript should be rendered as #sub[2]
    assert "#sub[2]" in output


def test_superscript_conversion(simple_document, mock_builder):
    """Test that superscript nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Visit a superscript node
    superscript = nodes.superscript(text="2")
    translator.visit_superscript(superscript)
    translator.visit_Text(nodes.Text("2"))
    translator.depart_Text(nodes.Text("2"))
    translator.depart_superscript(superscript)

    output = translator.astext()
    # Superscript should be rendered as #super[2]
    assert "#super[2]" in output


def test_mixed_inline_elements(simple_document, mock_builder):
    """Test that mixed inline elements work correctly together."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a paragraph with mixed inline elements
    para = nodes.paragraph()
    translator.visit_paragraph(para)

    # Regular text
    translator.visit_Text(nodes.Text("This is "))
    translator.depart_Text(nodes.Text("This is "))

    # Bold text
    strong = nodes.strong(text="bold")
    translator.visit_strong(strong)
    translator.visit_Text(nodes.Text("bold"))
    translator.depart_Text(nodes.Text("bold"))
    translator.depart_strong(strong)

    # Regular text
    translator.visit_Text(nodes.Text(" and "))
    translator.depart_Text(nodes.Text(" and "))

    # Italic text
    emphasis = nodes.emphasis(text="italic")
    translator.visit_emphasis(emphasis)
    translator.visit_Text(nodes.Text("italic"))
    translator.depart_Text(nodes.Text("italic"))
    translator.depart_emphasis(emphasis)

    # Regular text
    translator.visit_Text(nodes.Text(" with "))
    translator.depart_Text(nodes.Text(" with "))

    # Inline code
    literal = nodes.literal(text="code")
    translator.visit_literal(literal)
    translator.visit_Text(nodes.Text("code"))
    translator.depart_Text(nodes.Text("code"))
    translator.depart_literal(literal)

    translator.visit_Text(nodes.Text("."))
    translator.depart_Text(nodes.Text("."))

    translator.depart_paragraph(para)

    output = translator.astext()
    assert "This is *bold* and _italic_ with `code`." in output


def test_bullet_list_conversion(simple_document, mock_builder):
    """Test that bullet lists are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a bullet list
    bullet_list = nodes.bullet_list()
    translator.visit_bullet_list(bullet_list)

    # First item
    item1 = nodes.list_item()
    translator.visit_list_item(item1)
    translator.visit_Text(nodes.Text("First item"))
    translator.depart_Text(nodes.Text("First item"))
    translator.depart_list_item(item1)

    # Second item
    item2 = nodes.list_item()
    translator.visit_list_item(item2)
    translator.visit_Text(nodes.Text("Second item"))
    translator.depart_Text(nodes.Text("Second item"))
    translator.depart_list_item(item2)

    translator.depart_bullet_list(bullet_list)

    output = translator.astext()
    assert "- First item" in output
    assert "- Second item" in output


def test_enumerated_list_conversion(simple_document, mock_builder):
    """Test that enumerated lists are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an enumerated list
    enum_list = nodes.enumerated_list()
    translator.visit_enumerated_list(enum_list)

    # First item
    item1 = nodes.list_item()
    translator.visit_list_item(item1)
    translator.visit_Text(nodes.Text("First item"))
    translator.depart_Text(nodes.Text("First item"))
    translator.depart_list_item(item1)

    # Second item
    item2 = nodes.list_item()
    translator.visit_list_item(item2)
    translator.visit_Text(nodes.Text("Second item"))
    translator.depart_Text(nodes.Text("Second item"))
    translator.depart_list_item(item2)

    translator.depart_enumerated_list(enum_list)

    output = translator.astext()
    assert "+ First item" in output
    assert "+ Second item" in output


def test_nested_bullet_list(simple_document, mock_builder):
    """Test that nested bullet lists are converted correctly with proper indentation."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Outer bullet list
    outer_list = nodes.bullet_list()
    translator.visit_bullet_list(outer_list)

    # First outer item
    outer_item1 = nodes.list_item()
    translator.visit_list_item(outer_item1)
    translator.visit_Text(nodes.Text("Outer item 1"))
    translator.depart_Text(nodes.Text("Outer item 1"))
    translator.depart_list_item(outer_item1)

    # Second outer item with nested list
    outer_item2 = nodes.list_item()
    translator.visit_list_item(outer_item2)
    translator.visit_Text(nodes.Text("Outer item 2"))
    translator.depart_Text(nodes.Text("Outer item 2"))

    # Nested bullet list
    inner_list = nodes.bullet_list()
    translator.visit_bullet_list(inner_list)

    # Inner item
    inner_item1 = nodes.list_item()
    translator.visit_list_item(inner_item1)
    translator.visit_Text(nodes.Text("Inner item 1"))
    translator.depart_Text(nodes.Text("Inner item 1"))
    translator.depart_list_item(inner_item1)

    translator.depart_bullet_list(inner_list)
    translator.depart_list_item(outer_item2)

    translator.depart_bullet_list(outer_list)

    output = translator.astext()
    assert "- Outer item 1" in output
    assert "- Outer item 2" in output
    assert "  - Inner item 1" in output  # Indented


def test_nested_enumerated_list(simple_document, mock_builder):
    """Test that nested enumerated lists are converted correctly with proper indentation."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Outer enumerated list
    outer_list = nodes.enumerated_list()
    translator.visit_enumerated_list(outer_list)

    # First outer item
    outer_item1 = nodes.list_item()
    translator.visit_list_item(outer_item1)
    translator.visit_Text(nodes.Text("Outer item 1"))
    translator.depart_Text(nodes.Text("Outer item 1"))
    translator.depart_list_item(outer_item1)

    # Second outer item with nested list
    outer_item2 = nodes.list_item()
    translator.visit_list_item(outer_item2)
    translator.visit_Text(nodes.Text("Outer item 2"))
    translator.depart_Text(nodes.Text("Outer item 2"))

    # Nested enumerated list
    inner_list = nodes.enumerated_list()
    translator.visit_enumerated_list(inner_list)

    # Inner item
    inner_item1 = nodes.list_item()
    translator.visit_list_item(inner_item1)
    translator.visit_Text(nodes.Text("Inner item 1"))
    translator.depart_Text(nodes.Text("Inner item 1"))
    translator.depart_list_item(inner_item1)

    translator.depart_enumerated_list(inner_list)
    translator.depart_list_item(outer_item2)

    translator.depart_enumerated_list(outer_list)

    output = translator.astext()
    assert "+ Outer item 1" in output
    assert "+ Outer item 2" in output
    assert "  + Inner item 1" in output  # Indented


def test_mixed_nested_lists(simple_document, mock_builder):
    """Test that mixed nested lists (bullet + enumerated) work correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Outer bullet list
    outer_list = nodes.bullet_list()
    translator.visit_bullet_list(outer_list)

    # First item with nested enumerated list
    outer_item1 = nodes.list_item()
    translator.visit_list_item(outer_item1)
    translator.visit_Text(nodes.Text("Bullet item"))
    translator.depart_Text(nodes.Text("Bullet item"))

    # Nested enumerated list
    inner_list = nodes.enumerated_list()
    translator.visit_enumerated_list(inner_list)

    inner_item1 = nodes.list_item()
    translator.visit_list_item(inner_item1)
    translator.visit_Text(nodes.Text("Numbered item"))
    translator.depart_Text(nodes.Text("Numbered item"))
    translator.depart_list_item(inner_item1)

    translator.depart_enumerated_list(inner_list)
    translator.depart_list_item(outer_item1)

    translator.depart_bullet_list(outer_list)

    output = translator.astext()
    assert "- Bullet item" in output
    assert "  + Numbered item" in output  # Indented with different marker


def test_literal_block_without_language(simple_document, mock_builder):
    """Test that literal blocks without language are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block without language
    literal_block = nodes.literal_block(text="def hello():\n    print('Hello')")
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("def hello():\n    print('Hello')"))
    translator.depart_Text(nodes.Text("def hello():\n    print('Hello')"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should generate code block with backticks
    assert "```" in output
    assert "def hello():" in output
    assert "print('Hello')" in output


def test_literal_block_with_language(simple_document, mock_builder):
    """Test that literal blocks with language specification are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with language
    literal_block = nodes.literal_block(text="def hello():\n    print('Hello')")
    literal_block["language"] = "python"
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("def hello():\n    print('Hello')"))
    translator.depart_Text(nodes.Text("def hello():\n    print('Hello')"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should generate code block with language specification
    assert "```python" in output
    assert "def hello():" in output
    assert "print('Hello')" in output


def test_literal_block_escaping(simple_document, mock_builder):
    """Test that literal blocks handle special characters correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with special characters
    literal_block = nodes.literal_block(text="x = `value`\ny = ${var}")
    literal_block["language"] = "bash"
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("x = `value`\ny = ${var}"))
    translator.depart_Text(nodes.Text("x = `value`\ny = ${var}"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Special characters should be preserved in code block
    assert "```bash" in output
    assert "x = `value`" in output
    assert "y = ${var}" in output


def test_literal_block_with_linenos(simple_document, mock_builder):
    """Test that literal blocks with line numbers are handled correctly (Task 4.2)."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with linenos option
    literal_block = nodes.literal_block(text="line 1\nline 2\nline 3")
    literal_block["language"] = "python"
    literal_block["linenos"] = True
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("line 1\nline 2\nline 3"))
    translator.depart_Text(nodes.Text("line 1\nline 2\nline 3"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should generate raw block with numbering parameter
    # Typst #raw() with numbering: "line-1" or similar
    assert "#raw(" in output or "```python" in output
    if "#raw(" in output:
        # Check for numbering parameter
        assert "numbering:" in output or "line-1" in output


def test_literal_block_with_highlight_lines(simple_document, mock_builder):
    """
    Test that literal blocks with highlight_args generate #codly-range() (Task 4.2.2).

    Design 3.5: codly forced usage with #codly-range() for highlighted lines
    Requirement 7.4: highlight_args should be converted to #codly-range(highlight: (...))
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with highlight_args
    literal_block = nodes.literal_block(text="line 1\nline 2\nline 3\nline 4")
    literal_block["language"] = "python"
    literal_block["highlight_args"] = {"hl_lines": [2, 3]}
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("line 1\nline 2\nline 3\nline 4"))
    translator.depart_Text(nodes.Text("line 1\nline 2\nline 3\nline 4"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should generate #codly-range() before code block
    assert (
        "#codly-range(" in output
    ), "Should generate #codly-range() for highlighted lines"
    assert "highlight:" in output, "Should specify highlight parameter"
    assert "2" in output and "3" in output, "Should include highlighted line numbers"
    assert "```python" in output, "Should still use code block with language"


def test_literal_block_with_linenos_and_highlights(simple_document, mock_builder):
    """
    Test literal blocks with both line numbers and highlights (Task 4.2.2).

    Design 3.5: codly provides line numbers by default, use #codly-range() for highlights
    Requirement 7.3, 7.4: Both linenos and highlight_args should be supported
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with both options
    literal_block = nodes.literal_block(text="def foo():\n    x = 1\n    return x")
    literal_block["language"] = "python"
    literal_block["linenos"] = True
    literal_block["highlight_args"] = {"hl_lines": [2]}
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("def foo():\n    x = 1\n    return x"))
    translator.depart_Text(nodes.Text("def foo():\n    x = 1\n    return x"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # codly provides line numbers by default, should generate #codly-range() for highlights
    assert (
        "#codly-range(" in output
    ), "Should generate #codly-range() for highlighted lines"
    assert "highlight:" in output, "Should specify highlight parameter"
    assert "2" in output, "Should include highlighted line number"
    assert "```python" in output, "Should use code block with language"


def test_literal_block_with_highlight_ranges(simple_document, mock_builder):
    """
    Test literal blocks with highlight ranges (Task 4.2.2).

    Design 3.5: #codly-range() should support both individual lines and ranges
    Example: #codly-range(highlight: (2, 4-6)) highlights line 2 and lines 4-6
    """
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with range highlights (simulating ":emphasize-lines: 2,4-6")
    literal_block = nodes.literal_block(
        text="line 1\nline 2\nline 3\nline 4\nline 5\nline 6"
    )
    literal_block["language"] = "python"
    # hl_lines can contain individual lines and ranges
    literal_block["highlight_args"] = {"hl_lines": [2, 4, 5, 6]}
    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("line 1\nline 2\nline 3\nline 4\nline 5\nline 6"))
    translator.depart_Text(nodes.Text("line 1\nline 2\nline 3\nline 4\nline 5\nline 6"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should generate #codly-range() with highlight parameter
    assert "#codly-range(" in output, "Should generate #codly-range()"
    assert "highlight:" in output, "Should specify highlight parameter"
    # Should contain line numbers (exact format depends on implementation)
    assert (
        "2" in output or "4" in output
    ), "Should include some highlighted line numbers"


def test_literal_block_unsupported_language_warning(simple_document, mock_builder):
    """Test handling of unsupported languages (Task 4.2)."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a literal block with potentially unsupported language
    literal_block = nodes.literal_block(text="some code")
    literal_block["language"] = "obscure-language-xyz"

    translator.visit_literal_block(literal_block)
    translator.visit_Text(nodes.Text("some code"))
    translator.depart_Text(nodes.Text("some code"))
    translator.depart_literal_block(literal_block)

    output = translator.astext()
    # Should still generate code block (Typst handles unknown languages gracefully)
    assert "```obscure-language-xyz" in output or "```" in output


def test_definition_list_conversion(simple_document, mock_builder):
    """Test that definition lists are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a definition list
    def_list = nodes.definition_list()
    translator.visit_definition_list(def_list)

    # First definition list item
    def_item1 = nodes.definition_list_item()

    # Term
    term1 = nodes.term(text="API")
    translator.visit_term(term1)
    translator.visit_Text(nodes.Text("API"))
    translator.depart_Text(nodes.Text("API"))
    translator.depart_term(term1)

    # Definition
    definition1 = nodes.definition()
    translator.visit_definition(definition1)
    translator.visit_Text(nodes.Text("Application Programming Interface"))
    translator.depart_Text(nodes.Text("Application Programming Interface"))
    translator.depart_definition(definition1)

    # Second definition list item
    def_item2 = nodes.definition_list_item()

    # Term
    term2 = nodes.term(text="SDK")
    translator.visit_term(term2)
    translator.visit_Text(nodes.Text("SDK"))
    translator.depart_Text(nodes.Text("SDK"))
    translator.depart_term(term2)

    # Definition
    definition2 = nodes.definition()
    translator.visit_definition(definition2)
    translator.visit_Text(nodes.Text("Software Development Kit"))
    translator.depart_Text(nodes.Text("Software Development Kit"))
    translator.depart_definition(definition2)

    translator.depart_definition_list(def_list)

    output = translator.astext()
    # Typst definition list syntax: / term: definition
    assert "/ API: Application Programming Interface" in output
    assert "/ SDK: Software Development Kit" in output


def test_definition_list_with_multiple_definitions(simple_document, mock_builder):
    """Test that definition lists with multiple definitions per term work correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a definition list
    def_list = nodes.definition_list()
    translator.visit_definition_list(def_list)

    # Term
    term = nodes.term(text="Python")
    translator.visit_term(term)
    translator.visit_Text(nodes.Text("Python"))
    translator.depart_Text(nodes.Text("Python"))
    translator.depart_term(term)

    # First definition
    definition1 = nodes.definition()
    translator.visit_definition(definition1)
    translator.visit_Text(nodes.Text("A programming language"))
    translator.depart_Text(nodes.Text("A programming language"))
    translator.depart_definition(definition1)

    translator.depart_definition_list(def_list)

    output = translator.astext()
    assert "/ Python: A programming language" in output


def test_block_quote_conversion(simple_document, mock_builder):
    """Test that block quotes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a block quote
    block_quote = nodes.block_quote()
    translator.visit_block_quote(block_quote)

    # Paragraph inside block quote
    para = nodes.paragraph(text="This is a quoted text.")
    translator.visit_paragraph(para)
    translator.visit_Text(nodes.Text("This is a quoted text."))
    translator.depart_Text(nodes.Text("This is a quoted text."))
    translator.depart_paragraph(para)

    translator.depart_block_quote(block_quote)

    output = translator.astext()
    # Typst block quote syntax: #quote[...]
    assert "#quote[" in output
    assert "This is a quoted text." in output
    assert "]" in output


def test_block_quote_with_attribution(simple_document, mock_builder):
    """Test that block quotes with attribution are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a block quote
    block_quote = nodes.block_quote()
    translator.visit_block_quote(block_quote)

    # Paragraph inside block quote
    para = nodes.paragraph(text="To be or not to be.")
    translator.visit_paragraph(para)
    translator.visit_Text(nodes.Text("To be or not to be."))
    translator.depart_Text(nodes.Text("To be or not to be."))
    translator.depart_paragraph(para)

    # Attribution
    attribution = nodes.attribution(text="Shakespeare")
    translator.visit_attribution(attribution)
    translator.visit_Text(nodes.Text("Shakespeare"))
    translator.depart_Text(nodes.Text("Shakespeare"))
    translator.depart_attribution(attribution)

    translator.depart_block_quote(block_quote)

    output = translator.astext()
    # Typst block quote with attribution
    assert "#quote[" in output
    assert "To be or not to be." in output
    assert "attribution: [Shakespeare]" in output
    assert "]" in output


def test_nested_block_quote(simple_document, mock_builder):
    """Test that nested block quotes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Outer block quote
    outer_quote = nodes.block_quote()
    translator.visit_block_quote(outer_quote)

    # Paragraph in outer quote
    para1 = nodes.paragraph(text="Outer quote.")
    translator.visit_paragraph(para1)
    translator.visit_Text(nodes.Text("Outer quote."))
    translator.depart_Text(nodes.Text("Outer quote."))
    translator.depart_paragraph(para1)

    # Inner block quote
    inner_quote = nodes.block_quote()
    translator.visit_block_quote(inner_quote)

    # Paragraph in inner quote
    para2 = nodes.paragraph(text="Inner quote.")
    translator.visit_paragraph(para2)
    translator.visit_Text(nodes.Text("Inner quote."))
    translator.depart_Text(nodes.Text("Inner quote."))
    translator.depart_paragraph(para2)

    translator.depart_block_quote(inner_quote)
    translator.depart_block_quote(outer_quote)

    output = translator.astext()
    # Nested quotes should both use #quote[]
    assert output.count("#quote[") == 2
    assert "Outer quote." in output
    assert "Inner quote." in output


def test_image_conversion(simple_document, mock_builder):
    """Test that image nodes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an image node
    image = nodes.image(uri="path/to/image.png")
    translator.visit_image(image)
    translator.depart_image(image)

    output = translator.astext()
    # Typst image syntax: #image("path")
    assert "#image(" in output
    assert "path/to/image.png" in output


def test_image_with_attributes(simple_document, mock_builder):
    """Test that image nodes with attributes are converted correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an image node with width and alt attributes
    image = nodes.image(uri="diagram.svg")
    image["width"] = "300px"
    image["alt"] = "System diagram"
    translator.visit_image(image)
    translator.depart_image(image)

    output = translator.astext()
    # Image with attributes
    assert "#image(" in output
    assert "diagram.svg" in output
    assert "width:" in output


def test_image_relative_path(simple_document, mock_builder):
    """Test that relative image paths are handled correctly."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an image with relative path
    image = nodes.image(uri="../images/logo.png")
    translator.visit_image(image)
    translator.depart_image(image)

    output = translator.astext()
    # Should preserve relative path
    assert "#image(" in output
    assert "../images/logo.png" in output


def test_figure_with_caption(simple_document, mock_builder):
    """Test that figure with caption is converted to Typst #figure() syntax."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a figure with image and caption
    # Figure structure: figure > (image, caption)
    figure = nodes.figure()
    image = nodes.image(uri="diagram.png")
    caption = nodes.caption()
    caption += nodes.Text("Figure caption text")

    figure += image
    figure += caption

    # Visit using walkabout
    figure.walkabout(translator)

    output = translator.astext()

    # Check that Typst #figure() syntax is generated
    assert "#figure(" in output
    assert "#image(" in output or "image(" in output
    assert "diagram.png" in output
    assert "caption:" in output
    assert "Figure caption text" in output


def test_figure_with_label(simple_document, mock_builder):
    """Test that figure with label generates proper Typst label."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a figure with label (target node with ids)
    figure = nodes.figure(ids=["fig-example"])
    image = nodes.image(uri="example.png")
    caption = nodes.caption()
    caption += nodes.Text("An example figure")

    figure += image
    figure += caption

    # Visit using walkabout
    figure.walkabout(translator)

    output = translator.astext()

    # Check that Typst label is generated
    assert "#figure(" in output
    assert "<fig-example>" in output or "label(" in output
    assert "An example figure" in output


def test_figure_without_caption(simple_document, mock_builder):
    """Test that figure without caption still generates #figure()."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a figure with only image
    figure = nodes.figure()
    image = nodes.image(uri="simple.png")
    figure += image

    # Visit using walkabout
    figure.walkabout(translator)

    output = translator.astext()

    # Should still generate figure syntax even without caption
    assert "#figure(" in output or "#image(" in output
    assert "simple.png" in output


def test_target_label_generation(simple_document, mock_builder):
    """Test that target nodes generate Typst labels."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a target node with id
    target = nodes.target(ids=["my-label"])

    # Visit using walkabout
    target.walkabout(translator)

    output = translator.astext()

    # Check that Typst label is generated
    assert "<my-label>" in output


def test_reference_to_target(simple_document, mock_builder):
    """Test that reference nodes generate Typst links."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a reference to an internal target
    reference = nodes.reference(refuri="#section-1")
    reference += nodes.Text("See Section 1")

    # Visit using walkabout
    reference.walkabout(translator)

    output = translator.astext()

    # Check that Typst link is generated
    assert "#link(" in output
    assert "See Section 1" in output


def test_external_reference(simple_document, mock_builder):
    """Test that external references generate proper Typst links."""
    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create an external reference
    reference = nodes.reference(refuri="https://example.com")
    reference += nodes.Text("External Link")

    # Visit using walkabout
    reference.walkabout(translator)

    output = translator.astext()

    # Check that Typst external link is generated
    assert '#link("https://example.com")' in output
    assert "External Link" in output


def test_pending_xref_doc_reference(simple_document, mock_builder):
    """Test that pending_xref for document references are handled."""
    from sphinx import addnodes

    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a pending cross-reference to a document
    xref = addnodes.pending_xref(
        refdomain="std",
        reftype="doc",
        reftarget="other_document",
        refexplicit=False,
    )
    xref += nodes.Text("Other Document")

    # Visit using walkabout
    xref.walkabout(translator)

    output = translator.astext()

    # Should generate a link (pending_xref is typically resolved by Sphinx,
    # but we handle the fallback case)
    # For now, we expect it to extract the text content
    assert "Other Document" in output


def test_pending_xref_with_refid(simple_document, mock_builder):
    """Test that pending_xref with refid generates proper reference."""
    from sphinx import addnodes

    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a pending cross-reference with refid
    xref = addnodes.pending_xref(
        refdomain="std",
        reftype="ref",
        reftarget="section-label",
        refexplicit=True,
    )
    xref += nodes.inline(text="Section Reference")

    # Visit using walkabout
    xref.walkabout(translator)

    output = translator.astext()

    # Should handle the cross-reference
    assert "Section Reference" in output


def test_toctree_generates_outline(simple_document, mock_builder):
    """
    Test that toctree node generates #include() directives.

    Updated for Requirement 13: toctree now generates #include() instead of #outline()
    """
    from sphinx import addnodes

    from sphinxcontrib.typst.translator import TypstTranslator

    translator = TypstTranslator(simple_document, mock_builder)

    # Create a toctree node
    toctree = addnodes.toctree()
    toctree["entries"] = [
        ("Introduction", "intro"),
        ("Getting Started", "getting_started"),
        ("API Reference", "api"),
    ]

    # Visit using walkabout
    toctree.walkabout(translator)

    output = translator.astext()

    # Should generate #include() directives with heading offset (Requirement 13)
    assert "#include(" in output
    assert '#include("intro.typ")' in output
    assert '#include("getting_started.typ")' in output
    assert '#include("api.typ")' in output
    assert "#set heading(offset: 1)" in output
