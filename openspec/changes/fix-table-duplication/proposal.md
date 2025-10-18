# 提案: テーブル内容の重複出力を修正

**Change ID:** `fix-table-duplication`
**ステータス:** 提案中
**作成日:** 2025-10-18
**関連Issue:** [#19](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/19)

## 概要

`list-table`ディレクティブを含むreStructuredTextドキュメントをTypst形式に変換する際、テーブルの内容が重複して出力される問題を修正します。現在、プレーンテキストと`#table()`構造の両方が生成され、ドキュメントが読めない状態になっています。

## 問題の詳細

### 影響を受けるテーブル形式

**すべてのreStructuredTextテーブル形式で重複問題が発生します:**

- ❌ **list-table** ディレクティブ
- ❌ **grid table** (ASCIIアート形式)
- ❌ **simple table** (シンプルな罫線形式)
- ❌ **csv-table** ディレクティブ

これらすべてが同じdocutilsノード構造（`table` → `entry` → `Text`）を使用しているため、同一の根本原因により重複が発生します。

### 現在の挙動

テーブルを含むドキュメントをビルドすると、セルの内容が2回出力されます:

1. 各セルが個別の段落としてプレーンテキスト表示される
2. その後、正しい`#table()`構造として表示される

**実際の出力例（不正）:**
```typst
Language

Type

Python

Dynamic

#table(
  columns: 2,
  [Language],
  [Type],
  [Python],
  [Dynamic],
)
```

**期待される出力:**
```typst
#table(
  columns: 2,
  [Language],
  [Type],
  [Python],
  [Dynamic],
)
```

### 影響範囲

- **影響を受けるコンポーネント:** `sphinxcontrib/typst/translator.py` (TypstTranslator クラス)
- **影響を受けるドキュメント:** **すべてのテーブル形式**を使用するドキュメント
  - list-table ディレクティブ
  - grid table (罫線形式)
  - simple table
  - csv-table ディレクティブ
- **症状:**
  - Typst出力が読みにくくなる
  - PDF生成時に誤った内容が表示される（セルの内容が2倍表示される）
  - ドキュメントのサイズが不必要に増加する
  - テーブルが多いドキュメントでは特に顕著な問題となる

## 根本原因

`sphinxcontrib/typst/translator.py`における処理フローの問題:

1. **192行目 (`visit_Text()`)**: `self.add_text()`を呼び出し、無条件に`self.body`に追加
2. **683行目 (`visit_entry()`)**: `self.table_cell_content = []`を作成するが、実際にはそこにテキストが蓄積されない
3. **700行目 (`depart_entry()`)**: `node.astext()`を使用してセルの内容を再度取得
4. **結果**: テキストが`self.body`（プレーン出力）と`node.astext()`経由の`#table()`の両方に含まれる

## 提案する解決策

テキスト収集メカニズムを変更し、テーブルセル内にいる場合は`table_cell_content`にテキストをルーティングします:

```python
def add_text(self, text: str) -> None:
    """Add text to the output body or table cell content."""
    if hasattr(self, "in_table") and self.in_table and hasattr(self, "table_cell_content"):
        self.table_cell_content.append(text)
    else:
        self.body.append(text)
```

### 動作の変更点

- テーブルセル内のテキスト → `table_cell_content`に蓄積
- テーブル外のテキスト → 従来通り`self.body`に追加
- `depart_entry()`は`node.astext()`の代わりに`table_cell_content`を使用

## 影響評価

### メリット

- テーブル内容の重複が解消される
- クリーンで読みやすいTypst出力が生成される
- PDF生成時の誤った表示が修正される

### リスク評価: 低

- 変更箇所が限定的（単一メソッドの修正）
- 既存のテーブル構造ロジックは保持される
- テーブルセル内のテキストルーティングのみに影響

### 後方互換性

- 出力形式が改善されるため、既存の動作に依存するコードには影響なし
- テーブル以外の要素には一切影響なし

## テスト戦略

1. **既存テストの実行**: `tests/test_translator.py`と`tests/test_integration_advanced.py`でリグレッションがないことを確認
2. **フィクスチャ検証**: `examples/advanced/chapter2.rst`（16-39行目）を使用して修正を検証
3. **新規テストケース追加**: **すべてのテーブル形式**で内容の非重複を明示的にテストするケースを追加
   - list-table ディレクティブ
   - grid table形式
   - simple table形式
   - csv-table ディレクティブ
4. **出力検証**: `_build/typst/chapter2.typ`がプレーンテキストなしで`#table()`のみを含むことを確認

## 検討した代替案

### 1. テーブル内のテキストノードをスキップ

**アプローチ:** `visit_Text()`でテーブル内の場合は処理をスキップ

**却下理由:**
- 複雑なセル内容（インラインマークアップ、数式など）が壊れる可能性がある
- テキスト収集の一貫性が失われる

### 2. ポストプロセスで重複を削除

**アプローチ:** 生成後に重複テキストを検出・削除

**却下理由:**
- ソースで修正するよりも脆弱
- パターンマッチングの誤検知リスクが高い
- パフォーマンス上のオーバーヘッド

### 3. テーブルビジターフローの再構築

**アプローチ:** テーブル処理全体のアーキテクチャを変更

**却下理由:**
- 変更範囲が大きく、リスクが高い
- 他の機能への影響が不明確
- 最小限の修正で解決可能

## 参考資料

- **Issue:** [#19 - Table content duplicated in Typst output](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/19)
- **ソース例:** `examples/advanced/chapter2.rst:16-39`
- **現在の出力:** `examples/advanced/_build/typst/chapter2.typ:21-85`
- **関連コード:** `sphinxcontrib/typst/translator.py:59,192,675-703`
