# Specification: Document Conversion - Unified Code Mode Architecture

## Overview

This specification defines the requirements for establishing a unified code mode architecture in sphinx-typst translator. The entire document will be wrapped in a single `#[...]` code mode block, with all function calls using bare function names (no `#` prefix) and all text wrapped in content blocks `[...]`.

---

## ADDED Requirements

### Requirement: ドキュメント全体のコードモード化

ドキュメント全体は単一のコードモードブロック `#[...]` で包まれなければならない (MUST)。コードモードブロック内のすべての関数呼び出しは `#` プレフィックスを使用してはならない (MUST NOT)。すべてのテキストコンテンツは `text()` 関数で包まれなければならない (MUST)。

**Rationale**: Document-level code mode provides maximum rigor and consistency. `text()` function uses string mode (not markup mode), eliminating the need to escape special characters like `#`, `*`, `_`, `$`, `[`, `]`.

#### Scenario: ドキュメントの開始

```gherkin
GIVEN a Sphinx document being translated
WHEN visit_document() is called
THEN the output MUST start with `#[\n`
AND NOT with any other content
```

#### Scenario: ドキュメントの終了

```gherkin
GIVEN a Sphinx document translation completing
WHEN depart_document() is called
THEN the output MUST end with `]\n`
AND NOT with any other content
```

#### Scenario: 完全なドキュメント構造

```gherkin
GIVEN a Sphinx document with heading and text
WHEN the document is fully translated
THEN the output structure MUST be:
  #[
    heading(level: 1, text("Title"))
    text("Text content")
  ]
AND the entire content MUST be wrapped in the code mode block
AND all text MUST use text() function
```

---

## MODIFIED Requirements

### Requirement: 見出しの変換

見出しノードは `heading()` 関数として出力されなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`=`, `==`, `===`, etc.) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. Explicit function calls provide clear 1:1 mapping between visitor methods and Typst functions.

#### Scenario: 第1レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 1 heading "Introduction"
WHEN the translator processes the title node at section_level=1
THEN the output MUST be `heading(level: 1, text("Introduction"))`
AND NOT `#heading(level: 1, text("Introduction"))` (no # prefix)
AND NOT `= Introduction` (no sugar syntax)
```

#### Scenario: 第2レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 2 heading "Background"
WHEN the translator processes the title node at section_level=2
THEN the output MUST be `heading(level: 2, text("Background"))`
AND NOT `#heading(level: 2, text("Background"))` (no # prefix)
AND NOT `== Background` (no sugar syntax)
```

#### Scenario: 第6レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 6 heading "Details"
WHEN the translator processes the title node at section_level=6
THEN the output MUST be `heading(level: 6, text("Details"))`
AND NOT `====== Details` (no sugar syntax)
```

---

### Requirement: 強調と太字の変換

