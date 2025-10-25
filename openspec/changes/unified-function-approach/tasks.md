# Implementation Tasks: Unified Function Approach

This document outlines all tasks required to implement the unified code mode architecture (`#{...}`) for sphinx-typst.

---

## Phase 0: Document Wrapper & Import Zone

Foundation phase - establishes the code mode structure.

### 0.1 Import Zone (Builder)

- [ ] Verify builder generates import zone BEFORE translator runs
- [ ] Ensure `#import` statements stay at top level (outside `#{...}`)
- [ ] Ensure `#show: project.with(...)` stays at top level
- [ ] Test that import zone is generated correctly
- [ ] Verify no changes needed (current implementation correct)

**Estimated effort**: 1 hour (verification only)

### 0.2 Document Wrapper (Translator)

- [ ] Update `visit_document()` to generate `#{\n`
- [ ] Update `depart_document()` to generate `}\n`
- [ ] Test document wrapper with simple content
- [ ] Verify code block starts after import zone
- [ ] Update test fixtures with `#{...}` wrapper

**Estimated effort**: 2 hours

---

## Phase 1: Text Node Wrapping

Critical phase - all text must use `text()` function to avoid markup escaping.

### 1.1 Text Node Function

- [ ] Update `visit_Text()` to generate `text("...")`
- [ ] Implement string escaping: `\\`, `\"`, `\n`, `\r`, `\t`, `\u{...}`
- [ ] Handle escaping order (backslash first, then others)
- [ ] Handle empty text nodes
- [ ] Handle whitespace-only text nodes

**Estimated effort**: 3 hours

### 1.2 Text Concatenation

- [ ] Implement `+` operator for adjacent text and formatting nodes
- [ ] Test concatenation: `text("A ") + emph(text("B")) + text(" C")`
- [ ] Handle edge cases (start/end of paragraph)
- [ ] Update test fixtures with concatenation

**Estimated effort**: 2 hours

---

## Phase 2: Paragraph Wrapping

Paragraphs must use `par()` function to mark boundaries in code mode.

### 2.1 Paragraph Function

- [ ] Update `visit_paragraph()` to generate `par(`
- [ ] Update `depart_paragraph()` to generate `)\n`
- [ ] Test single paragraph with text only
- [ ] Test paragraph with inline formatting (emph, strong)
- [ ] Test multiple consecutive paragraphs

**Estimated effort**: 2 hours

### 2.2 Paragraph Content Collection

- [ ] Ensure all inline content stays within single `par()` call
- [ ] Test complex paragraphs (text + emph + strong + code + math)
- [ ] Update test fixtures for paragraph wrapping

**Estimated effort**: 2 hours

---

## Phase 3: Inline Formatting (Remove # Prefix)

Convert inline formatting to use bare function names with `text()` content.

### 3.1 Emphasis Conversion

- [ ] Update `visit_emphasis()` to generate `emph(` (no `#`)
- [ ] Update `depart_emphasis()` to generate `)`
- [ ] Ensure content uses `text()` function
- [ ] Test nested emphasis (italic inside italic)
- [ ] Update test fixtures

**Estimated effort**: 2 hours

### 3.2 Strong Conversion

- [ ] Update `visit_strong()` to generate `strong(` (no `#`)
- [ ] Update `depart_strong()` to generate `)`
- [ ] Ensure content uses `text()` function
- [ ] Test underscores in strong text (`file_name.txt`)
- [ ] Test nested strong + emphasis
- [ ] Update test fixtures

**Estimated effort**: 2 hours

### 3.3 Subtitle Conversion

- [ ] Update `visit_subtitle()` to generate `emph(` (no `#`)
- [ ] Update `depart_subtitle()` to generate `)`
- [ ] Ensure content uses `text()` function
- [ ] Test subtitle with special characters
- [ ] Update test fixtures

**Estimated effort**: 1 hour

### 3.4 Field Name Conversion

- [ ] Update `visit_field_name()` to generate `strong(` (no `#`)
- [ ] Update `depart_field_name()` to generate `)`
- [ ] Ensure content uses `text()` function
- [ ] Test API documentation field names
- [ ] Update test fixtures

**Estimated effort**: 1 hour

---

## Phase 4: Heading Conversion

