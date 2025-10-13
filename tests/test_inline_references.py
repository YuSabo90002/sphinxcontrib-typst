"""
Tests for inline reference node conversion to Typst.

Task 7.4: インライン相互参照（inline reference）の処理
"""

from docutils import nodes
from docutils.parsers.rst import states
from docutils.utils import Reporter
from sphinx.testing.util import SphinxTestApp

from sphinxcontrib.typst.translator import TypstTranslator
from sphinxcontrib.typst.writer import TypstWriter


def create_document():
    """Helper function to create a minimal document with reporter."""
    reporter = Reporter("", 2, 4)
    doc = nodes.document("", reporter=reporter)
    doc.settings = states.Struct()
    doc.settings.env = None
    doc.settings.language_code = "en"
    doc.settings.strict_visitor = False
    return doc


class TestInlineReferenceConversion:
    """Test inline reference node conversion."""

    def test_inline_without_xref_class(self, temp_sphinx_app: SphinxTestApp):
        """Test that regular inline nodes are processed normally."""
        inline = nodes.inline()
        text = nodes.Text("regular inline text")
        inline += text

        doc = create_document()
        para = nodes.paragraph()
        para += inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        assert "regular inline text" in output
        # Should not have any special formatting
        assert "#link" not in output

    def test_inline_with_xref_class(self, temp_sphinx_app: SphinxTestApp):
        """Test that inline nodes with 'xref' class are handled specially."""
        inline = nodes.inline(classes=["xref", "std", "std-ref"])
        text = nodes.Text("reference text")
        inline += text

        doc = create_document()
        para = nodes.paragraph()
        para += inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Should output the text content
        assert "reference text" in output

    def test_inline_with_doc_class(self, temp_sphinx_app: SphinxTestApp):
        """Test that inline nodes with 'doc' class are handled."""
        inline = nodes.inline(classes=["xref", "doc"])
        text = nodes.Text("document reference")
        inline += text

        doc = create_document()
        para = nodes.paragraph()
        para += inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        assert "document reference" in output

    def test_inline_in_paragraph(self, temp_sphinx_app: SphinxTestApp):
        """Test inline reference within paragraph context."""
        para = nodes.paragraph()
        para += nodes.Text("See ")

        inline = nodes.inline(classes=["xref", "std", "std-ref"])
        inline += nodes.Text("section 1")
        para += inline

        para += nodes.Text(" for details.")

        doc = create_document()
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        assert "See " in output
        assert "section 1" in output
        assert " for details." in output

    def test_inline_empty_content(self, temp_sphinx_app: SphinxTestApp):
        """Test inline node with empty content."""
        inline = nodes.inline(classes=["xref"])

        doc = create_document()
        para = nodes.paragraph()
        para += inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Should not crash, output should be valid
        assert isinstance(output, str)

    def test_nested_inline_nodes(self, temp_sphinx_app: SphinxTestApp):
        """Test nested inline nodes."""
        outer_inline = nodes.inline()
        inner_inline = nodes.inline(classes=["xref"])
        inner_inline += nodes.Text("nested ref")
        outer_inline += inner_inline

        doc = create_document()
        para = nodes.paragraph()
        para += outer_inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        assert "nested ref" in output

    def test_inline_with_multiple_classes(self, temp_sphinx_app: SphinxTestApp):
        """Test inline node with multiple CSS classes."""
        inline = nodes.inline(classes=["xref", "std", "std-ref", "custom"])
        inline += nodes.Text("multi-class ref")

        doc = create_document()
        para = nodes.paragraph()
        para += inline
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        assert "multi-class ref" in output

    def test_inline_code_reference(self, temp_sphinx_app: SphinxTestApp):
        """Test inline code within reference context."""
        # Inline code should be handled as code, not as xref
        literal = nodes.literal()
        literal += nodes.Text("code_reference")

        doc = create_document()
        para = nodes.paragraph()
        para += literal
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Literal should use backticks
        assert "`code_reference`" in output
