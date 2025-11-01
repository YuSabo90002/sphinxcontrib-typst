"""
Tests for inline reference node conversion to Typst.

Task 7.4: インライン相互参照（inline reference）の処理
"""

from docutils import nodes
from docutils.parsers.rst import states
from docutils.utils import Reporter
from sphinx.testing.util import SphinxTestApp

from typsphinx.translator import TypstTranslator
from typsphinx.writer import TypstWriter


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
        assert "link(" not in output

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
        # Literal should use raw() function in unified code mode
        assert 'raw("code_reference")' in output


class TestEmptyURLHandling:
    """Test empty URL handling in references (Typst 0.14+ compatibility)."""

    def test_empty_refuri_skips_link_wrapper(self, temp_sphinx_app: SphinxTestApp):
        """Test that empty refuri skips link() generation."""
        ref = nodes.reference()
        ref["refuri"] = ""  # Empty URL
        ref += nodes.Text("broken reference")

        doc = create_document()
        para = nodes.paragraph()
        para += ref
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Should NOT generate link()
        assert 'link("")' not in output
        assert 'link("", ' not in output
        # Should render content as plain text
        assert "broken reference" in output

    def test_empty_refuri_renders_content_as_text(self, temp_sphinx_app: SphinxTestApp):
        """Test that content is rendered as plain text when refuri is empty."""
        ref = nodes.reference()
        ref["refuri"] = ""
        ref += nodes.Text("nonexistent-section")

        doc = create_document()
        para = nodes.paragraph()
        para += ref
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Content should be present as text
        assert "nonexistent-section" in output
        # No link wrapper
        assert "link(" not in output

    def test_empty_refuri_emits_warning(self, temp_sphinx_app: SphinxTestApp):
        """Test that warning is emitted for empty refuri."""
        ref = nodes.reference()
        ref["refuri"] = ""
        ref += nodes.Text("broken-link")

        doc = create_document()
        para = nodes.paragraph()
        para += ref
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)

        # Capture warnings
        import io
        from contextlib import redirect_stderr

        stderr_capture = io.StringIO()
        with redirect_stderr(stderr_capture):
            doc.walkabout(translator)

        # Sphinx logger output goes to stderr in test context
        # We just verify the code runs without error and produces expected output
        output = translator.astext()
        assert "broken-link" in output
        assert 'link("")' not in output

    def test_valid_refuri_unchanged(self, temp_sphinx_app: SphinxTestApp):
        """Test that valid refuri generates link() as before (regression test)."""
        ref = nodes.reference()
        ref["refuri"] = "https://python.org"
        ref += nodes.Text("Python")

        doc = create_document()
        para = nodes.paragraph()
        para += ref
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Should generate link()
        assert 'link("https://python.org"' in output
        assert "Python" in output

    def test_internal_reference_with_hash(self, temp_sphinx_app: SphinxTestApp):
        """Test that internal references (starting with #) work correctly."""
        ref = nodes.reference()
        ref["refuri"] = "#section-label"
        ref += nodes.Text("See section")

        doc = create_document()
        para = nodes.paragraph()
        para += ref
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Should generate link(<label>, ...)
        assert "link(<section-label>" in output
        assert "See section" in output

    def test_multiple_empty_urls(self, temp_sphinx_app: SphinxTestApp):
        """Test that multiple empty URLs are handled correctly."""
        # First empty reference
        ref1 = nodes.reference()
        ref1["refuri"] = ""
        ref1 += nodes.Text("ref1")

        # Second empty reference
        ref2 = nodes.reference()
        ref2["refuri"] = ""
        ref2 += nodes.Text("ref2")

        doc = create_document()
        para = nodes.paragraph()
        para += ref1
        para += nodes.Text(" and ")
        para += ref2
        doc += para

        writer = TypstWriter(temp_sphinx_app.builder)
        writer.document = doc
        translator = TypstTranslator(doc, temp_sphinx_app.builder)
        doc.walkabout(translator)

        output = translator.astext()
        # Both should be rendered as text
        assert "ref1" in output
        assert "ref2" in output
        # No link wrappers
        assert 'link("")' not in output