強調ノードは `emph(text(...))` として、太字ノードは `strong(text(...))` として出力されなければならない (MUST)。テキストコンテンツは `text()` 関数で包まれなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`_text_`, `*text*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. `text()` function eliminates escaping issues. Function syntax eliminates syntax errors from nested combinations like `*_text_*` (Issue #55).

#### Scenario: 強調テキストの変換

```gherkin
GIVEN a Sphinx document with emphasis text "important"
WHEN the translator processes an emphasis node inside code mode
THEN the output MUST be `emph(text("important"))`
AND NOT `emph(text("important"))` (no # prefix)
AND NOT `_important_` (no sugar syntax)
```

#### Scenario: 太字テキストの変換

```gherkin
GIVEN a Sphinx document with strong text "critical"
WHEN the translator processes a strong node inside code mode
THEN the output MUST be `strong(text("critical"))`
AND NOT `strong(text("critical"))` (no # prefix)
AND NOT `*critical*` (no sugar syntax)
```

#### Scenario: 強調と太字のネスト

```gherkin
GIVEN a Sphinx document with nested strong and emphasis nodes
WHEN the translator processes strong node containing emphasis node "nested"
THEN the output MUST be `strong(emph(text("nested")))`
AND NOT `strong[#emph[nested]]` (no # prefix)
AND NOT `*_nested_*` (which causes unclosed delimiter errors)
```

#### Scenario: アンダースコアを含む太字テキスト

```gherkin
GIVEN a Sphinx document with strong text "file_name.txt"
WHEN the translator processes a strong node
THEN the output MUST be `strong(text("file_name.txt"))`
AND NOT `*file_name.txt*` (which causes unclosed delimiter errors due to `_`)
```

---

### Requirement: リストの変換

箇条書きリストは `list()` 関数として、番号付きリストは `enum()` 関数として出力されなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`- item`, `+ item`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. Function-based list generation enables proper item collection and supports complex nested structures.

#### Scenario: 単純な箇条書きリスト

```gherkin
GIVEN a Sphinx document with a bullet list containing 3 items
WHEN the translator processes the bullet_list node
THEN the output MUST be `list([item 1], [item 2], [item 3])`
AND NOT:
  - item 1
  - item 2
  - item 3
```

#### Scenario: 単純な番号付きリスト

```gherkin
GIVEN a Sphinx document with an enumerated list containing 3 items
WHEN the translator processes the enumerated_list node
THEN the output MUST be `enum([item 1], [item 2], [item 3])`
AND NOT:
  + item 1
  + item 2
  + item 3
```

#### Scenario: ネストされた箇条書きリスト

```gherkin
GIVEN a Sphinx document with nested bullet lists (2 levels)
WHEN the translator processes the nested structure
THEN the output MUST be:
  #list(
    [item 1],
    [item 2 #list([nested 1], [nested 2])],
    [item 3]
  )
AND nested lists MUST use function syntax, NOT indented sugar syntax
```

#### Scenario: 混在したネストリスト

```gherkin
GIVEN a Sphinx document with bullet list containing enumerated sub-list
WHEN the translator processes the mixed nested structure
THEN the output MUST use `list()` for outer list and `enum()` for inner list
AND both MUST use function syntax
```

#### Scenario: リスト項目内の複雑なコンテンツ

```gherkin
GIVEN a bullet list item containing paragraphs, code blocks, and emphasis
WHEN the translator processes the complex list item
THEN the output MUST collect all content within the list item's `[...]` block
AND maintain proper nesting of all child elements
```

---

### Requirement: 定義リストの維持

定義リストは Typst 標準の `/ term: definition` 構文を使用しなければならない (MUST)。これは sugar syntax ではなく、Typst の標準的な term list 構文である。

**Rationale**: Definition lists already use Typst's standard term list syntax, which is the canonical form with no function equivalent.

#### Scenario: 単純な定義リストの維持

```gherkin
GIVEN a Sphinx document with a definition list
WHEN the translator processes term and definition nodes
THEN the output MUST be `/ term: definition`
AND MUST NOT be changed to any function syntax
```

---

## ADDED Requirements

### Requirement: サブタイトルの変換

サブタイトルノードは `emph[]` 関数として出力されなければならない (MUST)。Sugar syntax (`_subtitle_`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Subtitle semantics map to emphasis in Typst. Using `emph[]` ensures consistency with other emphasis elements.

#### Scenario: サブタイトルの変換

```gherkin
GIVEN a Sphinx document with a subtitle "A Comprehensive Guide"
WHEN the translator processes a subtitle node
THEN the output MUST be `emph[A Comprehensive Guide]`
AND NOT `_A Comprehensive Guide_`
```

#### Scenario: サブタイトル内の特殊文字

```gherkin
GIVEN a subtitle containing special characters "Version 1.0 - Beta"
WHEN the translator processes the subtitle node
THEN the output MUST be `emph[Version 1.0 - Beta]`
AND special characters MUST be preserved correctly
```

---

### Requirement: APIドキュメントのフィールド名変換

APIドキュメント内のフィールド名は `strong[]` 関数として出力されなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`*name*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. Consistency with the unified code mode approach requires all strong formatting to use `strong[]`.

#### Scenario: Parameters フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Parameters"
WHEN the translator processes the field_name node inside code mode
THEN the output MUST be `strong[Parameters:]`
AND NOT `#strong[Parameters:]` (no # prefix)
AND NOT `*Parameters:*` (no sugar syntax)
```

#### Scenario: Returns フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Returns"
WHEN the translator processes the field_name node inside code mode
THEN the output MUST be `strong[Returns:]`
AND NOT `*Returns:*` (no sugar syntax)
```

---

### Requirement: テキストノードの `text()` 関数化

テキストノードは `text("...")` 関数で包まれなければならない (MUST)。`[...]` マークアップモードを使用してはならない (MUST NOT)。

**Rationale**: `text()` function uses string mode, eliminating the need to escape special characters (`#`, `*`, `_`, `$`, `[`, `]`). Markup mode `[...]` requires escaping and can cause syntax errors.

#### Scenario: 通常のテキストノードの変換

```gherkin
GIVEN a Text node with content "Hello world"
WHEN the translator processes the text node inside code mode
THEN the output MUST be `text("Hello world")`
AND NOT `[Hello world]` (markup mode)
```

#### Scenario: 特殊文字を含むテキスト

```gherkin
GIVEN a Text node with content "Price: $100 #1"
WHEN the translator processes the text node
THEN the output MUST be `text("Price: $100 #1")`
AND all characters MUST be literal (no escaping needed)
AND NOT `[Price: $100 #1]` (would require escaping in markup mode)
```

#### Scenario: 隣接するテキストとフォーマットの組み合わせ

```gherkin
GIVEN text "This is " followed by emphasis "important" followed by text " text"
WHEN the translator processes these nodes
THEN the output MUST be `text("This is ") + emph(text("important")) + text(" text")`
AND use `+` operator to concatenate
```

#### Scenario: 空のテキストノード

```gherkin
GIVEN a Text node with empty content
WHEN the translator processes the text node
THEN the output MAY be `text("")` or omitted
AND MUST NOT cause syntax errors
```

---

### Requirement: 既存関数呼び出しの `#` プレフィックス除去

既に関数構文を使用している要素（subscript, superscript, quote, image, figure, table, link, admonitions, math）は `#` プレフィックスを除去しなければならない (MUST)。

**Rationale**: Inside code mode block, ALL function calls use bare names without `#` prefix.

#### Scenario: Subscript/Superscript の変換

```gherkin
GIVEN subscript or superscript elements
WHEN the translator processes these nodes inside code mode
THEN the output MUST be `sub[text]` and `super[text]`
AND NOT `#sub[text]` and `#super[text]`
```

#### Scenario: Block Quote の変換

```gherkin
GIVEN a block quote element
WHEN the translator processes the block_quote node inside code mode
THEN the output MUST be `quote[...]`
AND NOT `#quote[...]`
```

#### Scenario: Image/Figure/Table の変換

```gherkin
GIVEN image, figure, or table elements
WHEN the translator processes these nodes inside code mode
THEN the output MUST be `image(...)`, `figure(...)`, `table(...)`
AND NOT `#image(...)`, `#figure(...)`, `#table(...)`
```

#### Scenario: Admonitions の変換

```gherkin
GIVEN admonition elements (note, warning, tip, etc.)
WHEN the translator processes these nodes inside code mode
THEN the output MUST be `info[...]`, `warning[...]`, `tip[...]`
AND NOT `#info[...]`, `#warning[...]`, `#tip[...]`
```

---

### Requirement: コードの `raw()` 関数化

インラインコードとコードブロックは `raw()` 関数として出力されなければならない (MUST)。Sugar syntax (`` ` ``, ` ``` `) による出力は使用してはならない (MUST NOT)。

**Rationale**: Codly uses `show raw.where(block: true)` and `raw.line` internally, making `raw()` function the proper way to integrate with codly. This ensures all codly features (line numbers, highlighting, annotations) work correctly while maintaining consistency with the unified code mode approach.

#### Scenario: インラインコードの変換

```gherkin
GIVEN a Sphinx document with inline code "print(x)"
WHEN the translator processes a literal node inside code mode
THEN the output MUST be `raw("print(x)")`
AND NOT `` `print(x)` `` (sugar syntax)
```

#### Scenario: コードブロックの変換

```gherkin
GIVEN a Sphinx document with a Python code block
WHEN the translator processes a literal_block node inside code mode
THEN the output MUST be `raw(block: true, lang: "python", "code content")`
AND NOT ` ```python\ncode\n``` ` (sugar syntax)
```

#### Scenario: Codly統合の維持

```gherkin
GIVEN a code block with line numbers and highlighting enabled
WHEN codly() and codly-range() are called before raw()
THEN codly features (line numbers, highlighting) MUST work correctly
AND raw() function MUST integrate with codly's show rules
```

#### Scenario: キャプション付きコードブロック

```gherkin
GIVEN a code block with :caption: option
WHEN the translator generates output inside code mode
THEN the output MUST be `figure(caption: text("..."), raw(block: true, lang: "...", "code"))`
AND codly features MUST still work
```

---

## Validation Rules

1. **Document Wrapped in Code Mode**
   - MUST start with `#[\n`
   - MUST end with `]\n`
   - ALL content MUST be inside code mode block

2. **No `#` Prefixes Inside Code Mode**
   - MUST NOT generate `#heading(...)`, `#emph[...]`, `#strong[...]`
   - MUST generate `heading(...)`, `emph[...]`, `strong[...]` (bare names)
   - Applies to ALL function calls inside code mode

3. **No Sugar Syntax in Output**
   - MUST NOT generate `=`, `_`, `*` for headings, emphasis, strong
   - MUST NOT generate `-`, `+` for lists
   - MUST NOT generate `` ` ``, ` ``` ` for code (use `raw()` function)
   - MAY generate `/ ` for definition lists (Typst standard term list syntax)
   - MAY generate `$` for math (Typst standard math delimiters)

4. **All Function Calls Well-Formed**
   - MUST generate `heading(level: N, text("..."))` (no `#`, use `text()`)
   - MUST generate `emph(text("..."))`, `strong(text("..."))` (no `#`, use `text()`)
   - MUST generate `list(text("..."), text("..."))`, `enum(text("..."), text("..."))` (no `#`, use `text()`)
   - MUST generate `raw("code")` for inline code (no `#`)
   - MUST generate `raw(block: true, lang: "...", "code")` for code blocks (no `#`)

5. **Text Nodes Use `text()` Function**
   - Text content MUST be wrapped in `text("...")` function
   - MUST NOT use `[...]` markup mode (requires escaping)
   - Use `+` operator to concatenate adjacent text and formatting

6. **Nested Elements Properly Handled**
   - MUST support `strong(emph(text("nested")))`
   - MUST support `list(emph(text("item")), strong(text("item")))`
   - MUST NOT generate malformed syntax combinations

7. **PDF Output Unchanged**
   - Generated PDFs MUST be visually identical to previous versions
   - Only source `.typ` format changes, not compiled output

---

## Implementation Notes

### Document Wrapper

Wrap entire document in code mode:

```python
# visit_document()
def visit_document(self, node):
    self.add_text("#[\n")

# depart_document()
def depart_document(self, node):
    self.add_text("]\n")
```

### Remove `#` Prefixes

All function calls must remove `#` prefix:

```python
# Current
self.add_text("#emph[")

# Target
self.add_text("emph[")
```

### Text Node Wrapping with `text()` Function

Wrap ALL text in `text()` function to avoid escaping issues:

```python
# visit_Text()
def visit_Text(self, node):
    text_content = node.astext()
    # Escape quotes in string
    escaped = text_content.replace('"', '\\"')
    self.add_text(f'text("{escaped}")')
```

**Why `text()` not `[...]`?**
- `text("...")` uses string mode → no need to escape `#`, `*`, `_`, `$`, `[`, `]`
- `[...]` uses markup mode → requires escaping special characters
- Example: `text("$100 #1")` works, `[$100 #1]` breaks

**For concatenation**:
```python
# Multiple text + formatting nodes
# Output: text("This is ") + emph(text("important")) + text(" text")
self.add_text('text("This is ") + ')
self.add_text('emph(text("important")) + ')
self.add_text('text(" text")')
```

### List State Redesign

Current implementation generates list markers incrementally:

```python
# Current (incremental)
def visit_list_item(self, node):
    self.add_text("- ")  # Add marker immediately
```

New implementation must collect items first:

```python
# Target (collection-based)
def visit_bullet_list(self, node):
    items = self._collect_list_items(node)
    # Each item is already wrapped in text() during collection
    self.add_text(f"list({', '.join(items)})")
```

**Item collection example**:
```python
# Each list item content → text("item content")
# Result: list(text("First"), text("Second"), text("Third"))
```

Note: NO `#` prefix, all text uses `text()`

### Heading Level Parameter

Heading level must be passed as parameter, heading text wrapped in `text()`:

```python
# Current
heading_prefix = "=" * self.section_level

# Target
self.add_text(f"heading(level: {self.section_level}, ")
# Heading text content processed by visit_Text → text("...")
# Final: heading(level: 1, text("Title"))
```

Note: NO `#` prefix, heading content uses `text()`

### Code Block with `raw()` Function and Codly Integration

Convert code blocks to `raw()` function while preserving codly features:

```python
# Current (sugar syntax with codly)
def visit_literal_block(self, node):
    if not linenos:
        self.add_text("#codly(number-format: none)\n")
    if hl_lines:
        self.add_text(f"#codly-range(highlight: ({highlight_str}))\n")
    self.add_text(f"```{language}\n")

# Target (raw() function with codly)
def visit_literal_block(self, node):
    if not linenos:
        self.add_text("codly(number-format: none)\n")  # NO #
    if hl_lines:
        self.add_text(f"codly-range(highlight: ({highlight_str}))\n")  # NO #

    # Get code content
    code_content = node.astext()
    escaped = code_content.replace('"', '\\"')

    # Generate raw() function
    lang = node.get("language", "")
    if lang:
        self.add_text(f'raw(block: true, lang: "{lang}", "{escaped}")\n')
    else:
        self.add_text(f'raw(block: true, "{escaped}")\n')
```

**Codly compatibility**:
- Codly uses `show raw.where(block: true)` show rules
- `raw()` function integrates with codly's `raw.line` processing
- All features preserved: line numbers, highlighting, zebra striping, annotations

### Inline Code with `raw()` Function

Convert inline code to `raw()` function:

```python
# Current
def visit_literal(self, node):
    self.add_text("`")

def depart_literal(self, node):
    self.add_text("`")

# Target
def visit_literal(self, node):
    code_content = node.astext()
    escaped = code_content.replace('"', '\\"')
    self.add_text(f'raw("{escaped}")')
    raise nodes.SkipNode  # Don't process children
```

---

## Test Coverage Requirements

1. **Unit Tests**: Each element type (heading, emphasis, strong, subtitle, lists, field names)
2. **Integration Tests**: Nested combinations, complex documents
3. **Regression Tests**: PDF output comparison (must be identical)
4. **Error Cases**: Malformed input handling

---

## Migration Impact

**Breaking Change**: YES

Users must rebuild all documents after upgrading. Generated `.typ` files will have different source format, but PDF output remains identical.