Headings use `heading(level: N, text("..."))` with no `#` prefix.

### 4.1 Heading Function

- [ ] Update `visit_title()` to generate `heading(level: N, ` (no `#`)
- [ ] Calculate level using `self.section_level`
- [ ] Ensure heading text uses `text()` function
- [ ] Update `depart_title()` to generate `)`
- [ ] Handle levels 1-6
- [ ] Handle deep nesting (level > 6)

**Estimated effort**: 3 hours

### 4.2 Heading Tests

- [ ] Test all 6 heading levels
- [ ] Test deeply nested sections
- [ ] Test heading with special characters
- [ ] Update integration tests
- [ ] Update test fixtures

**Estimated effort**: 2 hours

---

## Phase 5: Code Blocks (Backtick Raw Strings)

Inline code and code blocks use `raw()` with backtick raw string literals.

### 5.1 Inline Code Conversion

- [ ] Update `visit_literal()` to generate `raw(\`...\`)` (no `#`, no escaping)
- [ ] Implement backtick delimiter detection (`_count_max_consecutive_backticks`)
- [ ] Use minimum 3 backticks when code contains backticks
- [ ] Test inline code with quotes, backslashes
- [ ] Test inline code with backticks
- [ ] Update test fixtures

**Estimated effort**: 3 hours

### 5.2 Code Block Conversion

- [ ] Update `visit_literal_block()` to use `raw(block: true, lang: "...", \`...\`)` (no `#`)
- [ ] Remove `#` prefix from `codly()` and `codly-range()` calls
- [ ] Implement multi-line backtick raw strings
- [ ] Test code blocks with various content (quotes, backslashes, backticks)
- [ ] Test codly integration (line numbers, highlighting)
- [ ] Update test fixtures

**Estimated effort**: 4 hours

---

## Phase 6: Math Functions

Math uses `mi()` for inline and `mitex()` for block, both with backtick raw strings.

### 6.1 Inline Math Conversion

- [ ] Update `visit_math()` to generate `mi(\`...\`)` (no `#`, backtick raw string)
- [ ] Test LaTeX math with backslashes (`\frac{a}{b}`)
- [ ] Verify mitex integration
- [ ] Update test fixtures

**Estimated effort**: 1 hour

### 6.2 Block Math Conversion

- [ ] Update `visit_math_block()` to generate `mitex(\`...\`)` (no `#`, backtick raw string)
- [ ] Test LaTeX block math with multiple lines
- [ ] Verify mitex integration
- [ ] Update test fixtures

**Estimated effort**: 1 hour

---

## Phase 7: List Conversion (State Redesign)

Lists require collecting all items before generating function calls.

### 7.1 List State Infrastructure

- [ ] Add `list_items_stack` to `__init__`
- [ ] Design item collection mechanism
- [ ] Handle nested list state (stack-based)
- [ ] Design flush mechanism

**Estimated effort**: 3 hours

### 7.2 Bullet List Conversion

- [ ] Update `visit_bullet_list()` to initialize collection
- [ ] Update `depart_bullet_list()` to generate `list(text("..."), ...)` (no `#`)
- [ ] Update `visit_list_item()` to collect content
- [ ] Ensure list items use `text()` for content
- [ ] Test simple bullet lists
- [ ] Test nested bullet lists
- [ ] Update test fixtures

**Estimated effort**: 4 hours

### 7.3 Enumerated List Conversion

- [ ] Update `visit_enumerated_list()` to initialize collection
- [ ] Update `depart_enumerated_list()` to generate `enum(text("..."), ...)` (no `#`)
- [ ] Handle enumeration parameters if needed
- [ ] Ensure list items use `text()` for content
- [ ] Test simple enum lists
- [ ] Test nested enum lists
- [ ] Update test fixtures

**Estimated effort**: 4 hours

### 7.4 Mixed & Complex Lists

- [ ] Test bullet list with nested enum list
- [ ] Test enum list with nested bullet list
- [ ] Test 3-level nesting
- [ ] Test list items with complex content (paragraphs, code)
- [ ] Update comprehensive test fixtures

**Estimated effort**: 3 hours

---

## Phase 8: Definition Lists

Definition lists use `terms()` and `terms.item()` functions.

### 8.1 Definition List Conversion

