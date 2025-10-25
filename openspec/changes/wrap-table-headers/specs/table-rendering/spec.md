# Spec Delta: table-rendering

## ADDED Requirements

### Requirement: テーブルヘッダーのtable.header()ラッピング

テーブルヘッダー行（docutilsの`thead`ノード内のセル）は、Typst出力において`table.header()`でラップされなければならない (MUST)。これにより、ページ区切り時の自動ヘッダー繰り返しとアクセシビリティメタデータの付与を可能にする。

#### Scenario: grid tableのヘッダー変換

- **GIVEN** `=`区切りでヘッダーを定義したgrid table
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: N, table.header([Header 1], [Header 2], ...), ...)`構造を含む
- **AND** ヘッダーセルは`table.header()`内に配置される
- **AND** ボディセルは`table.header()`の外に配置される

#### Scenario: list-tableのheader-rowsオプション変換

- **GIVEN** `:header-rows: 1`オプション付きのlist-tableディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 最初の行のセルが`table.header()`内に配置される
- **AND** 残りの行のセルは`table.header()`の外に配置される

#### Scenario: simple tableのヘッダー変換

- **GIVEN** 上部に`=`区切りでヘッダーを定義したsimple table
- **WHEN** Typst形式に変換する
- **THEN** ヘッダー行のセルが`table.header()`内に配置される
- **AND** ボディ行のセルは`table.header()`の外に配置される

#### Scenario: csv-tableのheaderオプション変換

- **GIVEN** `:header:`オプション付きのcsv-tableディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** ヘッダー行として指定されたセルが`table.header()`内に配置される

#### Scenario: ヘッダーのないテーブル

- **GIVEN** ヘッダー行を持たないテーブル（grid table、list table、simple table、csv-tableのいずれか）
- **WHEN** Typst形式に変換する
- **THEN** `table.header()`は生成されない
- **AND** すべてのセルは通常のテーブルセルとして出力される
- **AND** 既存の動作を維持する（後方互換性）

#### Scenario: 複数行ヘッダーの変換

- **GIVEN** `:header-rows: 2`オプション付きのlist-tableディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 最初の2行のすべてのセルが単一の`table.header()`内に配置される
- **AND** 3行目以降のセルは`table.header()`の外に配置される

### Requirement: ヘッダー/ボディセルの状態追跡

translatorは、現在処理中のセルがテーブルヘッダー（`thead`）に属するかボディ（`tbody`）に属するかを追跡しなければならない (MUST)。

#### Scenario: thead訪問時の状態設定

- **GIVEN** docutilsの`thead`ノードを訪問する
- **WHEN** `visit_thead()`が呼び出される
- **THEN** translator内部の`in_thead`フラグが`True`に設定される

#### Scenario: thead離脱時の状態リセット

- **GIVEN** docutilsの`thead`ノードから離脱する
- **WHEN** `depart_thead()`が呼び出される
- **THEN** translator内部の`in_thead`フラグが`False`に設定される

#### Scenario: ヘッダーセルの保存

- **GIVEN** `in_thead`が`True`の状態でテーブルセル（`entry`ノード）を処理する
- **WHEN** `depart_entry()`が呼び出される
- **THEN** セルデータは`is_header: True`フラグとともに保存される

#### Scenario: ボディセルの保存

- **GIVEN** `in_thead`が`False`の状態でテーブルセル（`entry`ノード）を処理する
- **WHEN** `depart_entry()`が呼び出される
- **THEN** セルデータは`is_header: False`フラグとともに保存される

## MODIFIED Requirements

なし

## REMOVED Requirements

なし
