"""
Typst translator for docutils nodes.

This module implements the TypstTranslator class, which translates docutils
nodes to Typst markup.
"""

import re
from typing import Any, List, Optional, Union

from docutils import nodes
from sphinx import addnodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

logger = logging.getLogger(__name__)


class TypstTranslator(SphinxTranslator):
    """
    Translator class that converts docutils nodes to Typst markup.

    This translator visits nodes in the document tree and generates
    corresponding Typst markup.
    """

    def __init__(self, document: nodes.document, builder: Any) -> None:
        """
        Initialize the translator.

        Args:
            document: The docutils document to translate
            builder: The Sphinx builder instance
        """
        super().__init__(document, builder)
        self.builder = builder
        self.body = []

        # State management variables
        self.section_level = 0
        self.in_figure = False
        self.in_table = False
        self.in_thead = False  # Track if currently in table header
        self.in_caption = False
        self.list_stack = []  # Track list nesting: 'bullet' or 'enumerated'

        # Figure-specific state
        self.figure_content = []
        self.figure_caption = ""

        # Code block container state (Issue #20)
        self.in_captioned_code_block = False
        self.code_block_caption = ""
        self.code_block_label = ""

        # Unified code mode state
        self.in_paragraph = False
        self.paragraph_has_content = False  # Track if paragraph has any content nodes
        self.in_list_item = False  # Track if currently in a list item
        self.in_literal_block = False  # Track if currently in a code block

        # Stream-based list rendering state (Issue #61)
        self.is_first_list_item = True  # Track if current item is first in list
        self.list_item_needs_separator = (
            False  # Track if + is needed before next element
        )
        self._in_reference_with_target = (
            False  # Track if reference has following target for markup mode wrapping
        )
        self._in_markup_mode = (
            False  # Track if currently inside markup mode block [...] for # prefix
        )
        self.in_desc_parameter = (
            False  # Track if inside desc_parameter to avoid newlines between text nodes
        )
        self._in_link = False  # Track if inside link() function for + concatenation
        self._desc_parameter_has_content: bool = (
            False  # Track if desc_parameter has content for + separator
        )
        self._link_has_content: bool = (
            False  # Track if link has content for + separator
        )

        # Definition list state
        self.in_definition_list = False
        self.current_term_buffer: Union[str, List[str], None] = None
        self.current_definition_buffer: Optional[List[str]] = None
        self.definition_list_items = []  # List of (term, definition) tuples
        self.saved_body: Optional[List[Any]] = (
            None  # Used by definition lists for body swapping
        )

    def astext(self) -> str:
        """
        Return the translated text as a string.

        Returns:
            The translated Typst markup
        """
        return "".join(self.body)

    def add_text(self, text: str) -> None:
        """
        Add text to the output body or table cell content.

        Args:
            text: The text to add
        """
        if (
            hasattr(self, "in_table")
            and self.in_table
            and hasattr(self, "table_cell_content")
        ):
            self.table_cell_content.append(text)
        else:
            self.body.append(text)

    def _add_paragraph_separator(self) -> None:
        """
        Add + operator for concatenation in paragraph if not first node.

        In unified code mode, paragraph content nodes are concatenated with +.
        This method adds ' + ' before each node except the first one.
        """
        if self.in_paragraph and self.paragraph_has_content:
            self.add_text("\n")
        if self.in_paragraph:
            self.paragraph_has_content = True

    def visit_document(self, node: nodes.document) -> None:
        """
        Visit a document node.

        Generates opening code block wrapper for unified code mode.

        Args:
            node: The document node
        """
        # Start code block for unified code mode (all content uses function syntax without # prefix)
        self.add_text("#{\n")

    def depart_document(self, node: nodes.document) -> None:
        """
        Depart a document node.

        Generates closing code block wrapper for unified code mode.

        Args:
            node: The document node
        """
        # Close code block for unified code mode
        self.add_text("}\n")

    def visit_section(self, node: nodes.section) -> None:
        """
        Visit a section node.

        Args:
            node: The section node
        """
        # Increment section level
        self.section_level += 1

    def depart_section(self, node: nodes.section) -> None:
        """
        Depart a section node.

        Args:
            node: The section node
        """
        # Decrement section level
        self.section_level -= 1
        # Add a newline after sections
        self.add_text("\n")

    def visit_title(self, node: nodes.title) -> None:
        """
        Visit a title node.

        Generates heading() function call with level parameter.
        Child text nodes will be wrapped in text() automatically.

        Args:
            node: The title node
        """
        # Use heading() function (no # prefix in code mode)
        self.add_text(f"heading(level: {self.section_level}, ")

    def depart_title(self, node: nodes.title) -> None:
        """
        Depart a title node.

        Closes heading() function call.

        Args:
            node: The title node
        """
        # Close heading() function
        self.add_text(")\n\n")

    def visit_subtitle(self, node: nodes.subtitle) -> None:
        """
        Visit a subtitle node.

        Generates emph() function for subtitle (no # prefix in code mode).
        Child text nodes will be wrapped in text() automatically.

        Args:
            node: The subtitle node
        """
        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Use emph() function for subtitle (no # prefix in code mode)
        self.add_text("emph(")

        # Store state to restore in depart
        self._subtitle_was_in_paragraph = was_in_paragraph

    def depart_subtitle(self, node: nodes.subtitle) -> None:
        """
        Depart a subtitle node.

        Closes emph() function.

        Args:
            node: The subtitle node
        """
        # Close emph() function
        self.add_text(")\n\n")

        # Restore paragraph state
        if hasattr(self, "_subtitle_was_in_paragraph"):
            self.in_paragraph = self._subtitle_was_in_paragraph
            delattr(self, "_subtitle_was_in_paragraph")

    def visit_compound(self, node: nodes.compound) -> None:
        """
        Visit a compound node.

        Compound nodes are containers that group related content.
        They are often used to wrap toctree directives.

        Args:
            node: The compound node
        """
        # Compound nodes are just containers, process their children
        pass

    def depart_compound(self, node: nodes.compound) -> None:
        """
        Depart a compound node.

        Args:
            node: The compound node
        """
        pass

    def visit_container(self, node: nodes.container) -> None:
        """
        Visit a container node.

        Handle Sphinx-generated containers, particularly literal-block-wrapper
        for captioned code blocks (Issue #20).

        Args:
            node: The container node
        """
        # Check if this is a literal-block-wrapper (captioned code block)
        if "literal-block-wrapper" in node.get("classes", []):
            self.in_captioned_code_block = True
            # Caption and literal_block children will be processed separately
            # We need to extract caption text first
            for child in node.children:
                if isinstance(child, nodes.caption):
                    self.code_block_caption = child.astext()
                elif isinstance(child, nodes.literal_block):
                    # Extract label from :name: option
                    if child.get("names"):
                        self.code_block_label = child.get("names")[0]
        # Other container types: just process children
        pass

    def depart_container(self, node: nodes.container) -> None:
        """
        Depart a container node.

        Args:
            node: The container node
        """
        # Reset state after literal-block-wrapper
        if "literal-block-wrapper" in node.get("classes", []):
            self.in_captioned_code_block = False
            self.code_block_caption = ""
            self.code_block_label = ""

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        """
        Visit a paragraph node.

        Wraps paragraph content in par() function for unified code mode.
        Code mode doesn't auto-recognize paragraph breaks from blank lines.

        Exception: Inside list items, paragraphs are not wrapped in par()
        to avoid syntax like "- par(text(...))" which is invalid.

        Args:
            node: The paragraph node
        """
        # Skip par() wrapping inside list items
        if self.in_list_item:
            self.in_paragraph = False
            return

        # Start par() with {} content block (no # prefix in code mode)
        self.in_paragraph = True
        self.paragraph_has_content = False
        self.add_text("par({")

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        """
        Depart a paragraph node.

        Closes par({}) function and adds spacing.

        Args:
            node: The paragraph node
        """
        # Skip closing if inside list items
        if self.in_list_item:
            return

        # Close par({}) content block and add spacing
        self.in_paragraph = False
        self.paragraph_has_content = False
        self.add_text("})\n\n")

    def visit_comment(self, node: nodes.comment) -> None:
        """
        Visit a comment node.

        Comments are skipped entirely in Typst output as they are meant
        for source-level documentation only.

        Args:
            node: The comment node

        Raises:
            nodes.SkipNode: Always raised to skip the comment
        """
        raise nodes.SkipNode

    def depart_comment(self, node: nodes.comment) -> None:
        """
        Depart a comment node.

        Args:
            node: The comment node

        Note:
            This method is not called when SkipNode is raised in visit_comment.
        """
        pass

    def visit_raw(self, node: nodes.raw) -> None:
        """
        Visit a raw node.

        Pass through content if format is 'typst', otherwise skip.

        Args:
            node: The raw node

        Raises:
            nodes.SkipNode: When format is not 'typst'
        """
        format_name = node.get("format", "").lower()

        if format_name == "typst":
            # Output the raw Typst content directly
            content = node.astext()
            if content:  # Only add non-empty content
                self.add_text(content)
                self.add_text("\n\n")
            raise nodes.SkipNode
        else:
            # Skip content for other formats
            logger.debug(f"Skipping raw node with format: {format_name}")
            raise nodes.SkipNode

    def depart_raw(self, node: nodes.raw) -> None:
        """
        Depart a raw node.

        Args:
            node: The raw node

        Note:
            This method is not called when SkipNode is raised in visit_raw.
        """
        pass

    def visit_Text(self, node: nodes.Text) -> None:
        """
        Visit a text node.

        Wraps text in text() function for unified code mode.
        Uses string escaping (not markup escaping).

        Exception: Inside literal blocks, text is output directly
        without text() wrapping to preserve code content.

        Args:
            node: The text node
        """
        text_content = node.astext()

        # Inside literal blocks, output text directly (no wrapping)
        if self.in_literal_block:
            self.add_text(text_content)
            return

        # Escape string content (order matters: backslash first)
        text_content = text_content.replace("\\", "\\\\")  # Backslash
        text_content = text_content.replace('"', '\\"')  # Quote
        text_content = text_content.replace("\n", "\\n")  # Newline
        text_content = text_content.replace("\r", "\\r")  # Carriage return
        text_content = text_content.replace("\t", "\\t")  # Tab

        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Add separator before text
        # In list items: use newline separator
        # In desc_parameter or link: use + operator for concatenation
        # In paragraphs: handled by _add_paragraph_separator
        if self.in_desc_parameter:
            # In desc_parameter, add + before text (except first)
            if (
                hasattr(self, "_desc_parameter_has_content")
                and self._desc_parameter_has_content
            ):
                self.add_text(" + ")
        elif hasattr(self, "_in_link") and self._in_link:
            # In link(), add + before text (except first)
            if hasattr(self, "_link_has_content") and self._link_has_content:
                self.add_text(" + ")
        elif self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Determine if we need # prefix (in markup mode)
        prefix = "#" if self._in_markup_mode else ""

        # Wrap in text() function (# prefix needed in markup mode)
        self.add_text(f'{prefix}text("{text_content}")')

        # Mark that content was added
        if self.in_desc_parameter:
            self._desc_parameter_has_content = True
        elif hasattr(self, "_in_link") and self._in_link:
            self._link_has_content = True
        elif self.in_list_item:
            self.list_item_needs_separator = True

    def depart_Text(self, node: nodes.Text) -> None:
        """
        Depart a text node.

        Args:
            node: The text node
        """
        # Text nodes don't need closing
        pass

    def visit_emphasis(self, node: nodes.emphasis) -> None:
        """
        Visit an emphasis (italic) node.

        Generates emph() function call. Child text nodes will be
        wrapped in text() automatically.

        Args:
            node: The emphasis node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Save and reset list item separator for children (they're inside this element)
        was_list_item_needs_separator = self.list_item_needs_separator

        # Since emph({}) uses content block, treat it like list_item
        # Children need newline separators, not + operators
        was_in_list_item = self.in_list_item
        self.in_list_item = True
        self.list_item_needs_separator = False

        # Determine if we need # prefix (in markup mode)
        prefix = "#" if self._in_markup_mode else ""

        # Use emph({}) function with content block
        self.add_text(f"{prefix}emph({{")

        # Store state to restore in depart
        self._emph_was_in_paragraph = was_in_paragraph
        self._emph_was_in_list_item = was_in_list_item
        self._emph_was_list_item_needs_separator = was_list_item_needs_separator

    def depart_emphasis(self, node: nodes.emphasis) -> None:
        """
        Depart an emphasis (italic) node.

        Closes emph({}) function call.

        Args:
            node: The emphasis node
        """
        # Close emph({}) function
        self.add_text("})")

        # Restore paragraph state
        if hasattr(self, "_emph_was_in_paragraph"):
            self.in_paragraph = self._emph_was_in_paragraph
            delattr(self, "_emph_was_in_paragraph")

        # Restore in_list_item state
        if hasattr(self, "_emph_was_in_list_item"):
            self.in_list_item = self._emph_was_in_list_item
            delattr(self, "_emph_was_in_list_item")

        # Restore and mark that next element needs separator
        if hasattr(self, "_emph_was_list_item_needs_separator"):
            # Restore previous state, then mark next element needs separator
            if self.in_list_item:
                self.list_item_needs_separator = True
            delattr(self, "_emph_was_list_item_needs_separator")

    def visit_strong(self, node: nodes.strong) -> None:
        """
        Visit a strong (bold) node.

        Generates strong() function call. Child text nodes will be
        wrapped in text() automatically.

        Args:
            node: The strong node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Save and reset list item separator for children (they're inside this element)
        was_list_item_needs_separator = self.list_item_needs_separator

        # Since strong({}) uses content block, treat it like list_item
        # Children need newline separators, not + operators
        was_in_list_item = self.in_list_item
        self.in_list_item = True
        self.list_item_needs_separator = False

        # Determine if we need # prefix (in markup mode)
        prefix = "#" if self._in_markup_mode else ""

        # Use strong({}) function with content block
        self.add_text(f"{prefix}strong({{")

        # Store state to restore in depart
        self._strong_was_in_paragraph = was_in_paragraph
        self._strong_was_in_list_item = was_in_list_item
        self._strong_was_list_item_needs_separator = was_list_item_needs_separator

    def depart_strong(self, node: nodes.strong) -> None:
        """
        Depart a strong (bold) node.

        Closes strong({}) function call.

        Args:
            node: The strong node
        """
        # Close strong({}) function
        self.add_text("})")

        # Restore paragraph state
        if hasattr(self, "_strong_was_in_paragraph"):
            self.in_paragraph = self._strong_was_in_paragraph
            delattr(self, "_strong_was_in_paragraph")

        # Restore in_list_item state
        if hasattr(self, "_strong_was_in_list_item"):
            self.in_list_item = self._strong_was_in_list_item
            delattr(self, "_strong_was_in_list_item")

        # Restore and mark that next element needs separator
        if hasattr(self, "_strong_was_list_item_needs_separator"):
            # Restore previous state, then mark next element needs separator
            if self.in_list_item:
                self.list_item_needs_separator = True
            delattr(self, "_strong_was_list_item_needs_separator")

    def visit_literal(self, node: nodes.literal) -> None:
        """
        Visit a literal (inline code) node.

        Generates raw() function call with backtick raw string.
        Uses backticks to avoid escaping issues.

        Args:
            node: The literal node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Get code content directly
        code_content = node.astext()

        # Escape code content for string parameter
        escaped_code = code_content.replace("\\", "\\\\")  # Backslash
        escaped_code = escaped_code.replace('"', '\\"')  # Quote

        # Generate raw() function with string parameter (no # prefix in code mode)
        # Using string instead of backtick raw literal for compatibility with + operator
        self.add_text(f'raw("{escaped_code}")')

        # Mark that next element in list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

        # Skip processing child text nodes (we already got the content)
        raise nodes.SkipNode

    def depart_literal(self, node: nodes.literal) -> None:
        """
        Depart a literal (inline code) node.

        This is not called when SkipNode is raised in visit_literal.

        Args:
            node: The literal node
        """
        pass

    def visit_subscript(self, node: nodes.subscript) -> None:
        """
        Visit a subscript node.

        Generates sub() function call. Child text nodes will be
        wrapped in text() automatically.

        Args:
            node: The subscript node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Use sub() function (no # prefix in code mode)
        self.add_text("sub(")

        # Store state to restore in depart
        self._subscript_was_in_paragraph = was_in_paragraph

    def depart_subscript(self, node: nodes.subscript) -> None:
        """
        Depart a subscript node.

        Closes sub() function call.

        Args:
            node: The subscript node
        """
        # Close sub() function
        self.add_text(")")

        # Restore paragraph state
        if hasattr(self, "_subscript_was_in_paragraph"):
            self.in_paragraph = self._subscript_was_in_paragraph
            delattr(self, "_subscript_was_in_paragraph")

    def visit_superscript(self, node: nodes.superscript) -> None:
        """
        Visit a superscript node.

        Generates super() function call. Child text nodes will be
        wrapped in text() automatically.

        Args:
            node: The superscript node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Use super() function (no # prefix in code mode)
        self.add_text("super(")

        # Store state to restore in depart
        self._superscript_was_in_paragraph = was_in_paragraph

    def depart_superscript(self, node: nodes.superscript) -> None:
        """
        Depart a superscript node.

        Closes super() function call.

        Args:
            node: The superscript node
        """
        # Close super() function
        self.add_text(")")

        # Restore paragraph state
        if hasattr(self, "_superscript_was_in_paragraph"):
            self.in_paragraph = self._superscript_was_in_paragraph
            delattr(self, "_superscript_was_in_paragraph")

    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        """
        Visit a bullet list node.

        Outputs list( and prepares for stream-based item rendering.

        Args:
            node: The bullet list node
        """
        # Add + separator if nested in a list item
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        self.list_stack.append("bullet")
        self.add_text("list(")

        # Save parent list state and start fresh for nested list
        if len(self.list_stack) > 1:  # Nested list
            self._saved_is_first_list_item = self.is_first_list_item
            self._saved_list_item_needs_separator = self.list_item_needs_separator

        self.is_first_list_item = True

        # Mark that next element in parent list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        """
        Depart a bullet list node.

        Closes the list() function.

        Args:
            node: The bullet list node
        """
        self.list_stack.pop()
        self.add_text(")")

        # Restore parent list state if nested
        if hasattr(self, "_saved_is_first_list_item"):
            self.is_first_list_item = self._saved_is_first_list_item
            delattr(self, "_saved_is_first_list_item")
        if hasattr(self, "_saved_list_item_needs_separator"):
            self.list_item_needs_separator = self._saved_list_item_needs_separator
            delattr(self, "_saved_list_item_needs_separator")

        # Add newlines only if this is a top-level list
        if not self.list_stack:
            self.add_text("\n\n")

    def visit_enumerated_list(self, node: nodes.enumerated_list) -> None:
        """
        Visit an enumerated (numbered) list node.

        Outputs enum( and prepares for stream-based item rendering.

        Args:
            node: The enumerated list node
        """
        # Add + separator if nested in a list item
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        self.list_stack.append("enumerated")
        self.add_text("enum(")

        # Save parent list state and start fresh for nested list
        if len(self.list_stack) > 1:  # Nested list
            self._saved_is_first_list_item = self.is_first_list_item
            self._saved_list_item_needs_separator = self.list_item_needs_separator

        self.is_first_list_item = True

        # Mark that next element in parent list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

    def depart_enumerated_list(self, node: nodes.enumerated_list) -> None:
        """
        Depart an enumerated (numbered) list node.

        Closes the enum() function.

        Args:
            node: The enumerated list node
        """
        self.list_stack.pop()
        self.add_text(")")

        # Restore parent list state if nested
        if hasattr(self, "_saved_is_first_list_item"):
            self.is_first_list_item = self._saved_is_first_list_item
            delattr(self, "_saved_is_first_list_item")
        if hasattr(self, "_saved_list_item_needs_separator"):
            self.list_item_needs_separator = self._saved_list_item_needs_separator
            delattr(self, "_saved_list_item_needs_separator")

        # Add newlines only if this is a top-level list
        if not self.list_stack:
            self.add_text("\n\n")

    def visit_list_item(self, node: nodes.list_item) -> None:
        """
        Visit a list item node.

        Adds comma separator if not first item, then prepares for item content.

        Args:
            node: The list item node
        """
        # Mark that we're in a list item (disable par() wrapping)
        self.in_list_item = True

        # Add comma before 2nd+ items
        if not self.is_first_list_item:
            self.add_text(", ")
        self.is_first_list_item = False

        # Wrap list item content in { } block
        # This allows multiple statements without + operator
        self.add_text("{\n")

        # Reset separator flag for item content
        self.list_item_needs_separator = False

    def depart_list_item(self, node: nodes.list_item) -> None:
        """
        Depart a list item node.

        Close the { } block wrapper and mark that we're no longer in a list item.

        Args:
            node: The list item node
        """
        # Close the { } block
        self.add_text("\n}")

        self.in_list_item = False

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        """
        Visit a literal block (code block) node.

        Implements Task 4.2.2: codly forced usage with #codly-range() for highlighted lines
        Design 3.5: All code blocks use codly, with #codly-range() for highlights
        Requirements 7.3, 7.4: Support line numbers and highlighted lines
        Issue #20: Support :linenos:, :caption:, and :name: options
        Issue #31: Support :lineno-start: and :dedent: options

        Args:
            node: The literal block node
        """
        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Mark that we're in a literal block (disable text() wrapping)
        self.in_literal_block = True

        # Issue #20: Handle captioned code blocks
        # If we're in a captioned code block (literal-block-wrapper container),
        # wrap the code block in figure() (no # prefix in code mode)
        if self.in_captioned_code_block and self.code_block_caption:
            # Escape special characters in caption
            escaped_caption = self.code_block_caption
            # Start figure with caption (will add closing bracket in depart)
            # No # prefix in code mode
            self.add_text(f"figure(caption: [{escaped_caption}])[\n")

        # If in list item, wrap codly() calls and code block in { } to make it an expression
        if self.in_list_item:
            self.add_text("{\n")

        # Check for :linenos: option (Issue #20)
        # If linenos is not set or False, disable line numbers in codly
        linenos = node.get("linenos", False)
        if not linenos:
            # No # prefix in code mode
            self.add_text("codly(number-format: none)\n")

        # Extract highlight_args if present (Task 4.2.2)
        highlight_args = node.get("highlight_args", {})
        hl_lines = highlight_args.get("hl_lines", [])

        # Issue #31: Support :lineno-start: option
        # Sphinx stores lineno-start in highlight_args['linenostart']
        lineno_start = highlight_args.get("linenostart")
        if linenos and lineno_start is not None:
            # No # prefix in code mode
            self.add_text(f"codly(start: {lineno_start})\n")

        # Generate codly-range() if highlight lines are specified
        if hl_lines:
            # Convert list of line numbers to Typst array format
            # Example: [2, 3] -> codly-range(highlight: (2, 3))
            # Example: [2, 4, 5, 6] -> codly-range(highlight: (2, 4, 5, 6))
            highlight_str = ", ".join(str(line) for line in hl_lines)
            # No # prefix in code mode
            self.add_text(f"codly-range(highlight: ({highlight_str}))\n")

        # Typst code block syntax: ```language\ncode\n```
        # Extract language if specified
        language = node.get("language", "")
        if language:
            self.add_text(f"```{language}\n")
        else:
            self.add_text("```\n")

    def depart_literal_block(self, node: nodes.literal_block) -> None:
        """
        Depart a literal block (code block) node.

        Issue #20: Handle closing figure bracket and labels.

        Args:
            node: The literal block node
        """
        # Clear literal block flag
        self.in_literal_block = False

        # Close code block
        self.add_text("\n```\n")

        # Close the { } wrapper if we're in a list item
        if self.in_list_item:
            self.add_text("}")

        # Issue #20: Close figure wrapper if we're in a captioned code block
        if self.in_captioned_code_block and self.code_block_caption:
            # Close the figure's trailing content block with ]
            self.add_text("]")
            # Add label if present
            if self.code_block_label:
                self.add_text(f" <{self.code_block_label}>")
            self.add_text("\n\n")
        elif node.get("names"):
            # Handle :name: option without :caption: - just add label after code block
            label = node.get("names")[0]
            self.add_text(f" <{label}>\n\n")
        else:
            # Normal code block - just add spacing
            self.add_text("\n")

        # Mark that next element in list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

    def visit_definition_list(self, node: nodes.definition_list) -> None:
        """
        Visit a definition list node.

        Collects all term-definition pairs and generates terms() function
        in unified code mode.

        Args:
            node: The definition list node
        """
        self.in_definition_list = True
        self.definition_list_items = []

    def depart_definition_list(self, node: nodes.definition_list) -> None:
        """
        Depart a definition list node.

        Generates terms() function with all collected term-definition pairs.

        Args:
            node: The definition list node
        """
        self.in_definition_list = False

        # Generate terms() function with all items (no # prefix in code mode)
        if self.definition_list_items:
            items_str = ", ".join(
                f"terms.item({term}, {definition})"
                for term, definition in self.definition_list_items
            )
            self.add_text(f"terms({items_str})\n\n")
        else:
            self.add_text("terms()\n\n")

        # Clear collected items
        self.definition_list_items = []

    def visit_definition_list_item(self, node: nodes.definition_list_item) -> None:
        """
        Visit a definition list item node.

        Args:
            node: The definition list item node
        """
        # Definition list items don't need special markup
        pass

    def depart_definition_list_item(self, node: nodes.definition_list_item) -> None:
        """
        Depart a definition list item node.

        Args:
            node: The definition list item node
        """
        # Definition list items don't need closing
        pass

    def visit_term(self, node: nodes.term) -> None:
        """
        Visit a term (definition list term) node.

        Starts buffering term content.

        Args:
            node: The term node
        """
        # Start buffering term content
        self.saved_body = self.body
        self.current_term_buffer = []
        self.body = self.current_term_buffer

    def depart_term(self, node: nodes.term) -> None:
        """
        Depart a term (definition list term) node.

        Saves buffered term content.

        Args:
            node: The term node
        """
        # Get buffered term content
        if isinstance(self.current_term_buffer, list):
            term_content = "".join(self.current_term_buffer).strip()
        else:
            term_content = ""

        # Restore original body
        if self.saved_body is not None:
            self.body = self.saved_body
        self.saved_body = None

        # Store term for later (will be paired with definition)
        self.current_term_buffer = term_content

    def visit_definition(self, node: nodes.definition) -> None:
        """
        Visit a definition (definition list definition) node.

        Starts buffering definition content.

        Args:
            node: The definition node
        """
        # Start buffering definition content
        self.saved_body = self.body
        self.current_definition_buffer = []
        self.body = self.current_definition_buffer

    def depart_definition(self, node: nodes.definition) -> None:
        """
        Depart a definition (definition list definition) node.

        Saves buffered definition content and pairs it with the term.

        Args:
            node: The definition node
        """
        # Get buffered definition content
        definition_content = "".join(self.current_definition_buffer or []).strip()

        # Restore original body
        if self.saved_body is not None:
            self.body = self.saved_body
        self.saved_body = None

        # Pair term and definition
        if isinstance(self.current_term_buffer, str):
            self.definition_list_items.append(
                (self.current_term_buffer, definition_content)
            )
            self.current_term_buffer = None

        self.current_definition_buffer = None

    def visit_figure(self, node: nodes.figure) -> None:
        """
        Visit a figure node.

        Generates figure() function call (no # prefix in code mode).

        Args:
            node: The figure node
        """
        self.in_figure = True
        self.figure_content = []  # Store figure content (image)
        self.figure_caption = ""  # Store caption text

        # Start figure with potential label (no # prefix in code mode)
        self.add_text("figure(\n")

    def depart_figure(self, node: nodes.figure) -> None:
        """
        Depart a figure node.

        Args:
            node: The figure node
        """
        # Close the figure
        if self.figure_caption:
            self.add_text(f",\n  caption: [{self.figure_caption}]")

        # Add label if figure has ids
        if node.get("ids"):
            label = node["ids"][0]
            self.add_text(f"\n) <{label}>\n\n")
        else:
            self.add_text("\n)\n\n")

        self.in_figure = False
        self.figure_content = []
        self.figure_caption = ""

    def visit_caption(self, node: nodes.caption) -> None:
        """
        Visit a caption node.

        Handles captions for both figures and code blocks (Issue #20).

        Args:
            node: The caption node
        """
        # For captioned code blocks, caption is already extracted in visit_container
        # We should skip output to avoid duplicate caption text
        if self.in_captioned_code_block:
            raise nodes.SkipNode
        # For figures, start collecting caption text
        self.in_caption = True

    def depart_caption(self, node: nodes.caption) -> None:
        """
        Depart a caption node.

        Args:
            node: The caption node
        """
        # Store caption text for figures
        if self.in_figure:
            self.figure_caption = node.astext()
        self.in_caption = False

    def visit_table(self, node: nodes.table) -> None:
        """
        Visit a table node.

        Args:
            node: The table node
        """
        self.in_table = True
        self.table_cells = []  # Store cells for table generation
        self.table_colcount = 0  # Track number of columns

    def _format_table_cell(self, cell: dict, indent: str = "  ") -> str:
        """
        Format a table cell with optional colspan/rowspan.

        Args:
            cell: Cell dictionary with 'content', 'colspan', 'rowspan'
            indent: Indentation string

        Returns:
            Formatted Typst cell string
        """
        content = cell["content"]
        colspan = cell.get("colspan", 1)
        rowspan = cell.get("rowspan", 1)

        # Normal cell (no spanning)
        if colspan == 1 and rowspan == 1:
            return f"{indent}{{{content}}},\n"

        # Cell with spanning - use table.cell()
        params = []
        if colspan > 1:
            params.append(f"colspan: {colspan}")
        if rowspan > 1:
            params.append(f"rowspan: {rowspan}")

        params_str = ", ".join(params)
        return f"{indent}table.cell({{{content}}}, {params_str}),\n"

    def depart_table(self, node: nodes.table) -> None:
        """
        Depart a table node.

        Args:
            node: The table node
        """
        # Generate Typst table() syntax (no # prefix in unified code mode)
        if self.table_colcount > 0:
            # Use self.body.append directly to avoid routing to table_cell_content
            self.body.append(f"table(\n  columns: {self.table_colcount},\n")

            # Separate header cells from body cells
            header_cells = [cell for cell in self.table_cells if cell.get("is_header")]
            body_cells = [
                cell for cell in self.table_cells if not cell.get("is_header")
            ]

            # Add header cells with table.header() wrapper
            if header_cells:
                self.body.append("  table.header(\n")
                for cell in header_cells:
                    self.body.append(self._format_table_cell(cell, indent="    "))
                self.body.append("  ),\n")

            # Add body cells
            for cell in body_cells:
                self.body.append(self._format_table_cell(cell, indent="  "))

            self.body.append(")\n\n")

        self.in_table = False
        self.table_cells = []
        self.table_colcount = 0

    def visit_tgroup(self, node: nodes.tgroup) -> None:
        """
        Visit a tgroup (table group) node.

        Args:
            node: The tgroup node
        """
        # Get column count from tgroup
        self.table_colcount = node.get("cols", 0)

    def depart_tgroup(self, node: nodes.tgroup) -> None:
        """
        Depart a tgroup (table group) node.

        Args:
            node: The tgroup node
        """
        pass

    def visit_colspec(self, node: nodes.colspec) -> None:
        """
        Visit a colspec (column specification) node.

        Args:
            node: The colspec node
        """
        # Column specifications are handled by tgroup
        raise nodes.SkipNode

    def depart_colspec(self, node: nodes.colspec) -> None:
        """
        Depart a colspec (column specification) node.

        Args:
            node: The colspec node
        """
        pass

    def visit_thead(self, node: nodes.thead) -> None:
        """
        Visit a thead (table header) node.

        Args:
            node: The thead node
        """
        # Mark that we're in the header section
        self.in_thead = True

    def depart_thead(self, node: nodes.thead) -> None:
        """
        Depart a thead (table header) node.

        Args:
            node: The thead node
        """
        # Mark that we're no longer in the header section
        self.in_thead = False

    def visit_tbody(self, node: nodes.tbody) -> None:
        """
        Visit a tbody (table body) node.

        Args:
            node: The tbody node
        """
        pass

    def depart_tbody(self, node: nodes.tbody) -> None:
        """
        Depart a tbody (table body) node.

        Args:
            node: The tbody node
        """
        pass

    def visit_row(self, node: nodes.row) -> None:
        """
        Visit a row (table row) node.

        Args:
            node: The row node
        """
        # Rows are processed by collecting entries
        pass

    def depart_row(self, node: nodes.row) -> None:
        """
        Depart a row (table row) node.

        Args:
            node: The row node
        """
        pass

    def visit_entry(self, node: nodes.entry) -> None:
        """
        Visit an entry (table cell) node.

        Args:
            node: The entry node
        """
        # Start collecting cell content
        self.table_cell_content = []

        # Read cell spanning attributes
        # morecols: number of additional columns (0 = normal cell)
        # morerows: number of additional rows (0 = normal cell)
        self.current_morecols = node.get("morecols", 0)
        self.current_morerows = node.get("morerows", 0)

    def depart_entry(self, node: nodes.entry) -> None:
        """
        Depart an entry (table cell) node.

        Args:
            node: The entry node
        """
        # Get cell content and add to table cells
        # Extract text from the accumulated body content since visit_entry
        cell_text = ""
        if hasattr(self, "table_cell_content") and self.table_cell_content:
            cell_text = "".join(self.table_cell_content).strip()

        if not cell_text:
            # If no content was captured, try to get text from the node
            cell_text = node.astext().strip()

        # Calculate colspan and rowspan from morecols/morerows
        # morecols=1 means 2 columns total (1 + 1 additional)
        colspan = self.current_morecols + 1
        rowspan = self.current_morerows + 1

        # Store cell with header/body distinction and spanning info
        self.table_cells.append(
            {
                "content": cell_text,
                "is_header": self.in_thead,
                "colspan": colspan,
                "rowspan": rowspan,
            }
        )
        self.table_cell_content = []

    def visit_block_quote(self, node: nodes.block_quote) -> None:
        """
        Visit a block quote node.

        Generates quote() function call (no # prefix in code mode).

        Args:
            node: The block quote node
        """
        # Check if there's an attribution child node
        has_attribution = any(isinstance(child, nodes.attribution) for child in node)

        if has_attribution:
            # Will add attribution parameter when we encounter the attribution node
            self.add_text("quote(")
        else:
            self.add_text("quote[")

    def depart_block_quote(self, node: nodes.block_quote) -> None:
        """
        Depart a block quote node.

        Args:
            node: The block quote node
        """
        # Check if there's an attribution child node
        has_attribution = any(isinstance(child, nodes.attribution) for child in node)

        if has_attribution:
            self.add_text(")\n\n")
        else:
            self.add_text("]\n\n")

    def visit_attribution(self, node: nodes.attribution) -> None:
        """
        Visit an attribution node (quote attribution).

        Args:
            node: The attribution node
        """
        # Close the quote content and add attribution parameter
        self.add_text("], attribution: [")

    def depart_attribution(self, node: nodes.attribution) -> None:
        """
        Depart an attribution node.

        Args:
            node: The attribution node
        """
        # Close attribution parameter
        self.add_text("]")

    def visit_image(self, node: nodes.image) -> None:
        """
        Visit an image node.

        Generates image() function call (no # prefix in code mode).
        Adjusts image paths for nested documents (Issue #69).

        Args:
            node: The image node
        """
        uri = node.get("uri", "")

        # Get current document name for path adjustment (Issue #69)
        current_docname = getattr(self.builder, "current_docname", None)

        # Adjust path based on output file location (Issue #69)
        adjusted_uri = self._compute_relative_image_path(uri, current_docname)

        # Add proper indentation if inside a figure
        if self.in_figure:
            self.add_text(f'  image("{adjusted_uri}"')
        else:
            # No # prefix in code mode
            self.add_text(f'image("{adjusted_uri}"')

        # Add optional attributes
        if "width" in node:
            width = node["width"]
            self.add_text(f", width: {width}")

        if "height" in node:
            height = node["height"]
            self.add_text(f", height: {height}")

        self.add_text(")")

    def depart_image(self, node: nodes.image) -> None:
        """
        Depart an image node.

        Args:
            node: The image node
        """
        # If inside a figure, don't add extra newlines (figure will handle spacing)
        if not self.in_figure:
            self.add_text("\n\n")

    def visit_target(self, node: nodes.target) -> None:
        """
        Visit a target node (label definition).

        Args:
            node: The target node
        """
        # Check if we're in a markup mode wrapper started by reference
        if (
            hasattr(self, "_in_reference_with_target")
            and self._in_reference_with_target
        ):
            # Re-enable markup mode for label output (was disabled for link content)
            self._in_markup_mode = True
            # Output label in markup mode (with # prefix in markup mode)
            if node.get("ids"):
                label_id = node["ids"][0]
                self.add_text(f'\n#label("{label_id}")')
            # Close the markup block
            self.add_text("]")
            # Clear the flags
            self._in_reference_with_target = False
            self._in_markup_mode = False  # Exit markup mode
            # Mark separator needed for next element
            if self.in_list_item:
                self.list_item_needs_separator = True
            # Skip processing children as target is typically empty
            raise nodes.SkipNode

        # Original behavior for non-markup-wrapped targets
        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Generate Typst label if target has ids
        # In unified code mode, use label() function instead of <label> syntax
        if node.get("ids"):
            label_id = node["ids"][0]
            self.add_text(f'label("{label_id}")')

        # Mark that next element in list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

        # Skip processing children as target is typically empty
        raise nodes.SkipNode

    def depart_target(self, node: nodes.target) -> None:
        """
        Depart a target node.

        Args:
            node: The target node
        """
        # Target is handled in visit
        pass

    def visit_pending_xref(self, node: nodes.Node) -> None:
        """
        Visit a pending_xref node (Sphinx cross-reference).

        Args:
            node: The pending_xref node
        """
        # pending_xref nodes are typically resolved by Sphinx before reaching the writer
        # If we encounter one, it means resolution failed or we're in a special case
        # We handle it by generating a link to the target

        reftarget = node.get("reftarget", "")
        reftype = node.get("reftype", "")

        if reftarget:
            # Generate a link to the target
            # Sanitize the target for Typst label format
            label = reftarget.replace(".", "-").replace("_", "-")
            self.add_text(f"#link(<{label}>)[")
        # Continue processing children to get the link text

    def depart_pending_xref(self, node: nodes.Node) -> None:
        """
        Depart a pending_xref node.

        Args:
            node: The pending_xref node
        """
        reftarget = node.get("reftarget", "")
        if reftarget:
            self.add_text("]")

    def _compute_relative_include_path(
        self, target_docname: str, current_docname: Optional[str]
    ) -> str:
        """
        Compute relative path for toctree #include() directive.

        This method calculates the relative path from the current document
        to the target document for use in Typst #include() directives.
        Uses PurePosixPath for OS-independent POSIX path handling.

        Args:
            target_docname: Target document name (e.g., "chapter1/section1")
            current_docname: Current document name (e.g., "chapter1/index"), or None

        Returns:
            Relative path string for #include() (e.g., "section1" or "../chapter2/doc")

        Examples:
            >>> _compute_relative_include_path("chapter1/section1", "chapter1/index")
            "section1"
            >>> _compute_relative_include_path("chapter2/doc", "chapter1/index")
            "../chapter2/doc"
            >>> _compute_relative_include_path("chapter1/doc", None)
            "chapter1/doc"

        Notes:
            This method implements Issue #5 fix for nested toctree relative paths.
            It handles three cases:
            1. current_docname is None: return absolute path
            2. Same directory: use relative_to() directly
            3. Cross-directory: calculate via common parent

        Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
        """
        from pathlib import PurePosixPath

        logger.debug(
            f"Computing relative include path: target={target_docname}, "
            f"current={current_docname}"
        )

        # Fallback to absolute path if current_docname is None
        if not current_docname:
            logger.debug(f"No current document, using absolute path: {target_docname}")
            return target_docname

        current_path = PurePosixPath(current_docname)
        target_path = PurePosixPath(target_docname)
        current_dir = current_path.parent

        logger.debug(
            f"Path components: current_dir={current_dir}, " f"target_path={target_path}"
        )

        # Root directory case: use absolute path (backward compatibility)
        if current_dir == PurePosixPath("."):
            logger.debug(
                f"Current document is in root directory, "
                f"using absolute path: {target_docname}"
            )
            return target_docname

        # Try to compute relative path
        try:
            rel_path = target_path.relative_to(current_dir)
            result = str(rel_path)
            logger.debug(
                f"Same directory reference: {current_dir} -> {target_path}, "
                f"result: {result}"
            )
            return result
        except ValueError:
            # Different directory trees - build path via common parent
            logger.debug(
                "Cross-directory reference detected, calculating via common parent"
            )

            current_parts = current_dir.parts
            target_parts = target_path.parts

            # Find common parent by comparing path components
            common_length = 0
            for i, (c, t) in enumerate(zip(current_parts, target_parts)):
                if c == t:
                    common_length = i + 1
                else:
                    break

            logger.debug(
                f"Common parent depth: {common_length}, "
                f"current_parts={current_parts}, target_parts={target_parts}"
            )

            # Build path: "../" from current to common parent
            up_count = len(current_parts) - common_length
            up_path = "../" * up_count if up_count > 0 else ""

            # Build path: from common parent to target
            down_parts = target_parts[common_length:]
            down_path = "/".join(down_parts) if down_parts else ""

            relative_path: str = up_path + down_path

            logger.debug(
                f"Cross-directory path calculation: up_count={up_count}, "
                f"up_path='{up_path}', down_path='{down_path}', "
                f"result: {relative_path}"
            )

            return relative_path

    def _compute_relative_image_path(
        self, image_uri: str, current_docname: Optional[str]
    ) -> str:
        """
        Compute relative path for image() function.

        Adjusts image URIs from source-root-relative to output-file-relative.
        This is similar to _compute_relative_include_path() but for images.

        Args:
            image_uri: Image URI from Sphinx (source-root-relative)
            current_docname: Current document name (e.g., "chapter1/section1")

        Returns:
            Adjusted relative path for Typst image()

        Examples:
            >>> _compute_relative_image_path("images/logo.png", "chapter1/section1")
            "../images/logo.png"
            >>> _compute_relative_image_path("images/logo.png", "index")
            "images/logo.png"
            >>> _compute_relative_image_path("images/logo.png", None)
            "images/logo.png"

        Notes:
            This implements Issue #69 fix for nested document image paths.
            Uses the same logic as _compute_relative_include_path() from Issue #5.
        """
        from pathlib import PurePosixPath

        logger.debug(
            f"Computing relative image path: uri={image_uri}, "
            f"current={current_docname}"
        )

        # Fallback to absolute path if current_docname is None
        if not current_docname:
            logger.debug(f"No current document, using absolute path: {image_uri}")
            return image_uri

        current_path = PurePosixPath(current_docname)
        image_path = PurePosixPath(image_uri)
        current_dir = current_path.parent

        logger.debug(
            f"Path components: current_dir={current_dir}, image_path={image_path}"
        )

        # Root directory case: use absolute path (backward compatibility)
        if current_dir == PurePosixPath("."):
            logger.debug(
                f"Current document is in root directory, "
                f"using absolute path: {image_uri}"
            )
            return image_uri

        # Try to compute relative path
        try:
            rel_path = image_path.relative_to(current_dir)
            result = str(rel_path)
            logger.debug(
                f"Same directory reference: {current_dir} -> {image_path}, "
                f"result: {result}"
            )
            return result
        except ValueError:
            # Different directory trees - build path via common parent
            logger.debug(
                "Cross-directory reference detected, calculating via common parent"
            )

            current_parts = current_dir.parts
            image_parts = image_path.parts

            # Find common parent by comparing path components
            common_length = 0
            for i, (c, img) in enumerate(zip(current_parts, image_parts)):
                if c == img:
                    common_length = i + 1
                else:
                    break

            logger.debug(
                f"Common parent depth: {common_length}, "
                f"current_parts={current_parts}, image_parts={image_parts}"
            )

            # Build path: "../" from current to common parent
            up_count = len(current_parts) - common_length
            up_path = "../" * up_count if up_count > 0 else ""

            # Build path: from common parent to image
            down_parts = image_parts[common_length:]
            down_path = "/".join(down_parts) if down_parts else ""

            relative_path: str = up_path + down_path

            logger.debug(
                f"Cross-directory path calculation: up_count={up_count}, "
                f"up_path='{up_path}', down_path='{down_path}', "
                f"result: {relative_path}"
            )

            return relative_path

    def visit_toctree(self, node: nodes.Node) -> None:
        """
        Visit a toctree node (Sphinx table of contents tree).

        Requirement 13: Multi-document integration and toctree processing
        - Generate #include() for each entry
        - Apply #set heading(offset: 1) to lower heading levels
        - Issue #5: Fix relative paths for nested toctrees
          - Calculate relative paths from current document
        - Issue #7: Simplify toctree output with single content block
          - Generate single #[...] block containing all includes
          - Apply #set heading(offset: 1) once per toctree

        Args:
            node: The toctree node

        Notes:
            This method generates Typst #include() directives for each toctree entry
            within a single content block #[...] to apply heading offset without
            displaying the block delimiters in the output. This simplifies the
            generated Typst code and improves readability.
        """
        # Get entries from the toctree node
        entries = node.get("entries", [])

        logger.debug(f"Processing toctree with {len(entries)} entries")

        # If no entries, don't generate anything
        if not entries:
            logger.debug("Toctree has no entries, skipping")
            raise nodes.SkipNode

        # Get current document name for relative path calculation
        current_docname = getattr(self.builder, "current_docname", None)

        logger.debug(
            f"Current document for toctree: {current_docname}, "
            f"entries: {[docname for _, docname in entries]}"
        )

        # Generate scope block for all includes (unified code mode)
        # Use {...} scope block to isolate set rules while maintaining code mode
        # Start scope block (no # prefix in code mode)
        self.add_text("{\n")
        self.add_text("  set heading(offset: 1)\n")

        # Generate include() for each entry within the scope block
        # Each included file has its own imports, so block scope is safe
        for _title, docname in entries:
            # Compute relative path for include() (Issue #5 fix)
            relative_path = self._compute_relative_include_path(
                docname, current_docname
            )

            logger.debug(
                f"Generated include() for toctree: {docname} -> {relative_path}.typ"
            )

            # Generate include() within the block (no # prefix in code mode)
            self.add_text(f'  include("{relative_path}.typ")\n')

        # End scope block
        self.add_text("}\n\n")

        # Skip processing children as we've handled the toctree entries
        raise nodes.SkipNode

    def depart_toctree(self, node: nodes.Node) -> None:
        """
        Depart a toctree node.

        Args:
            node: The toctree node
        """
        # Toctree is handled in visit
        pass

    def visit_reference(self, node: nodes.reference) -> None:
        """
        Visit a reference node (link).

        Generates link() function call (no # prefix in code mode).

        Args:
            node: The reference node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Check if next sibling is a target node (for label attachment)
        # This is needed in both list items and paragraphs in unified code mode
        next_is_target = False
        if node.parent:
            node_index = node.parent.index(node)
            if node_index + 1 < len(node.parent.children):
                next_node = node.parent.children[node_index + 1]
                if isinstance(next_node, nodes.target):
                    next_is_target = True

        # If next is target, wrap in markup mode for label attachment
        # In unified code mode, labels can only attach in markup mode blocks [...]
        if next_is_target:
            self.add_text("[")
            self._in_reference_with_target = True
            self._in_markup_mode = (
                True  # Enter markup mode - need # prefix for functions
            )

        # Save and reset list item separator for children (they're inside this element)
        was_list_item_needs_separator = self.list_item_needs_separator
        self.list_item_needs_separator = False

        # Get the reference URI
        refuri = node.get("refuri", "")

        # Handle empty URLs (Typst 0.14+ rejects empty URLs)
        # This can occur with unresolved references, broken cross-references,
        # or malformed reStructuredText. Instead of generating invalid link("", ...),
        # we skip the link wrapper and render content as plain text.
        if not refuri:
            logger.warning(
                f"Reference node has empty URL. "
                f"Link will be rendered as plain text. "
                f"Check for broken references in source: {node.astext()}"
            )
            self._skip_link_wrapper = True
            return

        # Determine if we need # prefix (in markup mode)
        prefix = "#" if self._in_markup_mode else ""

        # Check if it's an internal reference (starts with #)
        if refuri.startswith("#"):
            # Internal reference to a label
            label = refuri[1:]  # Remove the #
            self.add_text(f"{prefix}link(<{label}>, ")
        else:
            # External reference (HTTP/HTTPS URL or relative path)
            self.add_text(f'{prefix}link("{refuri}", ')

        # After outputting link(), turn off markup mode for content (second argument)
        # Content inside function arguments is code mode (no # prefix)
        if self._in_markup_mode:
            self._in_markup_mode = False

        # Mark that we're inside link() to use + for concatenation
        self._in_link = True
        self._link_has_content = False

        # Store state to restore in depart
        self._reference_was_list_item_needs_separator = was_list_item_needs_separator

    def depart_reference(self, node: nodes.reference) -> None:
        """
        Depart a reference node.

        Args:
            node: The reference node
        """
        # Skip link wrapper closing if we skipped it in visit
        if getattr(self, "_skip_link_wrapper", False):
            self._skip_link_wrapper = False
            # Restore list item separator state if needed
            if hasattr(self, "_reference_was_list_item_needs_separator"):
                if self.in_list_item:
                    self.list_item_needs_separator = True
                delattr(self, "_reference_was_list_item_needs_separator")
            return

        # Close the link function
        self.add_text(")")

        # Exit link context
        self._in_link = False

        # Restore and mark that next element needs separator
        if hasattr(self, "_reference_was_list_item_needs_separator"):
            if self.in_list_item:
                self.list_item_needs_separator = True
            delattr(self, "_reference_was_list_item_needs_separator")

    def unknown_visit(self, node: nodes.Node) -> None:
        """
        Handle unknown nodes during visit.

        Args:
            node: The unknown node
        """
        # Log a warning for unknown nodes but don't raise an exception
        from sphinx.util import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"unknown node type: {node}")

    def unknown_departure(self, node: nodes.Node) -> None:
        """
        Handle unknown nodes during departure.

        Args:
            node: The unknown node
        """
        # Silently ignore unknown departures
        pass

    def _convert_latex_to_typst(self, latex_content: str) -> str:
        """
        Convert LaTeX math syntax to Typst native syntax.

        Implements Task 6.5: Basic LaTeX to Typst conversion
        Requirement 4.9: Fallback when typst_use_mitex=False

        Args:
            latex_content: LaTeX math content

        Returns:
            Typst native math content
        """
        # Basic conversion rules for common LaTeX commands
        result = latex_content

        # Greek letters: \alpha -> alpha, \beta -> beta, etc.
        greek_letters = [
            "alpha",
            "beta",
            "gamma",
            "delta",
            "epsilon",
            "zeta",
            "eta",
            "theta",
            "iota",
            "kappa",
            "lambda",
            "mu",
            "nu",
            "xi",
            "omicron",
            "pi",
            "rho",
            "sigma",
            "tau",
            "upsilon",
            "phi",
            "chi",
            "psi",
            "omega",
            "Alpha",
            "Beta",
            "Gamma",
            "Delta",
            "Epsilon",
            "Zeta",
            "Eta",
            "Theta",
            "Iota",
            "Kappa",
            "Lambda",
            "Mu",
            "Nu",
            "Xi",
            "Omicron",
            "Pi",
            "Rho",
            "Sigma",
            "Tau",
            "Upsilon",
            "Phi",
            "Chi",
            "Psi",
            "Omega",
        ]
        for letter in greek_letters:
            result = result.replace(f"\\{letter}", letter)

        # Fractions: \frac{a}{b} -> frac(a, b)
        result = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"frac(\1, \2)", result)

        # Sum: \sum_{lower}^{upper} -> sum_(lower)^upper
        result = re.sub(r"\\sum_\{([^}]+)\}\^\{([^}]+)\}", r"sum_(\1)^(\2)", result)
        result = re.sub(r"\\sum_\{([^}]+)\}", r"sum_(\1)", result)
        result = result.replace(r"\sum", "sum")

        # Integral: \int_{lower}^{upper} -> integral_(lower)^upper
        result = re.sub(
            r"\\int_\{([^}]+)\}\^\{([^}]+)\}", r"integral_(\1)^(\2)", result
        )
        result = re.sub(r"\\int_\{([^}]+)\}", r"integral_(\1)", result)
        result = result.replace(r"\int", "integral")

        # Product: \prod -> product
        result = result.replace(r"\prod", "product")

        # Square root: \sqrt{x} -> sqrt(x)
        result = re.sub(r"\\sqrt\{([^}]+)\}", r"sqrt(\1)", result)

        # Infinity: \infty -> infinity
        result = result.replace(r"\infty", "infinity")

        # Partial derivative: \partial -> diff (Typst uses diff or ∂)
        result = result.replace(r"\partial", "diff")

        # Common functions
        result = result.replace(r"\sin", "sin")
        result = result.replace(r"\cos", "cos")
        result = result.replace(r"\tan", "tan")
        result = result.replace(r"\log", "log")
        result = result.replace(r"\ln", "ln")
        result = result.replace(r"\exp", "exp")

        # If there are still backslashes, warn about unconverted syntax
        if "\\" in result:
            logger.warning(
                f"LaTeX math contains commands that may not convert well to Typst: {latex_content}"
            )

        return result

    def visit_math(self, node: nodes.math) -> None:
        """
        Visit an inline math node.

        Implements Task 6.2: LaTeX math conversion (mitex)
        Implements Task 6.3: Labeled equations
        Implements Task 6.4: Typst native math support
        Implements Task 6.5: Math fallback functionality
        Requirement 4.3: Inline math should use #mi(`...`) format (LaTeX)
        Requirement 4.9: Fallback when typst_use_mitex=False
        Requirement 5.2: Inline math should use $...$ format (Typst native)
        Requirement 4.7: Labeled equations should generate <eq:label> format
        Design 3.3: Support both mitex and Typst native math

        Args:
            node: The inline math node
        """
        # Add separator if in paragraph and not first node
        self._add_paragraph_separator()

        # Extract math content
        math_content = node.astext()

        # Task 6.4: Check if this is explicitly marked as Typst native
        is_typst_native = "typst-native" in node.get("classes", [])

        # Task 6.5: Check typst_use_mitex config (default to True)
        use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

        if is_typst_native or not use_mitex:
            # Requirement 5.2: Typst native inline math syntax
            # Task 6.5: Convert LaTeX to Typst if use_mitex=False
            if not is_typst_native and not use_mitex:
                # Convert LaTeX syntax to Typst native
                math_content = self._convert_latex_to_typst(math_content)
            self.add_text(f"${math_content}$")
        else:
            # Requirement 4.3: LaTeX math via mitex (no # prefix in code mode)
            self.add_text(f"mi(`{math_content}`)")

        # Task 6.3: Add label if present
        if "ids" in node and node["ids"]:
            label = node["ids"][0]
            self.add_text(f" <{label}>")

        # Skip children to prevent duplicate output of math content
        raise nodes.SkipNode

    def depart_math(self, node: nodes.math) -> None:
        """
        Depart an inline math node.

        Args:
            node: The inline math node
        """
        # No additional output needed
        pass

    def visit_math_block(self, node: nodes.math_block) -> None:
        """
        Visit a block math node.

        Implements Task 6.2: LaTeX math conversion (mitex)
        Implements Task 6.3: Labeled equations
        Implements Task 6.4: Typst native math support
        Implements Task 6.5: Math fallback functionality
        Requirement 4.2: Block math should use #mitex(`...`) format (LaTeX)
        Requirement 4.9: Fallback when typst_use_mitex=False
        Requirement 5.2: Block math should use $ ... $ format (Typst native)
        Requirement 4.7: Labeled equations should generate <eq:label> format
        Design 3.3: Support both mitex and Typst native math

        Args:
            node: The block math node
        """
        # Extract math content
        math_content = node.astext()

        # Task 6.4: Check if this is explicitly marked as Typst native
        is_typst_native = "typst-native" in node.get("classes", [])

        # Task 6.5: Check typst_use_mitex config (default to True)
        use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

        if is_typst_native or not use_mitex:
            # Requirement 5.2: Typst native block math syntax
            # Task 6.5: Convert LaTeX to Typst if use_mitex=False
            if not is_typst_native and not use_mitex:
                # Convert LaTeX syntax to Typst native
                math_content = self._convert_latex_to_typst(math_content)
            self.add_text(f"$ {math_content} $")
        else:
            # Requirement 4.2: LaTeX math via mitex (no # prefix in code mode)
            self.add_text(f"mitex(`{math_content}`)")

        # Task 6.3: Add label if present
        if "ids" in node and node["ids"]:
            label = node["ids"][0]
            self.add_text(f" <{label}>")

        self.add_text("\n\n")

        # Skip children to prevent duplicate output of math content
        raise nodes.SkipNode

    def depart_math_block(self, node: nodes.math_block) -> None:
        """
        Depart a block math node.

        Args:
            node: The block math node
        """
        # No additional output needed
        pass

    # Admonition nodes (Task 3.4)
    # Requirement 2.8-2.10: Convert Sphinx admonitions to gentle-clues

    def _visit_admonition(
        self, node: nodes.Node, clue_type: str, custom_title: str = None
    ) -> None:
        """
        Helper method to visit any admonition node.

        Args:
            node: The admonition node
            clue_type: The gentle-clues function name (e.g., 'info', 'warning', 'tip')
            custom_title: Optional custom title for the admonition
        """
        # Add newline separator if in list item and not first element
        if self.in_list_item and self.list_item_needs_separator:
            self.add_text("\n")

        # Check if there's a title element in the node
        title = None
        for child in node.children:
            if isinstance(child, nodes.title):
                title = child.astext()
                break

        # Use custom title if provided, otherwise check for title element
        # No # prefix in unified code mode
        if title:
            self.add_text(f'{clue_type}(title: "{title}")[')
        elif custom_title:
            self.add_text(f'{clue_type}(title: "{custom_title}")[')
        else:
            self.add_text(f"{clue_type}[")

    def _depart_admonition(self) -> None:
        """
        Helper method to depart any admonition node.
        """
        self.add_text("]\n\n")

        # Mark that next element in list item needs separator
        if self.in_list_item:
            self.list_item_needs_separator = True

    def visit_note(self, node: nodes.note) -> None:
        """Visit a note admonition (converts to #info[])."""
        self._visit_admonition(node, "info")

    def depart_note(self, node: nodes.note) -> None:
        """Depart a note admonition."""
        self._depart_admonition()

    def visit_warning(self, node: nodes.warning) -> None:
        """Visit a warning admonition (converts to #warning[])."""
        self._visit_admonition(node, "warning")

    def depart_warning(self, node: nodes.warning) -> None:
        """Depart a warning admonition."""
        self._depart_admonition()

    def visit_tip(self, node: nodes.tip) -> None:
        """Visit a tip admonition (converts to #tip[])."""
        self._visit_admonition(node, "tip")

    def depart_tip(self, node: nodes.tip) -> None:
        """Depart a tip admonition."""
        self._depart_admonition()

    def visit_important(self, node: nodes.important) -> None:
        """Visit an important admonition (converts to #warning(title: "Important")[])."""
        self._visit_admonition(node, "warning", custom_title="Important")

    def depart_important(self, node: nodes.important) -> None:
        """Depart an important admonition."""
        self._depart_admonition()

    def visit_caution(self, node: nodes.caution) -> None:
        """Visit a caution admonition (converts to #warning[])."""
        self._visit_admonition(node, "warning")

    def depart_caution(self, node: nodes.caution) -> None:
        """Depart a caution admonition."""
        self._depart_admonition()

    def visit_seealso(self, node: addnodes.seealso) -> None:
        """Visit a seealso admonition (converts to #info(title: "See Also")[])."""
        self._visit_admonition(node, "info", custom_title="See Also")

    def depart_seealso(self, node: addnodes.seealso) -> None:
        """Depart a seealso admonition."""
        self._depart_admonition()

    # Inline nodes (Task 7.4)
    # Requirement 3.1: Inline cross-references and links

    def visit_inline(self, node: nodes.inline) -> None:
        """
        Visit an inline node.

        Inline nodes are generic containers for inline content.
        They are often used for cross-references with specific CSS classes.

        Task 7.4: Handle inline nodes, especially those with 'xref' class
        Requirement 3.1: Cross-references and links
        """
        # Inline nodes are transparent containers - we just process their children
        # The CSS classes (like 'xref', 'doc', 'std-ref') are mainly for HTML/CSS styling
        # For Typst output, we simply render the text content
        pass

    def depart_inline(self, node: nodes.inline) -> None:
        """
        Depart an inline node.
        """
        pass

    # API description nodes (Issue #55)
    # Requirement: API説明ノードの処理

    def visit_index(self, node: addnodes.index) -> None:
        """
        Visit an index node.

        Index entries are skipped in Typst/PDF output as we don't generate indices.
        """
        raise nodes.SkipNode

    def depart_index(self, node: addnodes.index) -> None:
        """Depart an index node."""
        pass

    def visit_desc(self, node: addnodes.desc) -> None:
        """
        Visit a desc node (API description container).

        Desc nodes contain API descriptions (classes, functions, methods, etc.).
        """
        pass

    def depart_desc(self, node: addnodes.desc) -> None:
        """
        Depart a desc node.

        Add spacing after API description blocks.
        """
        self.body.append("\n\n")

    def visit_desc_signature(self, node: addnodes.desc_signature) -> None:
        """
        Visit a desc_signature node (API element signature).

        Signatures are rendered in bold using strong({}) wrapper.
        """
        # Create a dummy strong node and use its visitor logic
        dummy_strong = nodes.strong()
        self.visit_strong(dummy_strong)

    def depart_desc_signature(self, node: addnodes.desc_signature) -> None:
        """Depart a desc_signature node."""
        # Use strong's depart logic
        dummy_strong = nodes.strong()
        self.depart_strong(dummy_strong)
        # Add extra spacing after signature
        self.body.append("\n")

    def visit_desc_content(self, node: addnodes.desc_content) -> None:
        """
        Visit a desc_content node (API description content).
        """
        pass

    def depart_desc_content(self, node: addnodes.desc_content) -> None:
        """Depart a desc_content node."""
        pass

    def visit_desc_annotation(self, node: addnodes.desc_annotation) -> None:
        """
        Visit a desc_annotation node (type annotations like 'class', 'async', etc.).
        """
        pass

    def depart_desc_annotation(self, node: addnodes.desc_annotation) -> None:
        """
        Depart a desc_annotation node.

        Space after annotation is handled by desc_sig_space node.
        """
        # Don't add space here - desc_sig_space handles it
        # Don't set list_item_needs_separator - let next node handle it
        pass

    def visit_desc_addname(self, node: addnodes.desc_addname) -> None:
        """
        Visit a desc_addname node (module name prefix).
        """
        pass

    def depart_desc_addname(self, node: addnodes.desc_addname) -> None:
        """Depart a desc_addname node."""
        pass

    def visit_desc_name(self, node: addnodes.desc_name) -> None:
        """
        Visit a desc_name node (function/class name).
        """
        pass

    def depart_desc_name(self, node: addnodes.desc_name) -> None:
        """Depart a desc_name node."""
        # Mark that next element needs separator (for parameterlist)
        if self.in_list_item:
            self.list_item_needs_separator = True

    def visit_desc_parameterlist(self, node: addnodes.desc_parameterlist) -> None:
        """
        Visit a desc_parameterlist node (parameter list container).

        Parameters are concatenated with + inside text parentheses.
        """
        # Add separator before opening paren
        if self.in_list_item and self.list_item_needs_separator:
            self.body.append("\n")

        # Output opening paren as text with + after it
        self.body.append('text("(") + ')

        # Mark that parameterlist started
        self.in_desc_parameter = True
        self._desc_parameter_has_content = (
            False  # First parameter doesn't need + before it
        )

    def depart_desc_parameterlist(self, node: addnodes.desc_parameterlist) -> None:
        """Depart a desc_parameterlist node."""
        # Output closing paren as text, with + before it
        if self._desc_parameter_has_content:
            self.body.append(" + ")
        self.body.append('text(")")')
        self.in_desc_parameter = False

    def visit_desc_parameter(self, node: addnodes.desc_parameter) -> None:
        """
        Visit a desc_parameter node (individual parameter).
        """
        # No changes needed - already in desc_parameter context from parameterlist
        # Don't reset _desc_parameter_has_content here - it's managed by depart_desc_parameter
        pass

    def depart_desc_parameter(self, node: addnodes.desc_parameter) -> None:
        """
        Depart a desc_parameter node.

        Add comma + space between parameters if not last.
        """
        # Add comma between parameters
        if node.next_node(descend=False, siblings=True):
            self.body.append(' + text(", ")')
            self._desc_parameter_has_content = True

    def visit_field_list(self, node: nodes.field_list) -> None:
        """
        Visit a field_list node (structured fields like Parameters, Returns).
        """
        pass

    def depart_field_list(self, node: nodes.field_list) -> None:
        """
        Depart a field_list node.

        Add spacing after field lists.
        """
        self.body.append("\n")

    def visit_field(self, node: nodes.field) -> None:
        """
        Visit a field node (individual field in a field list).
        """
        pass

    def depart_field(self, node: nodes.field) -> None:
        """Depart a field node."""
        pass

    def visit_field_name(self, node: nodes.field_name) -> None:
        """
        Visit a field_name node (field name like 'Parameters', 'Returns').

        Field names are rendered in bold with a colon (no # prefix in code mode).
        """
        # Temporarily disable paragraph state for children
        was_in_paragraph = self.in_paragraph
        self.in_paragraph = False

        # Use strong() function (no # prefix in code mode)
        self.body.append("strong(")

        # Store state to restore in depart
        self._field_name_was_in_paragraph = was_in_paragraph

    def depart_field_name(self, node: nodes.field_name) -> None:
        """Depart a field_name node."""
        # Close strong() and add colon
        self.body.append(' + text(":"))\n')

        # Restore paragraph state
        if hasattr(self, "_field_name_was_in_paragraph"):
            self.in_paragraph = self._field_name_was_in_paragraph
            delattr(self, "_field_name_was_in_paragraph")

    def visit_field_body(self, node: nodes.field_body) -> None:
        """
        Visit a field_body node (field content).
        """
        pass

    def depart_field_body(self, node: nodes.field_body) -> None:
        """
        Depart a field_body node.

        Add newline after field body.
        """
        self.body.append("\n")

    def visit_rubric(self, node: nodes.rubric) -> None:
        """
        Visit a rubric node (section subheading).

        Rubrics are rendered as subsection headings using strong({}) wrapper.
        """
        # Add newline before rubric
        self.body.append("\n")
        # Create a dummy strong node and use its visitor logic
        dummy_strong = nodes.strong()
        self.visit_strong(dummy_strong)

    def depart_rubric(self, node: nodes.rubric) -> None:
        """Depart a rubric node."""
        # Use strong's depart logic
        dummy_strong = nodes.strong()
        self.depart_strong(dummy_strong)
        # Add extra spacing after rubric
        self.body.append("\n")

    def visit_title_reference(self, node: nodes.title_reference) -> None:
        """
        Visit a title_reference node (reference to a title).

        Title references are rendered in emphasis using emph({}) wrapper.
        """
        # Create a dummy emphasis node and use its visitor logic
        dummy_emph = nodes.emphasis()
        self.visit_emphasis(dummy_emph)

    def depart_title_reference(self, node: nodes.title_reference) -> None:
        """Depart a title_reference node."""
        # Use emphasis's depart logic
        dummy_emph = nodes.emphasis()
        self.depart_emphasis(dummy_emph)

    # Additional signature nodes (desc_sig_* family)

    def visit_desc_sig_keyword(self, node: addnodes.desc_sig_keyword) -> None:
        """Visit a desc_sig_keyword node (keywords in signatures like 'class', 'def')."""
        pass

    def depart_desc_sig_keyword(self, node: addnodes.desc_sig_keyword) -> None:
        """Depart a desc_sig_keyword node."""
        pass

    def visit_desc_sig_space(self, node: addnodes.desc_sig_space) -> None:
        """Visit a desc_sig_space node (whitespace in signatures)."""
        # Output space directly, not as separate text() node
        self.body.append(" ")
        # Don't set list_item_needs_separator - space is connector
        raise nodes.SkipNode

    def depart_desc_sig_space(self, node: addnodes.desc_sig_space) -> None:
        """Depart a desc_sig_space node."""
        # Handled in visit
        pass

    def visit_desc_sig_name(self, node: addnodes.desc_sig_name) -> None:
        """Visit a desc_sig_name node (names in signatures)."""
        pass

    def depart_desc_sig_name(self, node: addnodes.desc_sig_name) -> None:
        """Depart a desc_sig_name node."""
        pass

    def visit_desc_sig_punctuation(self, node: addnodes.desc_sig_punctuation) -> None:
        """Visit a desc_sig_punctuation node (punctuation in signatures like ':', '=')."""
        pass

    def depart_desc_sig_punctuation(self, node: addnodes.desc_sig_punctuation) -> None:
        """Depart a desc_sig_punctuation node."""
        pass

    def visit_desc_sig_operator(self, node: addnodes.desc_sig_operator) -> None:
        """Visit a desc_sig_operator node (operators in signatures)."""
        pass

    def depart_desc_sig_operator(self, node: addnodes.desc_sig_operator) -> None:
        """Depart a desc_sig_operator node."""
        pass

    # Literal nodes for API documentation

    def visit_literal_strong(self, node: nodes.inline) -> None:
        """Visit a literal_strong node (bold literal text in field lists)."""
        # Create a dummy strong node and use its visitor logic
        dummy_strong = nodes.strong()
        self.visit_strong(dummy_strong)

    def depart_literal_strong(self, node: nodes.inline) -> None:
        """Depart a literal_strong node."""
        # Use strong's depart logic
        dummy_strong = nodes.strong()
        self.depart_strong(dummy_strong)

    def visit_literal_emphasis(self, node: nodes.inline) -> None:
        """Visit a literal_emphasis node (emphasized literal text in field lists)."""
        # Create a dummy emphasis node and use its visitor logic
        dummy_emph = nodes.emphasis()
        self.visit_emphasis(dummy_emph)

    def depart_literal_emphasis(self, node: nodes.inline) -> None:
        """Depart a literal_emphasis node."""
        # Use emphasis's depart logic
        dummy_emph = nodes.emphasis()
        self.depart_emphasis(dummy_emph)
