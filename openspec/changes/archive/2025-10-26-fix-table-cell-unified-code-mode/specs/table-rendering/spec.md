# Spec Delta: table-rendering

## MODIFIED Requirements

### Requirement: セル結合のサポート

テーブルセルの水平結合（colspan）と垂直結合（rowspan）をサポートしなければならない (MUST)。docutilsの`morecols`と`morerows`属性を読み取り、Typstの`table.cell()`構文に変換する。

#### Scenario: 水平結合セルの変換

- **GIVEN** `morecols=1`属性を持つテーブルセル（2列分）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(content, colspan: 2)`を含む
- **AND** 通常セルは`content`として出力される（マークアップモード `[...]` なし）

**変更理由**: Unified Code Mode指針に従い、マークアップモード `[...]` を使用せず、content型を直接渡す。`table.cell()`の第1引数はcontent型のbody。

#### Scenario: 垂直結合セルの変換

- **GIVEN** `morerows=1`属性を持つテーブルセル（2行分）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(content, rowspan: 2)`を含む

**変更理由**: `table.cell()`の引数順序を修正（content型を第1引数に）。

#### Scenario: 複合結合セルの変換

- **GIVEN** `morecols=1`と`morerows=1`属性を持つテーブルセル
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(content, colspan: 2, rowspan: 2)`を含む

**変更理由**: `table.cell()`の引数順序を修正。

#### Scenario: ヘッダー内の結合セルの変換

- **GIVEN** `thead`内に`morecols=1`属性を持つヘッダーセル
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.header(table.cell(content, colspan: 2), ...)`を含む
- **AND** ヘッダーセルと結合セルの両方の機能が正しく動作する

**変更理由**: `table.cell()`の引数順序を修正し、マークアップモードを削除。

#### Scenario: 複数の結合セルを持つテーブル

- **GIVEN** 同一テーブル内に複数の結合セルが存在する
- **WHEN** Typst形式に変換する
- **THEN** すべての結合セルが正しく`table.cell(content, ...)`でラップされる
- **AND** 通常セルは`content`として出力される（マークアップモードなし）

**変更理由**: 一貫性のため、すべてのセルでマークアップモードを削除。

#### Scenario: 結合のないテーブル（後方互換性）

- **GIVEN** `morecols`も`morerows`も持たないテーブル
- **WHEN** Typst形式に変換する
- **THEN** すべてのセルは`content`として出力される（マークアップモード `[...]` なし）
- **AND** `table.cell()`は生成されない（既存の動作を維持）

**変更理由**: Unified Code Mode指針に従い、マークアップモードを削除。

## ADDED Requirements

### Requirement: Unified Code Mode準拠のセル出力

テーブルセルの出力は、Unified Code Mode指針に従い、マークアップモード `[...]` を使用せず、content型を直接渡さなければならない (MUST)。

#### Scenario: 通常セルのcontent型出力

- **GIVEN** colspan/rowspanを持たない通常のテーブルセル
- **AND** セル内容が`par({text("Cell 1")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`par({text("Cell 1")}),`を含む
- **AND** マークアップモード `[...]` でラップされない

**理由**: Unified Code Mode指針の「マークアップモードを避ける」に従う。

#### Scenario: spanningセルのcontent型第1引数

- **GIVEN** `morecols=1`を持つセル
- **AND** セル内容が`par({text("Spans 2 cols")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(par({text("Spans 2 cols")}), colspan: 2),`を含む
- **AND** content型が第1引数として渡される

**理由**: Typst公式の`table.cell(body, colspan: 1, rowspan: 1)`シグネチャに従う。

#### Scenario: ヘッダーセルのcontent型出力

- **GIVEN** `thead`内のヘッダーセル
- **AND** セル内容が`par({text("Header")})`
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.header(par({text("Header")}), ...)`を含む
- **AND** マークアップモード `[...]` でラップされない

**理由**: ヘッダーセルも通常セルと同様にUnified Code Mode指針に従う。

#### Scenario: 複雑な内容のセル出力

- **GIVEN** 複数の要素を含むセル（例: `text("A") + strong({text("B")})`）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`text("A") + strong({text("B")}),`を含む
- **AND** マークアップモードでラップされない
- **AND** content型の式が直接渡される

**理由**: 任意のcontent型式を直接渡せることを保証。
