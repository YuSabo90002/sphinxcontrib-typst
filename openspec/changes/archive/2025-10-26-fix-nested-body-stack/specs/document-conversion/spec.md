# Spec: ドキュメント変換

## MODIFIED Requirements

### Requirement: リストのストリームベースレンダリング

トランスレータは、リスト（bullet list、enumerated list）を処理する際、`self.body`を置き換えずにストリームベースで出力しなければならない (MUST)。リスト項目間の区切り（カンマ）と項目内要素間の結合（`+`演算子）は、状態フラグを使用して制御する。

#### Scenario: 単一リストの基本出力

- **GIVEN** 2つの項目を持つ単純なbullet list
  ```rst
  - First item
  - Second item
  ```
- **WHEN** `visit_bullet_list()`が呼び出される
- **THEN** `list(`が`self.body`に追加される
- **AND** `self.is_first_list_item`が`True`に設定される
- **WHEN** 最初の`visit_list_item()`が呼び出される
- **THEN** カンマは追加されない（最初の項目なので）
- **AND** `self.is_first_list_item`が`False`に設定される
- **WHEN** 2番目の`visit_list_item()`が呼び出される
- **THEN** `, `が`self.body`に追加される（2番目以降の項目なので）
- **WHEN** `depart_bullet_list()`が呼び出される
- **THEN** `)\n\n`が`self.body`に追加される
- **AND** 最終出力は`list(text("First item"), text("Second item"))\n\n`である

#### Scenario: リスト項目内の要素間結合

- **GIVEN** 複数要素を持つリスト項目
  ```rst
  - Item with **bold** and *emphasis*
  ```
- **WHEN** `visit_list_item()`が呼び出される
- **THEN** `self.list_item_needs_separator`が`False`に設定される
- **WHEN** 最初の`visit_Text()`が呼び出される
- **THEN** `+`は追加されない（最初の要素なので）
- **AND** `self.list_item_needs_separator`が`True`に設定される
- **WHEN** 2番目の要素（`visit_strong()`）が呼び出される
- **THEN** ` + `が`self.body`に追加される（2番目以降の要素なので）
- **AND** 最終出力は`text("Item with ") + strong(text("bold")) + text(" and ") + emph(text("emphasis"))`である

#### Scenario: ネストされたリストの処理

- **GIVEN** 2レベルのネストされたリスト
  ```rst
  - Outer item 1
  - Outer item 2

    - Inner item 1
    - Inner item 2
  ```
- **WHEN** 外側の`visit_bullet_list()`が呼び出される
- **THEN** `list(`が追加され、`is_first_list_item = True`
- **WHEN** 外側の2番目のlist item内で内側の`visit_bullet_list()`が呼び出される
- **THEN** ` + list(`が追加される（項目内の2番目の要素として）
- **AND** 内側のリストは独自の`is_first_list_item`状態を持つ
- **AND** 外側の`self.body`は置き換えられない（ストリーム出力）
- **AND** 最終出力は`list(text("Outer item 1"), text("Outer item 2") + list(text("Inner item 1"), text("Inner item 2")))`である

#### Scenario: ドキュメントラッパーの保持

- **GIVEN** リストを含む任意のドキュメント
- **WHEN** `visit_document()`が`#{\n`を`self.body`に追加する
- **AND** リスト処理が実行される
- **THEN** `self.body`は決して置き換えられない
- **AND** `#{\n`は`self.body`の最初の要素として保持される
- **AND** 最終出力は`#{`で始まり`}\n`で終わる

#### Scenario: 複雑なリスト項目（複数段落）

- **GIVEN** 複数段落を含むリスト項目
  ```rst
  - First paragraph in item

    Second paragraph in item
  ```
- **WHEN** リスト項目が処理される
- **THEN** 2つの段落は`+`で結合される
- **AND** 出力は`text("First paragraph in item") + text("\n\nSecond paragraph in item")`である

### Requirement: ボディ置き換えの禁止

トランスレータは、`self.body`を一時的な他のリストに置き換えてはならない (MUST NOT)。すべての出力は`self.body`に直接追加し、状態フラグで制御する。

#### Scenario: リスト処理でのボディ保持

- **GIVEN** 任意のリスト処理
- **WHEN** `visit_list_item()`が呼び出される
- **THEN** `self.body`は置き換えられない
- **AND** `self.saved_body`や`self.current_list_item_buffer`は使用されない
- **AND** すべての出力は`self.body.append()`経由で`self.body`に直接追加される

#### Scenario: 定義リスト処理でのボディ保持

- **GIVEN** 任意の定義リスト処理
- **WHEN** `visit_term()`または`visit_definition()`が呼び出される
- **THEN** `self.body`は置き換えられない
- **AND** すべての出力は`self.body`に直接追加される

### Requirement: 状態フラグによる区切り制御

トランスレータは、リスト項目間の区切り（カンマ）と項目内要素間の結合（`+`）を状態フラグで制御しなければならない (MUST)。

#### Scenario: is_first_list_itemフラグの管理

- **GIVEN** bullet listまたはenumerated list
- **WHEN** `visit_bullet_list()`が呼び出される
- **THEN** `self.is_first_list_item = True`が設定される
- **WHEN** 最初の`visit_list_item()`が呼び出される
- **THEN** `self.is_first_list_item`が`True`なのでカンマは追加されない
- **AND** `self.is_first_list_item = False`が設定される
- **WHEN** 2番目の`visit_list_item()`が呼び出される
- **THEN** `self.is_first_list_item`が`False`なのでカンマが追加される

#### Scenario: list_item_needs_separatorフラグの管理

- **GIVEN** リスト項目内の複数要素
- **WHEN** `visit_list_item()`が呼び出される
- **THEN** `self.list_item_needs_separator = False`が設定される
- **WHEN** 最初の要素が処理される
- **THEN** `+`は追加されない
- **AND** `self.list_item_needs_separator = True`が設定される
- **WHEN** 2番目の要素が処理される
- **THEN** ` + `が追加される

## REMOVED Requirements

### Requirement: ボディスタックのバランス保証

（削除：ボディを置き換えないため、スタック管理は不要）

### Requirement: ネストされた要素におけるボディ管理

（削除：ストリームベースアプローチでは、ボディのスタック管理は不要）
