# Spec Delta: Empty Cell Handling

## MODIFIED Requirements

### Requirement: Unified Code Mode準拠のセル出力

テーブルセルの出力は、Unified Code Mode指針に従い、**すべてのセル（空白セルを含む）をcontent型のブロック `{}` で囲まなければならない** (MUST)。これによりTypstの型システムに準拠し、空白セルでもコンパイルエラーが発生しないことを保証する。

**Change**: Added requirement for empty cell handling with content blocks.

#### Scenario: 空白セルのcontent型出力

- **GIVEN** content が空文字列のテーブルセル
- **WHEN** Typst形式に変換する
- **THEN** 出力は `{},` を含む
- **AND** マークアップモード `[...]` でラップされない
- **AND** Typst コンパイルが成功する

**Rationale**: Typst の `table()` 関数は各セルが `content` 型であることを要求する。空白セルでも `{}` （空のcontent block）として出力する必要がある。

#### Scenario: 通常セルのcontent型ブロック出力

- **GIVEN** colspan/rowspanを持たない通常のテーブルセル
- **AND** セル内容が`par({text("Cell 1")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`{par({text("Cell 1")})},`を含む
- **AND** content型が `{}` でラップされる
- **AND** マークアップモード `[...]` でラップされない

**Change**: Clarified that normal cells must also be wrapped in content blocks.

**Rationale**: すべてのセルを統一的に content block で囲むことで、Typst の型システムに準拠し、空白セルの特殊処理を不要にする。

#### Scenario: spanningセルのcontent型第1引数

- **GIVEN** `morecols=1`を持つセル
- **AND** セル内容が`par({text("Spans 2 cols")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell({par({text("Spans 2 cols")})}, colspan: 2),`を含む
- **AND** content型が第1引数として渡される

**Change**: No change - spanning cells already use `table.cell()` which accepts content type.

**Rationale**: Typst公式の`table.cell(body, colspan: 1, rowspan: 1)`シグネチャに従う。body は content 型。

#### Scenario: 空白colspanセルのcontent型出力

- **GIVEN** `morecols=1`を持つ空白セル（2列に跨る）
- **AND** セル内容が空文字列
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell({}, colspan: 2),`を含む
- **AND** 空のcontent block `{}` が第1引数として渡される
- **AND** Typst コンパイルが成功する

**Change**: New scenario for empty colspan cells.

**Rationale**: 水平結合セルでも空白の場合は `{}` を出力する必要がある。

#### Scenario: 空白rowspanセルのcontent型出力

- **GIVEN** `morerows=1`を持つ空白セル（2行に跨る）
- **AND** セル内容が空文字列
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell({}, rowspan: 2),`を含む
- **AND** 空のcontent block `{}` が第1引数として渡される
- **AND** Typst コンパイルが成功する

**Change**: New scenario for empty rowspan cells.

**Rationale**: 垂直結合セルでも空白の場合は `{}` を出力する必要がある。

#### Scenario: 空白colspan+rowspanセルのcontent型出力

- **GIVEN** `morecols=1`と`morerows=1`を持つ空白セル（2列×2行に跨る）
- **AND** セル内容が空文字列
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell({}, colspan: 2, rowspan: 2),`を含む
- **AND** 空のcontent block `{}` が第1引数として渡される
- **AND** Typst コンパイルが成功する

**Change**: New scenario for empty cells with both colspan and rowspan.

**Rationale**: 複合結合セル（水平＋垂直）でも空白の場合は `{}` を出力する必要がある。これは最も複雑なケースで、すべての結合パターンをカバーする。

#### Scenario: ヘッダーセルのcontent型ブロック出力

- **GIVEN** `thead`内のヘッダーセル
- **AND** セル内容が`par({text("Header")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.header({par({text("Header")})}, ...)`を含む
- **AND** content型が `{}` でラップされる
- **AND** マークアップモード `[...]` でラップされない

**Change**: Clarified that header cells are also wrapped in content blocks.

**Rationale**: ヘッダーセルも通常セルと同様にUnified Code Mode指針に従い、content block で囲む。

#### Scenario: 空白ヘッダーセルのcontent型出力

- **GIVEN** `thead`内の空白ヘッダーセル
- **AND** セル内容が空文字列
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.header({}, ...)`を含む
- **AND** 空のcontent block `{}` が出力される
- **AND** Typst コンパイルが成功する

**Change**: New scenario for empty header cells.

**Rationale**: ヘッダーセルでも空白の場合は `{}` を出力する必要がある。

#### Scenario: 複雑な内容のセルcontent型ブロック出力

- **GIVEN** 複数の要素を含むセル（例: `text("A") + strong({text("B")})`）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`{text("A") + strong({text("B")})},`を含む
- **AND** content型の式が `{}` でラップされる
- **AND** マークアップモードでラップされない

**Change**: Clarified that complex content is also wrapped in content blocks.

**Rationale**: 任意のcontent型式を content block で囲むことで、Typst の型システムに準拠する。

#### Scenario: 混合セル（空白と非空白）のテーブル出力

- **GIVEN** 同一テーブル内に空白セルと非空白セルが混在する
- **AND** 一部のセルは `par({text("Data")})` を含む
- **AND** 一部のセルは空文字列
- **WHEN** Typst形式に変換する
- **THEN** すべての非空白セルは `{par({text("Data")})},` として出力される
- **AND** すべての空白セルは `{},` として出力される
- **AND** Typst コンパイルが成功する

**Change**: New scenario for mixed empty and non-empty cells.

**Rationale**: 実際のユースケースでは空白セルと非空白セルが混在することが多い。両方が正しく処理されることを保証する。

## Implementation Notes

### Code Changes

**File**: `typsphinx/translator.py`

**Method**: `_format_table_cell()` (lines 1201-1228)

**Change**:
```python
# Before (line 1218):
return f"{indent}{content},\n"

# After:
return f"{indent}{{{content}}},\n"
```

**Rationale**:
- Wraps all normal cells (no spanning) in content blocks `{}`
- Empty cells become `{},` instead of `,`
- Non-empty cells become `{par({text("...")})},` instead of `par({text("...")})` ,`
- Aligns with Typst's type system requirement for table cells

**Note**: Spanning cells using `table.cell()` already pass content as the first argument, so no changes needed:
```python
# Line 1228 - already correct:
return f"{indent}table.cell({content}, {params_str}),\n"
```

### Test Coverage

**New Tests** (`tests/test_translator.py`):

1. `test_table_empty_cells()`: Table with only empty cells
2. `test_table_mixed_empty_and_content()`: Table with mixed empty and non-empty cells
3. `test_table_empty_spanning_cells()`: Empty cells with colspan/rowspan
4. `test_table_empty_header_cells()`: Empty header cells

**Existing Tests** (must pass):
- `test_table_conversion()`
- `test_table_cell_colspan()`
- `test_table_cell_rowspan()`
- `test_table_header_wrapping()`
- All other table-related tests

### Validation

**Manual Test**:
```python
# Create table with empty cells
table = nodes.table()
tgroup = nodes.tgroup(cols=2)
tbody = nodes.tbody()

row1 = nodes.row()
entry1 = nodes.entry()
entry1 += nodes.paragraph(text="A")
row1 += entry1
entry2 = nodes.entry()  # Empty cell
row1 += entry2
tbody += row1

# Verify output contains {} for empty cells
output = translator.astext()
assert "{}" in output
assert ",," not in output  # No bare commas
```

**Typst Compilation**:
```bash
# Generated Typst should compile without errors
typst compile output.typ
```

## Migration Notes

**Backwards Compatibility**: ✓ Fully compatible

- Existing non-empty cells: Still work correctly (content is wrapped in `{}`)
- Existing empty cells: Now work correctly (was broken before)
- Existing spanning cells: No change (already use `table.cell()`)
- No breaking changes to API or output format (structural change only)

**User Impact**: Positive only

- Users with empty cells: Tables now compile successfully
- Users without empty cells: No visible change (content just wrapped in `{}`)
