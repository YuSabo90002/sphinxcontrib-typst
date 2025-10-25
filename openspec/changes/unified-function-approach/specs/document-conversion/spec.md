# Specification: Document Conversion - Unified Code Mode Architecture

## Overview

This specification defines the requirements for establishing a unified code mode architecture in sphinx-typst translator. The entire document will be wrapped in a single `#[...]` code mode block, with all function calls using bare function names (no `#` prefix) and all text wrapped in content blocks `[...]`.

---

## ADDED Requirements

### Requirement: ドキュメント全体のコードモード化

ドキュメント全体は単一のコードモードブロック `#[...]` で包まれなければならない (MUST)。コードモードブロック内のすべての関数呼び出しは `#` プレフィックスを使用してはならない (MUST NOT)。

**Rationale**: Document-level code mode provides maximum rigor and consistency, eliminates `#` prefix management complexity, and matches the existing toctree implementation pattern.

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
    heading(level: 1)[Title]
    [Text content]
  ]
AND the entire content MUST be wrapped in the code mode block
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
THEN the output MUST be `heading(level: 1)[Introduction]`
AND NOT `#heading(level: 1)[Introduction]` (no # prefix)
AND NOT `= Introduction` (no sugar syntax)
```

#### Scenario: 第2レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 2 heading "Background"
WHEN the translator processes the title node at section_level=2
THEN the output MUST be `heading(level: 2)[Background]`
AND NOT `#heading(level: 2)[Background]` (no # prefix)
AND NOT `== Background` (no sugar syntax)
```

#### Scenario: 第6レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 6 heading "Details"
WHEN the translator processes the title node at section_level=6
THEN the output MUST be `heading(level: 6)[Details]`
AND NOT `====== Details` (no sugar syntax)
```

---

### Requirement: 強調と太字の変換

強調ノードは `emph[]` として、太字ノードは `strong[]` として出力されなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`_text_`, `*text*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. Function syntax eliminates syntax errors from nested combinations like `*_text_*` (Issue #55).

#### Scenario: 強調テキストの変換

```gherkin
GIVEN a Sphinx document with emphasis text "important"
WHEN the translator processes an emphasis node inside code mode
THEN the output MUST be `emph[important]`
AND NOT `emph[important]` (no # prefix)
AND NOT `_important_` (no sugar syntax)
```

#### Scenario: 太字テキストの変換

```gherkin
GIVEN a Sphinx document with strong text "critical"
WHEN the translator processes a strong node inside code mode
THEN the output MUST be `strong[critical]`
AND NOT `strong[critical]` (no # prefix)
AND NOT `*critical*` (no sugar syntax)
```

#### Scenario: 強調と太字のネスト

```gherkin
GIVEN a Sphinx document with nested strong and emphasis nodes
WHEN the translator processes strong node containing emphasis node "nested"
THEN the output MUST be `strong[emph[nested]]`
AND NOT `strong[#emph[nested]]` (no # prefix)
AND NOT `*_nested_*` (which causes unclosed delimiter errors)
```

#### Scenario: アンダースコアを含む太字テキスト

```gherkin
GIVEN a Sphinx document with strong text "file_name.txt"
WHEN the translator processes a strong node
THEN the output MUST be `strong[file_name.txt]`
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

### Requirement: テキストノードのコンテンツブロック化

テキストノードは `[...]` コンテンツブロックで包まれなければならない (MUST)。ただし、既にコンテンツブロック内にある場合は二重にラップしてはならない (MUST NOT)。

**Rationale**: Inside code mode block, text content must be wrapped in content blocks to distinguish it from code. Intelligent wrapping prevents `[[...]]` double-wrapping.

#### Scenario: 通常のテキストノードの変換

```gherkin
GIVEN a Text node with content "Hello world"
WHEN the translator processes the text node inside code mode
AND the text is NOT already inside a content block
THEN the output MUST be `[Hello world]`
AND NOT plain text `Hello world`
```

#### Scenario: 既にコンテンツブロック内のテキスト

```gherkin
GIVEN a Text node inside an emphasis element
WHEN the emphasis element already provides `emph[...]` content block
THEN the text MUST NOT be double-wrapped
AND the output MUST be `emph[text]`
AND NOT `emph[[text]]` (double wrapping)
```

#### Scenario: 空のテキストノード

```gherkin
GIVEN a Text node with empty content
WHEN the translator processes the text node
THEN the output MAY be empty or `[]`
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

### Requirement: Typst標準構文の維持

コードブロック、インラインコード、数式デリミタは Typst の標準構文を維持しなければならない (MUST)。これらは sugar syntax ではなく、Typst の公式な表記法である。

**Rationale**: These syntaxes are Typst standard forms with no function equivalents. They are not "sugar syntax" but the canonical Typst way to express these elements.

#### Scenario: インラインコードの維持

```gherkin
GIVEN a Sphinx document with inline code "print(x)"
WHEN the translator processes a literal node
THEN the output MUST be `print(x)`
AND MUST NOT be converted to any function form
```

#### Scenario: コードブロックの維持

```gherkin
GIVEN a Sphinx document with a code block in Python
WHEN the translator processes a literal_block node
THEN the output MUST be ```python\ncode\n```
AND MUST NOT be converted to any function form
```

#### Scenario: 数式デリミタの維持

```gherkin
GIVEN math content in Typst native mode
WHEN the translator processes inline or block math
THEN the output MUST use `$...$` delimiters
AND MUST NOT be changed (this is Typst standard)
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

3. **No Sugar Syntax in Output** (except Typst standard)
   - MUST NOT generate `=`, `_`, `*` for headings, emphasis, strong
   - MUST NOT generate `-`, `+` for lists
   - MAY generate `` ` ``, ` ``` `, `/ `, `$` (Typst standard)

4. **All Function Calls Well-Formed**
   - MUST generate `heading(level: N)[...]` (no `#`)
   - MUST generate `emph[...]`, `strong[...]` (no `#`)
   - MUST generate `list([...], [...])`, `enum([...], [...])` (no `#`)

5. **Text Nodes Wrapped**
   - Text content MUST be wrapped in `[...]` content blocks
   - MUST NOT double-wrap (avoid `[[...]]`)

6. **Nested Elements Properly Handled**
   - MUST support `strong[emph[nested]]`
   - MUST support `list([emph[item]], [strong[item]])`
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

### Text Node Wrapping

Wrap text in content blocks with intelligent double-wrap prevention:

```python
# visit_Text()
def visit_Text(self, node):
    text = node.astext()
    if self._needs_content_block():
        self.add_text(f"[{text}]")
    else:
        self.add_text(text)
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
    self.add_text(f"list({', '.join(f'[{item}]' for item in items)})")
```

Note: NO `#` prefix

### Heading Level Parameter

Heading level must be passed as parameter:

```python
# Current
heading_prefix = "=" * self.section_level

# Target
self.add_text(f"heading(level: {self.section_level})[")
```

Note: NO `#` prefix

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