- [ ] Update `visit_definition_list()` to collect term-definition pairs
- [ ] Generate `terms(terms.item(text("term"), text("def")), ...)` (no `#`)
- [ ] Ensure terms and definitions use `text()`
- [ ] Handle complex definition content (emphasis, strong)
- [ ] Test simple definition lists
- [ ] Test nested content in definitions
- [ ] Update test fixtures

**Estimated effort**: 4 hours

---

## Phase 9: Toctree (Scope Block)

Toctree uses `{...}` scope block for `set` rule isolation.

### 9.1 Toctree Scope Block

- [ ] Update `visit_toctree()` to generate `{\n` (no `#[`)
- [ ] Update to generate `set heading(offset: 1)\n` (no `#`)
- [ ] Update to generate `include("...")\n` (no `#`)
- [ ] Update `depart_toctree()` to generate `}\n` (no `]`)
- [ ] Test scope isolation (offset doesn't leak)
- [ ] Test multiple includes
- [ ] Test relative path calculation
- [ ] Update test fixtures

**Estimated effort**: 3 hours

---

## Phase 10: Existing Function Calls

Update all existing function calls to remove `#` prefix and use `text()`.

### 10.1 Subscript/Superscript

- [ ] Update `visit_subscript()` to generate `sub(` (no `#`)
- [ ] Update `visit_superscript()` to generate `super(` (no `#`)
- [ ] Ensure content uses `text()` function
- [ ] Update test fixtures

**Estimated effort**: 1 hour

### 10.2 Block Quote

- [ ] Update `visit_block_quote()` to generate `quote(` (no `#`)
- [ ] Update `depart_block_quote()` to generate `)`
- [ ] Test quote with complex content
- [ ] Update test fixtures

**Estimated effort**: 1 hour

### 10.3 Images & Figures

- [ ] Update `visit_image()` to generate `image(...)` (no `#`)
- [ ] Update `visit_figure()` to generate `figure(...)` (no `#`)
- [ ] Test image paths and captions
- [ ] Update test fixtures

**Estimated effort**: 2 hours

### 10.4 Tables

- [ ] Update `visit_table()` to generate `table(...)` (no `#`)
- [ ] Ensure table content uses proper formatting
- [ ] Test complex tables
- [ ] Update test fixtures

**Estimated effort**: 2 hours

### 10.5 Links

- [ ] Update `visit_reference()` to generate `link(...)` (no `#`)
- [ ] Ensure link text uses `text()` function
- [ ] Test internal and external links
- [ ] Update test fixtures

**Estimated effort**: 1 hour

### 10.6 Admonitions

- [ ] Update all admonition visitors to remove `#` prefix
- [ ] `info()`, `warning()`, `tip()`, `note()`, etc.
- [ ] Ensure admonition content uses proper formatting
- [ ] Test all admonition types
- [ ] Update test fixtures

**Estimated effort**: 2 hours

---

## Phase 11: Integration & Testing

### 11.1 Test Fixture Updates

- [ ] Update all `.typ` test fixtures to use code mode syntax
- [ ] Verify all fixtures compile with Typst
- [ ] Compare PDF output (must be identical)
- [ ] Update fixture README

**Estimated effort**: 6 hours

### 11.2 Unit Test Updates

- [ ] Update `test_translator.py` for all changes
- [ ] Add tests for `text()` function and escaping
- [ ] Add tests for `par()` function
- [ ] Add tests for backtick raw strings
- [ ] Add tests for scope blocks
- [ ] Ensure 95%+ code coverage

**Estimated effort**: 8 hours

### 11.3 Integration Tests

- [ ] Test complete documents with all element types
- [ ] Test deeply nested structures
- [ ] Test API documentation
- [ ] Test multi-document projects with toctree
- [ ] Test with real-world Sphinx projects

**Estimated effort**: 6 hours

---

## Phase 12: Code Quality & Documentation

### 12.1 Code Quality

- [ ] Run `uv run black .` to format code
- [ ] Run `uv run ruff check .` to check linting
- [ ] Run `uv run mypy typsphinx/` to check types
- [ ] Fix all type errors and linting issues
- [ ] Run `uv run tox` for full test matrix

**Estimated effort**: 4 hours

### 12.2 Code Documentation

- [ ] Update all docstrings for modified methods
- [ ] Add inline comments for complex logic
- [ ] Update module-level documentation
- [ ] Document architectural decisions

**Estimated effort**: 3 hours

### 12.3 User Documentation

- [ ] Update `README.md` with breaking change notice
- [ ] Update `CHANGELOG.md` with detailed changes
- [ ] Write migration guide for users
- [ ] Update example outputs
- [ ] Document new code mode architecture

**Estimated effort**: 4 hours

---

## Phase 13: Validation & Release

### 13.1 OpenSpec Validation

- [ ] Run `openspec validate unified-function-approach --strict`
- [ ] Fix any validation errors
- [ ] Ensure all requirements are testable
- [ ] Verify all scenarios have tests

**Estimated effort**: 2 hours

### 13.2 PDF Verification

- [ ] Generate PDFs from old syntax
- [ ] Generate PDFs from new syntax
- [ ] Visual comparison (must be identical)
- [ ] Test with large documents (>100 pages)
- [ ] Verify compilation performance

**Estimated effort**: 4 hours

### 13.3 Version Bump & Release

- [ ] Decide version number (v0.3.0 or v1.0.0)
- [ ] Update `pyproject.toml` version
- [ ] Update version references in docs
- [ ] Write comprehensive changelog
- [ ] Write release notes
- [ ] Code review and approval

**Estimated effort**: 3 hours

---

## Task Dependencies

```
Phase 0 (Document Wrapper)
  ↓
Phase 1 (Text Nodes) + Phase 2 (Paragraphs)
  ↓
Phase 3 (Inline Formatting) + Phase 4 (Headings)
  ↓
Phase 5 (Code) + Phase 6 (Math) + Phase 7 (Lists) + Phase 8 (Definition Lists) + Phase 9 (Toctree)
  ↓
Phase 10 (Existing Functions)
  ↓
Phase 11 (Integration & Testing)
  ↓
Phase 12 (Code Quality & Docs) + Phase 13 (Validation & Release)
```

---

## Estimated Effort Summary

| Phase | Description | Hours |
|-------|-------------|-------|
| 0 | Document Wrapper & Import Zone | 3 |
| 1 | Text Node Wrapping | 5 |
| 2 | Paragraph Wrapping | 4 |
| 3 | Inline Formatting | 8 |
| 4 | Heading Conversion | 5 |
| 5 | Code Blocks | 7 |
| 6 | Math Functions | 2 |
| 7 | List Conversion | 14 |
| 8 | Definition Lists | 4 |
| 9 | Toctree | 3 |
| 10 | Existing Functions | 9 |
| 11 | Integration & Testing | 20 |
| 12 | Code Quality & Docs | 11 |
| 13 | Validation & Release | 9 |
| **Total** | | **104 hours** |

**Approximately 13 working days (8 hours/day)**

---

## Success Criteria

1. ✅ Document wrapped in `#{...}` code block
2. ✅ Import zone stays outside code block
3. ✅ All function calls use bare names (no `#` prefix)
4. ✅ All text uses `text()` function with proper escaping
5. ✅ All paragraphs wrapped in `par()` function
6. ✅ Code uses backtick raw string literals (no escaping)
7. ✅ Math uses backtick raw strings
8. ✅ Toctree uses `{...}` scope block (no `#` prefix)
9. ✅ All tests passing (pytest, mypy, black, ruff, tox)
10. ✅ PDF output identical to previous version
11. ✅ No syntax errors in generated `.typ` files
12. ✅ OpenSpec validation passing
13. ✅ Documentation updated with migration guide
14. ✅ Code review approved
15. ✅ Ready for major version release

---

## Key Changes from Original Tasks

1. **Added Phase 0**: Import zone handling (critical!)
2. **Added Phase 1**: Text node wrapping with `text()` (critical!)
3. **Added Phase 2**: Paragraph wrapping with `par()` (new requirement)
4. **Updated Phase 5**: Code blocks use backtick raw strings (not string escaping)
5. **Updated Phase 6**: Math functions use backtick raw strings
6. **Updated Phase 9**: Toctree uses `{...}` scope block (not `#[...]` content block)
7. **Updated all phases**: Remove `#` prefix consistently
8. **Increased estimate**: 38 hours → 104 hours (more accurate, includes text/paragraph wrapping)
