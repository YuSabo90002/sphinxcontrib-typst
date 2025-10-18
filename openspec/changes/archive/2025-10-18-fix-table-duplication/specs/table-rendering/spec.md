# Spec: テーブルレンダリング

## MODIFIED Requirements

### Requirement: テーブルセルのテキスト収集

テーブル内のテキストノードは、通常の出力ボディではなく専用のセルコンテンツバッファに蓄積されなければならない (MUST)。これにより、テーブル構造の生成時に内容が重複しないことを保証する。

#### Scenario: テーブルセル内のテキストノード処理

- **GIVEN** 任意のreStructuredTextテーブル形式（list-table、grid table、simple table、csv-table）を含むドキュメント
- **AND** テーブルセル内にテキストノードが存在する
- **WHEN** `visit_Text()`が呼び出される
- **THEN** テキストは`self.table_cell_content`に追加される
- **AND** `self.body`には追加されない

#### Scenario: テーブル外のテキストノード処理

- **GIVEN** テーブル構造の外側にテキストノードが存在する
- **WHEN** `visit_Text()`が呼び出される
- **THEN** テキストは通常通り`self.body`に追加される
- **AND** `self.table_cell_content`には影響しない

#### Scenario: セル内容の取得

- **GIVEN** テーブルセルの処理が完了した
- **WHEN** `depart_entry()`が呼び出される
- **THEN** `table_cell_content`から蓄積されたテキストを取得する
- **AND** `node.astext()`は`table_cell_content`が空の場合のみフォールバックとして使用される

### Requirement: テーブル構造の非重複出力

Typst出力において、テーブルの内容は`#table()`構造としてのみ出力され、プレーンテキストとしての重複出力があってはならない (MUST NOT)。

#### Scenario: list-tableディレクティブの変換

- **GIVEN** 2列2行の`list-table`ディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造のみを含む
- **AND** テーブルの前にプレーンテキストのセル内容が出力されない

#### Scenario: grid table形式の変換

- **GIVEN** 2列2行のgrid table（ASCIIアート罫線形式）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造のみを含む
- **AND** テーブルの前にプレーンテキストのセル内容が出力されない

#### Scenario: simple table形式の変換

- **GIVEN** 2列2行のsimple table形式
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造のみを含む
- **AND** テーブルの前にプレーンテキストのセル内容が出力されない

#### Scenario: csv-tableディレクティブの変換

- **GIVEN** 2列2行の`csv-table`ディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造のみを含む
- **AND** テーブルの前にプレーンテキストのセル内容が出力されない

#### Scenario: ヘッダー行を持つテーブルの変換

- **GIVEN** ヘッダー行を持つ任意のテーブル形式（`:header-rows: 1`オプション付きlist-table、またはgrid/simple tableのヘッダー行）
- **WHEN** Typst形式に変換する
- **THEN** ヘッダー行のセルも`#table()`内でのみ出力される
- **AND** ヘッダー内容のプレーンテキスト重複がない

#### Scenario: 複数行の複雑なテーブルの変換

- **GIVEN** 4列5行の任意のテーブル形式（list-table、grid table、simple table、csv-tableのいずれか）
- **AND** 各セルにテキストコンテンツが含まれる
- **WHEN** Typst形式に変換する
- **THEN** すべてのセルの内容が`#table()`構造内にのみ出力される
- **AND** 20個すべてのセル内容について重複がない

#### Scenario: 全テーブル形式の統一的処理

- **GIVEN** 同一ドキュメント内にlist-table、grid table、simple table、csv-tableの4種類すべてが存在する
- **WHEN** Typst形式に変換する
- **THEN** すべてのテーブル形式で一貫して`#table()`構造のみが出力される
- **AND** いずれのテーブル形式でもプレーンテキストの重複が発生しない
