# Specification: Document Conversion - Unified Function Approach

## Overview

This specification defines the requirements for converting all Typst sugar syntax to canonical function call syntax in sphinx-typst translator, establishing a unified function-based architecture.

---

## MODIFIED Requirements

### Requirement: 見出しの変換

見出しノードは Typst の `#heading()` 関数として出力されなければならない (MUST)。Sugar syntax (`=`, `==`, `===`, etc.) による出力は使用してはならない (MUST NOT)。

**Rationale**: Explicit function calls provide clear 1:1 mapping between visitor methods and Typst functions, improving maintainability and eliminating ambiguity.

#### Scenario: 第1レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 1 heading "Introduction"
WHEN the translator processes the title node at section_level=1
THEN the output MUST be `#heading(level: 1)[Introduction]`
AND NOT `= Introduction`
```

#### Scenario: 第2レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 2 heading "Background"
WHEN the translator processes the title node at section_level=2
THEN the output MUST be `#heading(level: 2)[Background]`
AND NOT `== Background`
```

#### Scenario: 第6レベル見出しの変換

```gherkin
GIVEN a Sphinx document with a level 6 heading "Details"
WHEN the translator processes the title node at section_level=6
THEN the output MUST be `#heading(level: 6)[Details]`
AND NOT `====== Details`
```

---

### Requirement: 強調と太字の変換

強調ノードは `#emph[]` として、太字ノードは `#strong[]` として出力されなければならない (MUST)。Sugar syntax (`_text_`, `*text*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Function syntax eliminates syntax errors from nested combinations like `*_text_*` (Issue #55) and provides consistent, robust behavior.

#### Scenario: 強調テキストの変換

```gherkin
GIVEN a Sphinx document with emphasis text "important"
WHEN the translator processes an emphasis node
THEN the output MUST be `#emph[important]`
AND NOT `_important_`
```

#### Scenario: 太字テキストの変換

```gherkin
GIVEN a Sphinx document with strong text "critical"
WHEN the translator processes a strong node
THEN the output MUST be `#strong[critical]`
AND NOT `*critical*`
```

#### Scenario: 強調と太字のネスト

```gherkin
GIVEN a Sphinx document with nested strong and emphasis nodes
WHEN the translator processes strong node containing emphasis node "nested"
THEN the output MUST be `#strong[#emph[nested]]`
AND NOT `*_nested_*` (which causes unclosed delimiter errors)
```

#### Scenario: アンダースコアを含む太字テキスト

```gherkin
GIVEN a Sphinx document with strong text "file_name.txt"
WHEN the translator processes a strong node
THEN the output MUST be `#strong[file_name.txt]`
AND NOT `*file_name.txt*` (which causes unclosed delimiter errors due to `_`)
```

---

### Requirement: リストの変換

箇条書きリストは `#list()` 関数として、番号付きリストは `#enum()` 関数として出力されなければならない (MUST)。Sugar syntax (`- item`, `+ item`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Function-based list generation enables proper item collection and supports complex nested structures without fragile incremental syntax building.

#### Scenario: 単純な箇条書きリスト

```gherkin
GIVEN a Sphinx document with a bullet list containing 3 items
WHEN the translator processes the bullet_list node
THEN the output MUST be `#list([item 1], [item 2], [item 3])`
AND NOT:
  - item 1
  - item 2
  - item 3
```

#### Scenario: 単純な番号付きリスト

```gherkin
GIVEN a Sphinx document with an enumerated list containing 3 items
WHEN the translator processes the enumerated_list node
THEN the output MUST be `#enum([item 1], [item 2], [item 3])`
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
THEN the output MUST use `#list()` for outer list and `#enum()` for inner list
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

サブタイトルノードは `#emph[]` 関数として出力されなければならない (MUST)。Sugar syntax (`_subtitle_`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Subtitle semantics map to emphasis in Typst. Using `#emph[]` ensures consistency with other emphasis elements.

#### Scenario: サブタイトルの変換

```gherkin
GIVEN a Sphinx document with a subtitle "A Comprehensive Guide"
WHEN the translator processes a subtitle node
THEN the output MUST be `#emph[A Comprehensive Guide]`
AND NOT `_A Comprehensive Guide_`
```

#### Scenario: サブタイトル内の特殊文字

```gherkin
GIVEN a subtitle containing special characters "Version 1.0 - Beta"
WHEN the translator processes the subtitle node
THEN the output MUST be `#emph[Version 1.0 - Beta]`
AND special characters MUST be preserved correctly
```

---

### Requirement: APIドキュメントのフィールド名変換

APIドキュメント内のフィールド名は `#strong[]` 関数として出力されなければならない (MUST)。Sugar syntax (`*name*`) による出力は使用してはならない (MUST NOT)。

**Rationale**: Consistency with the unified function approach requires all strong formatting to use `#strong[]`, including field names in API documentation.

#### Scenario: Parameters フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Parameters"
WHEN the translator processes the field_name node
THEN the output MUST be `#strong[Parameters:]`
AND NOT `*Parameters:*`
```

#### Scenario: Returns フィールド名の変換

```gherkin
GIVEN an API documentation field with name "Returns"
WHEN the translator processes the field_name node
THEN the output MUST be `#strong[Returns:]`
AND NOT `*Returns:*`
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

1. **No Sugar Syntax in Output** (except Typst standard)
   - MUST NOT generate `=`, `_`, `*` for headings, emphasis, strong
   - MUST NOT generate `-`, `+` for lists
   - MAY generate `` ` ``, ` ``` `, `/ `, `$` (Typst standard)

2. **All Function Calls Well-Formed**
   - MUST generate `#heading(level: N)[...]`
   - MUST generate `#emph[...]`, `#strong[...]`
   - MUST generate `#list([...], [...])`, `#enum([...], [...])`

3. **Nested Elements Properly Handled**
   - MUST support `#strong[#emph[nested]]`
   - MUST support `#list([#emph[item]], [#strong[item]])`
   - MUST NOT generate malformed syntax combinations

4. **PDF Output Unchanged**
   - Generated PDFs MUST be visually identical to previous versions
   - Only source `.typ` format changes, not compiled output

---

## Implementation Notes

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
    self.add_text(f"#list({', '.join(f'[{item}]' for item in items)})")
```

### Heading Level Parameter

Heading level must be passed as parameter:

```python
# Current
heading_prefix = "=" * self.section_level

# Target
self.add_text(f"#heading(level: {self.section_level})[")
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
