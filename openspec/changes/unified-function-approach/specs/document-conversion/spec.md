# Specification: Document Conversion - Unified Code Mode Architecture

## Overview

This specification defines the requirements for establishing a unified code mode architecture in sphinx-typst translator. The entire document will be wrapped in a single `#{...}` code mode block, with all function calls using bare function names (no `#` prefix) and all text wrapped in `text()` functions.

---

## ADDED Requirements

### Requirement: ドキュメント全体のコードモード化

ドキュメント全体は単一のコードモードブロック `#{...}` で包まれなければならない (MUST)。コードモードブロック内のすべての関数呼び出しは `#` プレフィックスを使用してはならない (MUST NOT)。すべてのテキストコンテンツは `text()` 関数で包まれなければならない (MUST)。

**Rationale**: Document-level code mode provides maximum rigor and consistency. `text()` function uses string mode (not markup mode), eliminating the need to escape special characters like `#`, `*`, `_`, `$`, `[`, `}`.

#### Scenario: ドキュメントの開始

```gherkin
GIVEN a Sphinx document being translated
WHEN visit_document() is called
THEN the output MUST start with `#{\n`
AND NOT with any other content
```

#### Scenario: ドキュメントの終了

```gherkin
GIVEN a Sphinx document translation completing
WHEN depart_document() is called
THEN the output MUST end with `}\n`
AND NOT with any other content
```

#### Scenario: 完全なドキュメント構造

```gherkin
GIVEN a Sphinx document with heading and text
WHEN the document is fully translated
THEN the output structure MUST be:
  #{
    heading(level: 1, text("Title"))
    text("Text content")
  }
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
AND NOT `strong(emph[nested])` (use text() function, not markup mode)
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

### Requirement: 定義リストの `terms.item()` 関数化

