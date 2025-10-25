# Spec Delta: table-rendering

## ADDED Requirements

### Requirement: セル結合のサポート

テーブルセルの水平結合（colspan）と垂直結合（rowspan）をサポートしなければならない (MUST)。docutilsの`morecols`と`morerows`属性を読み取り、Typstの`table.cell()`構文に変換する。

#### Scenario: 水平結合セルの変換

- **GIVEN** `morecols=1`属性を持つテーブルセル（2列分）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(colspan: 2)[content]`を含む
- **AND** 通常セルは`[content]`として出力される

#### Scenario: 垂直結合セルの変換

- **GIVEN** `morerows=1`属性を持つテーブルセル（2行分）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(rowspan: 2)[content]`を含む

#### Scenario: 複合結合セルの変換

- **GIVEN** `morecols=1`と`morerows=1`属性を持つテーブルセル
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.cell(colspan: 2, rowspan: 2)[content]`を含む

#### Scenario: ヘッダー内の結合セルの変換

- **GIVEN** `thead`内に`morecols=1`属性を持つヘッダーセル
- **WHEN** Typst形式に変換する
- **THEN** 出力は`table.header(table.cell(colspan: 2)[Header], ...)`を含む
- **AND** ヘッダーセルと結合セルの両方の機能が正しく動作する

#### Scenario: 複数の結合セルを持つテーブル

- **GIVEN** 同一テーブル内に複数の結合セルが存在する
- **WHEN** Typst形式に変換する
- **THEN** すべての結合セルが正しく`table.cell()`でラップされる
- **AND** 通常セルは`[content]`として出力される

#### Scenario: 結合のないテーブル（後方互換性）

- **GIVEN** `morecols`も`morerows`も持たないテーブル
- **WHEN** Typst形式に変換する
- **THEN** すべてのセルは`[content]`として出力される
- **AND** `table.cell()`は生成されない（既存の動作を維持）

### Requirement: セル結合情報の保存

translatorは、各セルの結合情報（colspan、rowspan）を保存しなければならない (MUST)。

#### Scenario: セル結合属性の読み取り

- **GIVEN** `morecols`または`morerows`属性を持つ`entry`ノード
- **WHEN** `visit_entry()`が呼び出される
- **THEN** `morecols`値を読み取る（デフォルト0）
- **AND** `morerows`値を読み取る（デフォルト0）

#### Scenario: colspan/rowspanへの変換

- **GIVEN** `morecols=1`と`morerows=2`を持つセル
- **WHEN** セルデータを保存する
- **THEN** `colspan = morecols + 1 = 2`として計算される
- **AND** `rowspan = morerows + 1 = 3`として計算される

#### Scenario: セル辞書への結合情報の追加

- **GIVEN** セルの処理が完了した
- **WHEN** `depart_entry()`が呼び出される
- **THEN** セルデータは`{"content": str, "is_header": bool, "colspan": int, "rowspan": int}`形式で保存される
- **AND** 結合のないセルは`colspan=1, rowspan=1`として保存される

## MODIFIED Requirements

なし

## REMOVED Requirements

なし
