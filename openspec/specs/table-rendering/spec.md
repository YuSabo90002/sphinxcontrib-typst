# Spec: テーブルレンダリング

## Purpose

reStructuredTextのすべてのテーブル形式（list-table、grid table、simple table、csv-table）をTypst形式の`#table()`構造に正しく変換する機能を定義します。
## Requirements
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

### Requirement: テーブルのTypst変換

reStructuredTextのテーブル形式をTypst形式の`#table()`構造に変換する機能を提供しなければならない (MUST)。

#### Scenario: list-tableディレクティブの変換

- **GIVEN** 2列2行の`list-table`ディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造を含む

#### Scenario: grid table形式の変換

- **GIVEN** 2列2行のgrid table（ASCIIアート罫線形式）
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造を含む

#### Scenario: simple table形式の変換

- **GIVEN** 2列2行のsimple table形式
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造を含む

#### Scenario: csv-tableディレクティブの変換

- **GIVEN** 2列2行の`csv-table`ディレクティブ
- **WHEN** Typst形式に変換する
- **THEN** 出力は`#table(columns: 2, ...)`構造を含む

#### Scenario: ヘッダー行を持つテーブルの変換

- **GIVEN** ヘッダー行を持つ任意のテーブル形式
- **WHEN** Typst形式に変換する
- **THEN** ヘッダー行のセルも`#table()`内で出力される

#### Scenario: 複数行のテーブルの変換

- **GIVEN** 4列5行の任意のテーブル形式
- **AND** 各セルにテキストコンテンツが含まれる
- **WHEN** Typst形式に変換する
- **THEN** すべてのセルの内容が`#table()`構造内で出力される

#### Scenario: 全テーブル形式のサポート

- **GIVEN** 同一ドキュメント内にlist-table、grid table、simple table、csv-tableの4種類すべてが存在する
- **WHEN** Typst形式に変換する
- **THEN** すべてのテーブル形式で`#table()`構造が生成される

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