定義リストは `terms.item()` 関数として出力されなければならない (MUST)。Sugar syntax (`/ term: definition`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Typst has `terms.item(term, description)` function for programmatic term list creation. This ensures consistency with the unified function approach.

#### Scenario: 単純な定義リストの変換

```gherkin
GIVEN a Sphinx document with a definition list (term "API", definition "Application Programming Interface")
WHEN the translator processes the definition_list node inside code mode
THEN the output MUST be `terms(terms.item(text("API"), text("Application Programming Interface")))`
AND NOT `/ API: Application Programming Interface` (sugar syntax)
```

#### Scenario: 複数の定義項目

```gherkin
GIVEN a definition list with 3 term-definition pairs
WHEN the translator processes the definition_list node
THEN the output MUST be `terms(terms.item(text("term1"), text("def1")), terms.item(text("term2"), text("def2")), terms.item(text("term3"), text("def3")))`
AND all items MUST use terms.item() function
```

#### Scenario: 定義内の複雑なコンテンツ

```gherkin
GIVEN a definition containing emphasis and strong elements
WHEN the translator processes the definition content
THEN the output MUST be `terms.item(text("term"), text("Definition with ") + emph(text("emphasis")) + text(" and ") + strong(text("strong")))`
AND nested formatting MUST be preserved
```

---

## ADDED Requirements

### Requirement: サブタイトルの変換

サブタイトルノードは `emph(text("..."))` 関数として出力されなければならない (MUST)。Sugar syntax (`_subtitle_`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Subtitle semantics map to emphasis in Typst. Using `emph()` with `text()` ensures consistency with other emphasis elements and avoids markup mode escaping issues.

#### Scenario: サブタイトルの変換

```gherkin
GIVEN a Sphinx document with a subtitle "A Comprehensive Guide"
WHEN the translator processes a subtitle node
THEN the output MUST be `emph(text("A Comprehensive Guide"))`
AND NOT `emph[A Comprehensive Guide]` (use text() function, not markup mode)
AND NOT `_A Comprehensive Guide_` (no sugar syntax)
```

#### Scenario: サブタイトル内の特殊文字

```gherkin
GIVEN a subtitle containing special characters "Version 1.0 - Beta"
WHEN the translator processes the subtitle node
THEN the output MUST be `emph(text("Version 1.0 - Beta"))`
AND special characters MUST be preserved correctly without escaping
```

---

### Requirement: APIドキュメントのフィールド名変換

APIドキュメント内のフィールド名は `strong(text("..."))` 関数として出力されなければならない (MUST)。`#` プレフィックスを使用してはならない (MUST NOT)。Sugar syntax (`*name*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Inside code mode block, function calls use bare names. Consistency with the unified code mode approach requires all strong formatting to use `strong()` with `text()` for content.

#### Scenario: Parameters フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Parameters"
WHEN the translator processes the field_name node inside code mode
THEN the output MUST be `strong(text("Parameters:"))`
AND NOT `#strong(text("Parameters:"))` (no # prefix)
AND NOT `strong[Parameters:]` (use text() function, not markup mode)
AND NOT `*Parameters:*` (no sugar syntax)
```

#### Scenario: Returns フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Returns"
WHEN the translator processes the field_name node inside code mode
THEN the output MUST be `strong(text("Returns:"))`
AND NOT `strong[Returns:]` (use text() function, not markup mode)
AND NOT `*Returns:*` (no sugar syntax)
```

---

### Requirement: 段落の `par()` 関数化

段落ノードは `par()` 関数で包まれなければならない (MUST)。コードモード内では空行による段落区切りは自動認識されないため (MUST NOT rely on blank lines)、`par()` で明示的に段落境界をマークしなければならない (MUST)。

**Rationale**: Code mode doesn't automatically recognize paragraph breaks from blank lines. Without `par()`, multiple text blocks merge into a single paragraph, breaking document structure.

#### Scenario: 単純な段落の変換

```gherkin
GIVEN a Sphinx document with a paragraph containing text "This is a paragraph."
WHEN the translator processes the paragraph node inside code mode
THEN the output MUST be `par(text("This is a paragraph."))`
AND NOT just `text("This is a paragraph.")` (missing par wrapper)
```

#### Scenario: インライン要素を含む段落

```gherkin
GIVEN a paragraph with text, emphasis, and strong elements
WHEN the translator processes the paragraph node
THEN the output MUST be `par(text("This is ") + emph(text("emphasized")) + text(" and ") + strong(text("strong")) + text("."))`
AND all inline content MUST be within a single par() call
```

#### Scenario: 複数段落の区切り

```gherkin
GIVEN a Sphinx document with 3 consecutive paragraphs
WHEN the translator processes all paragraph nodes
THEN the output MUST have 3 separate par() calls
AND each paragraph MUST be independently wrapped
THEN the structure MUST be:
  par(text("First paragraph"))
  par(text("Second paragraph"))
  par(text("Third paragraph"))
```

---

### Requirement: テキストノードの `text()` 関数化

テキストノードは `text("...")` 関数で包まれなければならない (MUST)。`[...]` マークアップモードを使用してはならない (MUST NOT)。文字列内では標準的なエスケープシーケンスを使用しなければならない (MUST): `\\` (backslash), `\"` (quote), `\n` (newline), `\r` (carriage return), `\t` (tab), `\u{...}` (Unicode)。

**Rationale**: `text()` function uses string mode, eliminating the need to escape special characters (`#`, `*`, `_`, `$`, `[`, `}`). However, standard string escape sequences must be used for backslash, quotes, newlines, tabs, etc. Markup mode `[...]` requires escaping and can cause syntax errors.

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

#### Scenario: 改行を含むテキスト

```gherkin
GIVEN a Text node with content "Line 1\nLine 2"
WHEN the translator processes the text node
THEN the output MUST be `text("Line 1\nLine 2")`
AND newlines MUST use escape sequence `\n`
AND NOT literal newline characters (would break string)
```

#### Scenario: 引用符を含むテキスト

```gherkin
GIVEN a Text node with content 'He said "Hello"'
WHEN the translator processes the text node
THEN the output MUST be `text("He said \"Hello\"")`
AND quotes MUST be escaped as `\"`
AND NOT unescaped quotes (would break string syntax)
```

#### Scenario: バックスラッシュを含むテキスト

```gherkin
GIVEN a Text node with content "Path: C:\Users\name"
WHEN the translator processes the text node
THEN the output MUST be `text("Path: C:\\Users\\name")`
AND backslashes MUST be escaped as `\\`
AND backslash escaping MUST be done first (before other escaping)
```

#### Scenario: タブを含むテキスト

```gherkin
GIVEN a Text node with content "Column1\tColumn2"
WHEN the translator processes the text node
THEN the output MUST be `text("Column1\tColumn2")`
AND tabs MUST use escape sequence `\t`
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

#### Scenario: Inline Math (mitex) の変換

```gherkin
GIVEN inline math using mitex with LaTeX content "\frac{a}{b}"
WHEN the translator processes the math node inside code mode
THEN the output MUST be `mi(\`\frac{a}{b}\`)`
AND NOT `#mi(\`\frac{a}{b}\`)` (no # prefix)
AND MUST use backticks for raw string (no escaping backslashes)
AND NOT `mi("\\frac{a}{b}")` (string escaping would require double backslashes)
```

#### Scenario: Block Math (mitex) の変換

```gherkin
GIVEN block math using mitex with LaTeX content "\int_0^1 f(x) dx"
WHEN the translator processes the math_block node inside code mode
THEN the output MUST be `mitex(\`\int_0^1 f(x) dx\`)`
AND NOT `#mitex(\`\int_0^1 f(x) dx\`)` (no # prefix)
AND MUST use backticks for raw string (no escaping backslashes)
```

#### Scenario: Math (Typst native) の変換

```gherkin
GIVEN inline or block math using Typst native syntax "x + y"
WHEN the translator processes the math node inside code mode
THEN the output MUST be `$x + y$` for inline or `$ x + y $` for block
AND sugar syntax MUST be kept as-is (works in code mode)
```

---

### Requirement: Toctree の `include()` とスコープ管理

Toctreeで生成される `include()` 呼び出しは**ネストされた content block (`#[...]`)** 内に配置しなければならない (MUST)。`set` と `include()` には `#` プレフィックスが必要である (MUST)。

**Rationale**: Content blocks create isolated scopes for `set` rules. Without a nested content block, `set heading(offset: 1)` would affect ALL subsequent headings in the document, not just the included files. The `#` prefix is required when using `set` and `include()` inside content blocks (`#[...]`). This differs from code blocks (`#{...}`) where `#` prefix is not needed.

#### Scenario: Toctreeの単純な変換

```gherkin
GIVEN a Sphinx toctree with 2 entries
WHEN the translator processes the toctree node inside document-level code mode
THEN the output MUST be:
  #[
    #set heading(offset: 1)
    #include("doc1.typ")
    #include("doc2.typ")
  ]
AND MUST wrap in nested content block #[...] for scope isolation
AND MUST use #include() and #set (# prefix required in content blocks)
```

#### Scenario: Toctreeの相対パス計算

```gherkin
GIVEN a toctree in "guides/index.typ" including "../api/reference.typ"
WHEN the translator computes the relative include path
THEN the output MUST be `#include("../api/reference.typ")`
AND path MUST be relative to the current document
AND # prefix MUST be present (inside content block)
```

#### Scenario: Toctreeのスコープ分離

```gherkin
GIVEN a document with heading before toctree, toctree with includes, and heading after toctree
WHEN the translator generates the complete document
THEN the output structure MUST be:
  #{
    heading(level: 1, text("Before"))  // offset NOT applied
    #[
      #set heading(offset: 1)
      #include("doc1.typ")  // offset applied to included headings
    ]
    heading(level: 1, text("After"))  // offset NOT applied
  }
AND set rule MUST NOT leak outside the content block
```

---

### Requirement: コードの `raw()` 関数化

インラインコードとコードブロックは `raw()` 関数として出力されなければならない (MUST)。コンテンツはバッククオートによるraw string literalとして渡されなければならない (MUST)。エスケープシーケンスの処理は不要である (MUST NOT escape)。Sugar syntax (`` ` ``, ` ``` `) による出力は使用してはならない (MUST NOT)。

**Rationale**: Typst's lexer processes backticks as raw string literals at lexer level, preserving content literally without escape processing. This eliminates the need to escape quotes, backslashes, and special characters. Codly uses `show raw.where(block: true)` and `raw.line` internally, making `raw()` function the proper way to integrate with codly. For code containing backticks, use 3+ backticks as delimiters (minimum 3, not 2).

#### Scenario: インラインコードの変換

```gherkin
GIVEN a Sphinx document with inline code "print(x)"
WHEN the translator processes a literal node inside code mode
THEN the output MUST be `raw(\`print(x)\`)`
AND use backtick raw string literal (no escaping)
AND NOT `` `print(x)` `` (sugar syntax)
AND NOT `raw("print(x)")` (string parameter requires escaping)
```

#### Scenario: 引用符を含むインラインコード

```gherkin
GIVEN a Sphinx document with inline code containing quotes: print("hello")
WHEN the translator processes the literal node inside code mode
THEN the output MUST be `raw(\`print("hello")\`)`
AND quotes MUST NOT be escaped (backticks preserve them literally)
AND NOT `raw("print(\"hello\")")` (string escaping not needed)
```

#### Scenario: バックスラッシュを含むインラインコード

```gherkin
GIVEN a Sphinx document with inline code containing backslashes: C:\path\file
WHEN the translator processes the literal node inside code mode
THEN the output MUST be `raw(\`C:\path\file\`)`
AND backslashes MUST NOT be escaped (backticks preserve them literally)
AND NOT `raw("C:\\path\\file")` (string escaping not needed)
```

#### Scenario: コードブロックの変換

```gherkin
GIVEN a Sphinx document with a Python code block containing quotes and newlines
WHEN the translator processes a literal_block node inside code mode
THEN the output MUST be `raw(block: true, lang: "python", \`def hello():
    print("world")\`)`
AND use backtick raw string literal (no escaping)
AND NOT ` ```python\ncode\n``` ` (sugar syntax)
AND NOT `raw(block: true, lang: "python", "def hello():\n    print(\"world\")")` (string escaping not needed)
```

#### Scenario: バッククオートを含むコード

```gherkin
GIVEN a Sphinx document with code containing a single backtick: `code`
WHEN the translator processes the literal node inside code mode
THEN the output MUST be `raw(\`\`\`code with \`backtick\` inside\`\`\`)`
AND use 3 backticks as delimiters (minimum required)
AND inner backticks MUST be preserved literally
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
THEN the output MUST be `figure(caption: text("..."), raw(block: true, lang: "...", \`code\`))`
AND codly features MUST still work
```

---

## Validation Rules

1. **Document Wrapped in Code Mode**
   - MUST start with `#{\n`
   - MUST end with `}\n`
   - ALL content MUST be inside code mode block

2. **No `#` Prefixes Inside Code Mode**
   - MUST NOT generate `#heading(...)`, `#emph(...)`, `#strong(...)`
   - MUST generate `heading(...)`, `emph(...)`, `strong(...)` (bare names)
   - Applies to ALL function calls inside code mode

3. **No Sugar Syntax in Output**
   - MUST NOT generate `=`, `_`, `*` for headings, emphasis, strong
   - MUST NOT generate `-`, `+` for lists
   - MUST NOT generate `` ` ``, ` ``` ` for code (use `raw()` function)
   - MUST NOT generate `/ ` for definition lists (use `terms.item()` function)
   - MAY generate `$` for math (Typst standard math delimiters - only element without function alternative)

4. **All Function Calls Well-Formed**
   - MUST generate `heading(level: N, text("..."))` (no `#`, use `text()`)
   - MUST generate `emph(text("..."))`, `strong(text("..."))` (no `#`, use `text()`)
   - MUST generate `list(text("..."), text("..."))`, `enum(text("..."), text("..."))` (no `#`, use `text()`)
   - MUST generate ``raw(`code`)`` for inline code (no `#`, backtick raw string)
   - MUST generate ``raw(block: true, lang: "...", `code`)`` for code blocks (no `#`, backtick raw string)
   - MUST generate `terms(terms.item(text("term"), text("def")), ...)` for definition lists (no `#`)

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
    self.add_text("#{\n")

# depart_document()
def depart_document(self, node):
    self.add_text("}\n")
```

### Remove `#` Prefixes and Use `text()` for Content

All function calls must remove `#` prefix and use `text()` for text content:

```python
# Current
self.add_text("#emph[")

# Target
self.add_text("emph(")
# Content processed by visit_Text() → text("...")
# Result: emph(text("content"))
```

### Paragraph Wrapping with `par()` Function

Wrap each paragraph in `par()` function to mark paragraph boundaries:

```python
# visit_paragraph()
def visit_paragraph(self, node):
    self.add_text("par(")

# depart_paragraph()
def depart_paragraph(self, node):
    self.add_text(")\n")
```

**Why `par()` is necessary:**
- Code mode doesn't auto-recognize paragraph breaks from blank lines
- Without `par()`, consecutive text blocks merge into single paragraph
- `par()` explicitly marks each paragraph boundary

**Example output structure:**
```typst
#{
  heading(level: 1, text("Title"))

  par(text("First paragraph content."))

  par(text("Second paragraph with ") + emph(text("emphasis")) + text("."))

  par(text("Third paragraph."))
}
```

### Text Node Wrapping with `text()` Function

Wrap ALL text in `text()` function to avoid escaping issues:

```python
# visit_Text()
def visit_Text(self, node):
    text_content = node.astext()
    # Standard string escaping (order matters!)
    escaped = text_content.replace('\\', '\\\\')  # 1. Backslash first
    escaped = escaped.replace('"', '\\"')          # 2. Quotes
    escaped = escaped.replace('\n', '\\n')         # 3. Newlines
    escaped = escaped.replace('\r', '\\r')         # 4. Carriage returns
    escaped = escaped.replace('\t', '\\t')         # 5. Tabs
    # Unicode escapes typically not needed (UTF-8 source)
    self.add_text(f'text("{escaped}")')
```

**Why `text()` not `[...]`?**
- `text("...")` uses string mode → no need to escape `#`, `*`, `_`, `$`, `[`, `}`
- `[...]` uses markup mode → requires escaping special characters
- Example: `text("$100 #1")` works, `[$100 #1]` breaks

**Standard string escape sequences** (as per Typst specification):
- `\\` for backslash (MUST escape first to avoid double-escaping)
- `\"` for quote (unescaped quotes would close string early)
- `\n` for newline (literal newline would break string syntax)
- `\r` for carriage return
- `\t` for tab
- `\u{...}` for Unicode escape sequence (e.g., `\u{1f600}` for 😀)

**Note**: Unicode escapes typically not needed since source files are UTF-8.

**For concatenation** (within a paragraph):
```python
# Multiple text + formatting nodes inside par()
# Output: par(text("This is ") + emph(text("important")) + text(" text"))
# visit_paragraph() already added "par("
self.add_text('text("This is ") + ')
self.add_text('emph(text("important")) + ')
self.add_text('text(" text")')
# depart_paragraph() will add ")"
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

Convert code blocks to `raw()` function with backtick raw string literals:

```python
# Current (sugar syntax with codly)
def visit_literal_block(self, node):
    if not linenos:
        self.add_text("#codly(number-format: none)\n")
    if hl_lines:
        self.add_text(f"#codly-range(highlight: ({highlight_str}))\n")
    self.add_text(f"```{language}\n")

# Target (raw() function with codly and backtick raw strings)
def visit_literal_block(self, node):
    if not linenos:
        self.add_text("codly(number-format: none)\n")  # NO #
    if hl_lines:
        self.add_text(f"codly-range(highlight: ({highlight_str}))\n")  # NO #

    # Get code content
    code_content = node.astext()
    lang = node.get("language", "")

    # Detect if code contains backticks (minimum delimiter is 3)
    backtick_count = self._count_max_consecutive_backticks(code_content)
    delimiter_count = max(3, backtick_count + 1)  # Minimum 3, or max+1 if code has backticks
    delimiter = "`" * delimiter_count

    # Generate raw() function with backtick raw string (no escaping)
    if lang:
        self.add_text(f'raw(block: true, lang: "{lang}", {delimiter}{code_content}{delimiter})\n')
    else:
        self.add_text(f'raw(block: true, {delimiter}{code_content}{delimiter})\n')

def _count_max_consecutive_backticks(self, text):
    """Count the maximum consecutive backticks in text."""
    max_count = 0
    current_count = 0
    for char in text:
        if char == '`':
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0
    return max_count
```

**Codly compatibility**:
- Codly uses `show raw.where(block: true)` show rules
- `raw()` function integrates with codly's `raw.line` processing
- All features preserved: line numbers, highlighting, zebra striping, annotations

**Backtick raw strings for `raw()`**:
- Typst's lexer processes backticks as raw string literals (no escape processing)
- No escaping needed for `\"`, `\\`, `\n`, or any special characters
- Content preserved literally (quotes, backslashes, newlines)
- For code containing backticks, use 3+ backticks as delimiters (minimum 3)

### Inline Code with `raw()` Function

Convert inline code to `raw()` function with backtick raw strings:

```python
# Current
def visit_literal(self, node):
    self.add_text("`")

def depart_literal(self, node):
    self.add_text("`")

# Target
def visit_literal(self, node):
    code_content = node.astext()

    # Detect if code contains backticks (minimum delimiter is 3)
    backtick_count = self._count_max_consecutive_backticks(code_content)
    delimiter_count = max(3, backtick_count + 1)  # Minimum 3, or max+1 if code has backticks
    delimiter = "`" * delimiter_count

    # Generate raw() with backtick raw string (no escaping)
    self.add_text(f'raw({delimiter}{code_content}{delimiter})')
    raise nodes.SkipNode  # Don't process children
```

**Why backtick raw strings for `raw()`?**
- Typst's lexer processes backticks as raw string literals (no escape processing)
- No escaping needed for quotes, backslashes, newlines, or special characters
- For code containing backticks, dynamically determine delimiter length

### Toctree with `include()` Function

Remove nested code mode block and `#` prefixes from toctree:

```python
# Current (nested content block with # prefixes)
def visit_toctree(self, node):
    entries = node.get("entries", [])

    # Generate nested content block
    self.add_text("#[\n")
    self.add_text("  #set heading(offset: 1)\n")

    for _title, docname in entries:
        relative_path = self._compute_relative_include_path(docname, current_docname)
        self.add_text(f'  #include("{relative_path}.typ")\n')

    self.add_text("]\n\n")
    raise nodes.SkipNode

# Target (KEEP nested content block for scope isolation)
def visit_toctree(self, node):
    entries = node.get("entries", [])

    # KEEP nested #[...] content block for scope isolation
    # #[...] creates isolated scope for set rules
    self.add_text("#[\n")
    self.add_text("  #set heading(offset: 1)\n")  # KEEP # prefix

    for _title, docname in entries:
        relative_path = self._compute_relative_include_path(docname, current_docname)
        self.add_text(f'  #include("{relative_path}.typ")\n')  # KEEP # prefix

    self.add_text("]\n\n")
    raise nodes.SkipNode
```

**Key points**:
- **KEEP nested `#[...]` content block** for scope isolation
- **KEEP `#` prefix** on `set` and `include()` (required in content blocks)
- Content block prevents `set` rules from leaking to rest of document
- Without content block, ALL subsequent headings would be affected by offset

**Why keep nested content block?**
- Creates isolated scope for `set heading(offset: 1)`
- Prevents offset from affecting headings after toctree
- `#[...]` = content block (different from `#{...}` code block)
- Inside content blocks, `#` prefix is required for statements

**No changes needed** - current implementation is already correct!

### Definition Lists with `terms.item()` Function

Convert definition lists to `terms()` with `terms.item()`:

```python
# Current (incremental)
def visit_term(self, node):
    self.add_text("/ ")

def depart_term(self, node):
    self.add_text(": ")

def visit_definition(self, node):
    pass

def depart_definition(self, node):
    self.add_text("\n")

# Target (collection-based)
def visit_definition_list(self, node):
    # Collect all term-definition pairs
    items = []
    for item in node.children:
        if isinstance(item, nodes.definition_list_item):
            term = item.children[0].astext()  # term node
            definition = item.children[1].astext()  # definition node
            term_escaped = term.replace('"', '\\"')
            def_escaped = definition.replace('"', '\\"')
            items.append(f'terms.item(text("{term_escaped}"), text("{def_escaped}"))')

    # Generate terms() with all items
    self.add_text(f"terms({', '.join(items)})\n")
    raise nodes.SkipNode

# Note: Actual implementation needs to handle complex content in definitions
# (emphasis, strong, etc.) using content collection, not just astext()
```

**Key points**:
- `terms()` function wraps all `terms.item()` calls
- Each term-definition pair becomes `terms.item(text("term"), text("def"))`
- NO `#` prefix
- Requires state redesign similar to lists

### Math with Backtick Raw Strings

Convert math to use backtick raw strings (avoid escaping backslashes):

```python
# Current (with # prefix)
def visit_math(self, node):
    """Inline math"""
    math_content = node.astext()
    use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

    if use_mitex:
        self.add_text(f"#mi(`{math_content}`)")  # WITH # - inline
    else:
        self.add_text(f"${math_content}$")

def visit_math_block(self, node):
    """Block math"""
    math_content = node.astext()
    use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

    if use_mitex:
        self.add_text(f"#mitex(`{math_content}`)")  # WITH # - block
    else:
        self.add_text(f"$ {math_content} $")

# Target (without # prefix)
def visit_math(self, node):
    """Inline math"""
    math_content = node.astext()
    use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

    if use_mitex:
        self.add_text(f"mi(`{math_content}`)")  # NO # prefix - inline
    else:
        self.add_text(f"${math_content}$")  # $ syntax works in code mode

def visit_math_block(self, node):
    """Block math"""
    math_content = node.astext()
    use_mitex = getattr(self.builder.config, "typst_use_mitex", True)

    if use_mitex:
        self.add_text(f"mitex(`{math_content}`)")  # NO # prefix - block
    else:
        self.add_text(f"$ {math_content} $")  # $ syntax works in code mode
```

**Why backticks for `mi()` and `mitex()`?**
- LaTeX math contains many backslashes: `\frac`, `\sum`, `\int`, etc.
- Backtick raw strings: `` mi(`\frac{a}{b}`) `` (no escaping needed)
- String escaping: `mi("\\frac{a}{b}")` (all backslashes must be doubled)
- **Backticks are much cleaner** and match current implementation

**Example comparison**:
```python
# Inline math with backticks (recommended)
mi(`\frac{d}{dx} \sum_{i=1}^{n} x_i^2`)

# Block math with backticks (recommended)
mitex(`\int_0^1 f(x) dx`)

# With string escaping (verbose - NOT recommended)
mi("\\frac{d}{dx} \\sum_{i=1}^{n} x_i^2")
mitex("\\int_0^1 f(x) dx")
```

**Note**: Typst native math `$...$` works directly in code mode without any changes.

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
