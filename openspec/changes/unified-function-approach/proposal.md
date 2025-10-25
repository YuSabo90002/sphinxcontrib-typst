# Proposal: Unified Function Approach for All Typst Elements

## Status
- **State**: Proposed
- **Related Issue**: #4
- **Breaking Change**: Yes (Major version bump required)
- **Created**: 2025-10-25

## Summary

This proposal establishes a **unified code mode architecture** for all Typst element generation in sphinx-typst. We will wrap the entire document in a single code mode block (`#{...}`) and use function calls without `#` prefixes inside, eliminating all sugar syntax (`=`, `*`, `_`, `-`, `+`).

This is an **architectural principle**, not just a set of individual conversions. The goal is to achieve **maximum rigor and complete consistency** across the entire translator implementation.

### Key Design Decision: Document-Level Code Mode

**Entire document wrapped in `#{...}`** with function calls inside (no `#` prefix needed).

**Critical: All plain text MUST use `text()` function** to avoid markup mode escaping issues.

**Example Output**:
```typst
#{
heading(level: 1, text("Introduction"))

par(text("This is ") + emph(text("emphasized")) + text(" and ") + strong(text("strong")) + text(" text."))

list(
  text("First item"),
  text("Second item"),
)
}
```

**Why `text()` function?**
- `[...]` uses markup mode → special characters (`#`, `*`, `_`, `$`, `[`, `]`) need escaping
- `text("...")` uses string mode → no escaping needed for special characters, all characters literal
- Example: `text("Price: $100 #1")` works correctly, `[Price: $100 #1]` breaks
- **Escape sequences** (standard string escaping):
  - `\\` for backslash
  - `\"` for quote
  - `\n` for newline
  - `\r` for carriage return
  - `\t` for tab
  - `\u{...}` for Unicode escape sequence

This approach matches the existing toctree implementation pattern at [translator.py:1230](https://github.com/YuSabo90002/typsphinx/blob/main/typsphinx/translator.py#L1230).

## Problem Statement

### Current State: Inconsistent Syntax Mixing

The current implementation mixes three different approaches:

1. **Sugar Syntax** (shorthand notation):
   - Headings: `= Heading`, `== Heading`
   - Emphasis: `_text_`
   - Strong: `*text*`
   - Bullet lists: `- item`
   - Enum lists: `+ item`
   - Field names in API docs: `*Parameters:*`

2. **Function Syntax** (explicit function calls):
   - Subscript: `#sub[text]`
   - Superscript: `#super[text]`
   - Block quotes: `#quote[...]`
   - Images: `#image("path")`
   - Tables: `#table(...)`
   - Admonitions: `#info[...]`, `#warning[...]`

3. **Typst Standard Syntax** (appropriate to keep):
   - Inline code: `` `code` ``
   - Code blocks: ` ```lang ... ``` `
   - Definition lists: `/ term: definition`
   - Math (native): `$ ... $`

### Core Issues

1. **Maintainability Crisis**
   - Mixed syntax makes code structure unclear
   - Difficult to understand which approach to use for new elements
   - Inconsistent patterns across the 70+ `visit_*` methods

2. **Syntax Error Risks** (Issue #55)
   - Combinations like `*_templates/custom_ieee.typ*:` cause "unclosed delimiter" errors
   - Sugar syntax nesting is fragile and error-prone
   - Hard to debug when syntax combinations fail

3. **No 1:1 Mapping**
   - `visit_emphasis` adds `_` in two places (open/close)
   - Not clear that this generates a specific Typst function
   - Violates visitor pattern clarity

4. **Architectural Inconsistency**
   - Some elements (sub, super, quote) already use functions
   - No clear principle governing when to use sugar vs functions
   - Creates confusion for contributors and maintainers

## Proposed Solution

### Architectural Principle

**Entire document MUST be wrapped in a single code mode block (`#{...}`) with NO `#` prefixes inside.**

Inside the code mode block:
1. ALL function calls use bare function names (e.g., `heading()`, `emph()`, `strong()`)
2. **Text nodes MUST use `text()` function** (NOT `[...]` markup mode)
3. **Paragraphs MUST use `par()` function** to explicitly mark paragraph boundaries
4. Sugar syntax is NOT used (no `=`, `_`, `*`, `-`, `+`)

**Why `text()` instead of `[...]`?**
- `[...]` = markup mode → requires escaping `#`, `*`, `_`, `$`, `[`, `]`
- `text("...")` = string mode → no escaping for special characters, all characters literal
- **Escape sequences** (standard string escaping):
  - `\\` for backslash
  - `\"` for quote
  - `\n` for newline
  - `\r` for carriage return
  - `\t` for tab
  - `\u{...}` for Unicode escape sequence (e.g., `\u{1f600}` for 😀)

**Why `par()` function?**
- Code mode doesn't automatically recognize paragraph breaks from blank lines
- `par()` explicitly marks paragraph boundaries
- Without `par()`, multiple text blocks merge into a single paragraph

### Document Structure

```typst
#{
  // All content here uses function calls without # prefix
  // All text uses text() function to avoid markup escaping
  // All paragraphs use par() function to mark boundaries
  heading(level: 1, text("Title"))

  par(text("Plain text content in first paragraph."))

  par(text("Second paragraph with ") + emph(text("emphasized")) + text(" text."))
}
```

### Elements to Convert

#### 1. Document Wrapper (NEW)
**Current**: No wrapper, direct output to file
**Target**: `#{` at document start, `}` at document end
**Location**: `translator.py:81-99` (`visit_document`, `depart_document`)
**Critical**: This enables all other conversions

#### 2. Headings (6 levels)
**Current**: `= Heading`, `== Heading`, `=== Heading`, etc.
**Target**: `heading(level: 1, text("Heading"))` (NO `#` prefix, use `text()`)
**Location**: `translator.py:132` (`visit_title`)

#### 3. Emphasis
**Current**: `_text_`
**Target**: `emph(text("text"))` (NO `#` prefix, use `text()`)
**Location**: `translator.py:336` (`visit_emphasis`)

#### 4. Strong
**Current**: `*text*`
**Target**: `strong(text("text"))` (NO `#` prefix, use `text()`)
**Location**: `translator.py:355` (`visit_strong`)

#### 5. Subtitle
**Current**: `_subtitle_`
**Target**: `emph(text("subtitle"))` (NO `#` prefix, use `text()`)
**Location**: `translator.py:152` (`visit_subtitle`)

#### 6. Bullet Lists
**Current**: `- item`
**Target**: `list(text("item1"), text("item2"), ...)` (NO `#` prefix, use `text()`)
**Location**: `translator.py:473` (`visit_list_item`)
**Note**: Requires redesign to collect all items before generating `list()`

#### 7. Enumerated Lists
**Current**: `+ item`
**Target**: `enum(text("item1"), text("item2"), ...)` (NO `#` prefix, use `text()`)
**Location**: `translator.py:475` (`visit_list_item`)
**Note**: Requires redesign to collect all items before generating `enum()`

#### 8. Field Names (API Documentation)
**Current**: `*Parameters:*`
**Target**: `strong(text("Parameters:"))` (NO `#` prefix, use `text()`)
**Location**: `translator.py:1790` (`visit_field_name`)

#### 9. Text Nodes (NEW - CRITICAL)
**Current**: Direct text output
**Target**: `text("content")` (wrapped in `text()` function)
**Location**: `translator.py:308` (`visit_Text`)
**Rationale**: `text()` uses string mode → no escaping needed for `#`, `*`, `_`, `$`, `[`, `]`
**Note**: For adjacent text + formatting, use `+` operator: `text("This is ") + emph(text("emphasized"))`

#### 10. Paragraphs (NEW - CRITICAL)
**Current**: Blank lines separate paragraphs (markup mode behavior)
**Target**: `par(...)` function wrapping paragraph content
**Location**: `translator.py:320` (`visit_paragraph`, `depart_paragraph`)
**Rationale**: Code mode doesn't auto-recognize paragraph breaks; `par()` explicitly marks boundaries
**Note**: Each paragraph's content (text + inline elements) should be wrapped in a single `par()` call

#### 11. Inline Code (NEW)
**Current**: `` `code` ``
**Target**: ``raw(`code`)`` (NO `#` prefix, backtick raw string literal)
**Location**: `translator.py:374` (`visit_literal`)
**Rationale**: Codly compatible, consistent with function approach, no escaping needed

#### 12. Code Blocks (NEW)
**Current**: ` ```lang ... ``` ` with `#codly()`, `#codly-range()` calls
**Target**: ``raw(block: true, lang: "...", `code`)`` with `codly()`, `codly-range()` calls (NO `#` prefix, backtick raw string literal)
**Location**: `translator.py:536` (`visit_literal_block`)
**Rationale**: Codly uses `show raw.where(block: true)` and `raw.line` internally
**Note**: Preserve existing codly features (line numbers, highlighting, captions)

#### 13. Definition Lists (NEW)
**Current**: `/ term: definition`
**Target**: `terms.item(text("term"), text("definition"))` (NO `#` prefix)
**Location**: `translator.py:616` (`visit_term`, `visit_definition`)
**Rationale**: Typst has `terms.item()` function for programmatic term list creation
**Note**: Requires collecting term-definition pairs before generating `terms()`

#### 14. Toctree Include (MODIFIED)
**Current**:
```typst
#[
  #set heading(offset: 1)
  #include("path/to/doc.typ")
]
```
**Target**:
```typst
// Within document-level #{...}
#[
  #set heading(offset: 1)
  #include("path/to/doc.typ")
]
```
**Location**: `translator.py:1230-1249` (`visit_toctree`)
**Note**:
- **Keep nested `#[...]` content block** for scoping `set` rules
- **Keep `#` prefix** on `set` and `include()` (required in content blocks)
- Content block creates isolated scope for heading offset
- Without content block, `set` would affect all subsequent headings in document

#### 15. Existing Function Calls (MODIFIED)
**Current**: `#sub[text]`, `#super[text]`, `#quote[...]`, `#image()`, etc.
**Target**: Remove `#` prefix + use `text()` → `sub(text("text"))`, `super(text("text"))`, `quote(...)`, `image()`, etc.
**Location**: Multiple locations (subscript:393, superscript:412, block_quote:944, image:997, etc.)
**Note**: Update ALL existing function calls to:
1. Remove `#` prefix
2. Use `text()` for text content (where applicable)

### Elements to Convert to Functions or Keep

1. **Inline Code**: `` `code` `` → Convert to ``raw(`code`)`` (backtick raw string literal, codly compatible)
2. **Code Blocks**: ` ```lang ... ``` ` → Convert to ``raw(block: true, lang: "...", `code`)`` (backtick raw string literal, codly uses `raw.line`)
3. **Definition Lists**: `/ term: definition` → Convert to `terms.item(term, description)` (function syntax exists!)
4. **Inline Math (mitex)**: `` #mi(`LaTeX`) `` → Convert to `` mi(`LaTeX`) `` (remove `#` prefix, keep backticks for raw string)
5. **Block Math (mitex)**: `` #mitex(`LaTeX`) `` → Convert to `` mitex(`LaTeX`) `` (remove `#` prefix, keep backticks for raw string)
6. **Math (Typst native)**: `$ typst $` → Keep as-is (Typst standard, works in code mode)

**Rationale for `raw()` with backtick raw string literals**:
- **Codly compatibility**: codly uses `show raw.where(block: true)` and `raw.line` internally
- **No escaping needed**: Backticks preserve content literally (quotes, backslashes, special chars)
- **Consistency**: All elements use function syntax inside code mode
- **Feature preservation**: codly's line numbers, highlighting with `codly()`, `codly-range()` still work
- **Explicit control**: Can pass parameters like `lang`, `block`, `align`, etc.
- **Lexer verification**: Typst's lexer handles backticks as raw string literals (no escape processing)

**Backtick raw strings in `raw()`, `mi()`, and `mitex()`**:
- **All three use backticks**: No escaping needed for `\`, `"`, or other special characters
- **Typst lexer**: Backticks are processed as raw string literals at lexer level
- **No escape sequences**: Content between backticks is preserved literally
- **For code with backticks**: Use 3+ backticks as delimiters (minimum 3, not 2)

**Example**:
```typst
#{
  // Code blocks (backtick raw string - no escaping)
  raw(block: true, lang: "python", `def hello():
    print("world")`)

  // Inline code (backtick raw string - no escaping)
  raw(`print("Hello")`)

  // Code with backticks (use 3+ backtick delimiters)
  raw(```code with `backtick` inside```)

  // Inline math (mitex with LaTeX - backticks for raw string literal)
  mi(`\frac{a}{b}`)  // No escaping backslashes

  // Block math (mitex with LaTeX - backticks for raw string literal)
  mitex(`\int_0^1 f(x) dx`)  // No escaping backslashes

  // Math (Typst native - both inline and block)
  $x + y$  // Works in code mode
}
```

## Impact Analysis

### Breaking Changes

⚠️ **Generated `.typ` files will change significantly**

1. **All documents must be rebuilt**
   - Existing `.typ` files use sugar syntax
   - New `.typ` files will use function syntax
   - Version control diffs will be large

2. **PDF output remains identical**
   - Typst compiler produces same PDF from both syntaxes
   - No visual changes for end users
   - This is a **source-level breaking change** only

3. **Version Bump Required**
   - Major version: v0.3.0 or v1.0.0
   - Cannot be a minor or patch release

### Benefits

1. **Maximum Rigor and Consistency**
   - Entire document in unified code mode structure
   - Single clear principle: wrap in `#[...]`, use functions without `#`
   - Matches existing toctree implementation pattern
   - Easy to understand and maintain

2. **Eliminated Syntax Errors**
   - No more `*_text_*` unclosed delimiter errors
   - Function syntax is robust to nesting
   - Predictable behavior
   - No `#` prefix ambiguity

3. **Clear 1:1 Mapping**
   - `visit_emphasis` → `emph(text("..."))` (clear relationship, no `#` needed)
   - `visit_strong` → `strong(text("..."))` (clear relationship, no `#` needed)
   - Visitor pattern becomes self-documenting

4. **Simpler Implementation**
   - No `#` prefix management in visit methods
   - Text wrapping logic isolated to `visit_Text`
   - Document-level wrapper is simple: `#[` start, `]` end

5. **Future-Proof Architecture**
   - Easy to add new elements following the same pattern
   - Consistent approach scales to new Typst features
   - Maintainable for long-term evolution

## Alternatives Considered

### Alternative 1: Keep Sugar Syntax (Status Quo)
**Rejected**: Continues all current problems

### Alternative 2: Partial Conversion (Original Issue #4 Scope)
**Rejected**: Still leaves inconsistency, doesn't solve architectural issues

### Alternative 3: Function Calls with `#` Prefixes
**Rejected**: Requires `#` prefix management in every visit method, more complex

### Alternative 4: Make Sugar Syntax Configurable
**Rejected**: Adds complexity, still requires maintaining two code paths

### Alternative 5: Code Mode Approach (This Proposal)
**Selected**: Maximum rigor, simplest implementation, matches existing toctree pattern

## Implementation Strategy

### Phase 0: Document Wrapper (Foundation)
- Update `visit_document()` to output `#{\n`
- Update `depart_document()` to output `}\n`
- This enables all other conversions

### Phase 1: Remove `#` Prefixes from Existing Functions
- Update all existing function calls to remove `#` prefix:
  - `#sub[...]` → `sub[...]`
  - `#super[...]` → `super[...]`
  - `#quote[...]` → `quote[...]`
  - `#image(...)` → `image(...)`
  - `#figure(...)` → `figure(...)`
  - `#table(...)` → `table(...)`
  - `#link(...)` → `link(...)`
  - Admonitions: `#info[...]`, `#warning[...]`, `#tip[...]` → `info[...]`, `warning[...]`, `tip[...]`
  - Inline Math: `` #mi(`...`) `` → `` mi(`...`) `` (keep backticks for raw strings)
  - Block Math: `` #mitex(`...`) `` → `` mitex(`...`) `` (keep backticks for raw strings)

### Phase 2: Text Node and Paragraph Wrapping
- Update `visit_Text()` to wrap text in `text("...")` function
- Handle string escaping (quotes, backslashes)
- Implement concatenation with `+` operator for adjacent nodes
- Handle edge cases: empty text, whitespace-only text
- Update `visit_paragraph()` to output `par(` and `depart_paragraph()` to output `)`
- Ensure paragraph content (all inline elements) is wrapped in single `par()` call

### Phase 3: Convert Sugar Syntax Elements
1. Emphasis: `_text_` → `emph(text("text"))` (NO `#`)
2. Strong: `*text*` → `strong(text("text"))` (NO `#`)
3. Subtitle: `_subtitle_` → `emph(text("subtitle"))` (NO `#`)
4. Field Names: `*name*` → `strong(text("name"))` (NO `#`)
5. Headings: `= Heading` → `heading(level: N, text("Heading"))` (NO `#`)
6. Inline Code: `` `code` `` → ``raw(`code`)`` (NO `#`, backtick raw string)
7. Code Blocks: ` ```lang ` → ``raw(block: true, lang: "...", `code`)`` (NO `#`, backtick raw string, preserve codly integration)

### Phase 4: Lists (State Redesign)
- Current: Incremental generation (`visit_list_item` adds `- ` per item)
- Target: Collect all items, then generate `list(text("item1"), text("item2"))` (NO `#`)
- Requires significant state management changes
- Also applies to definition lists: `terms(terms.item(text("term"), text("def")), ...)` (NO `#`)

### Phase 5: Integration & Testing
- Update all test fixtures
- Comprehensive integration tests
- PDF output verification (should be identical)

## Validation Criteria

1. **All sugar syntax converted** (except Typst standard)
2. **All tests passing** (mypy, black, ruff, tox)
3. **PDF output identical** for test cases
4. **No syntax errors** in generated `.typ` files
5. **Documentation updated** with new approach

## Migration Guide for Users

### For Library Users (Sphinx Projects)

**Action Required**: Rebuild all documents after upgrading

```bash
# After upgrading sphinx-typst to v0.3.0/v1.0.0
rm -rf _build/typst
make typst
```

**Expected Changes**:
- Generated `.typ` files will have different syntax
- PDF output remains identical
- Version control will show large diffs (source format change)

### For Contributors

**New Contribution Guidelines**:
- ALL new elements MUST use function syntax
- Sugar syntax is only for Typst standard forms
- Follow the consistent pattern across all `visit_*` methods

## References

- **Issue #4**: Convert sugar syntax to function call syntax (examples)
- **Issue #55**: Syntax error from `*_templates/custom_ieee.typ*:` combination
- **Typst Documentation**: Function reference for all element types
- **sphinx-typst Architecture**: Visitor pattern implementation

## Open Questions

1. Should inline code `` `...` `` and code blocks ` ```...``` ` be converted to `raw()` functions?
   - **Recommendation**: Keep as-is (they work in code mode and are Typst standard)

2. Should definition lists (`/ term: def`) be kept as-is?
   - **Recommendation**: Keep as-is (Typst standard term list syntax)

3. How should text node wrapping handle edge cases (empty text, whitespace)?
   - **Needs Investigation**: Test behavior in Phase 2 implementation

## Timeline

1. **Proposal Review**: 2025-10-25 - 2025-10-27
2. **Implementation**: 2025-10-28 - 2025-11-08 (5 phases, updated)
3. **Testing & Validation**: 2025-11-09 - 2025-11-11
4. **Release**: v0.3.0 or v1.0.0 by 2025-11-15
