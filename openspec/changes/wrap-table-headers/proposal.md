# Proposal: Wrap Table Headers in table.header()

## Why

現在、reStructuredTextのテーブルヘッダー（docutilsの`thead`または grid tableの`=`区切りで定義）は、Typstに変換する際に`table.header()`でラップされていない。これにより、Typstの自動ヘッダー繰り返し機能（ページ区切り時）が動作せず、アクセシビリティメタデータも失われる。[Typstドキュメント](https://typst.app/docs/reference/model/table/)によれば、テーブルがページをまたがない場合でも、Typstがアクセシビリティメタデータを付与するためヘッダーは常に`table.header()`でラップすべきである。

## What Changes

- テーブルレンダリングを修正し、セルがヘッダー（`thead`）に属するかボディ（`tbody`）に属するかを追跡する
- Typst出力でヘッダーセルに対して`table.header()`ラッパーを生成する
- 複数行ヘッダー（`:header-rows: N`でN > 1）をサポートする
- ヘッダーのないテーブルに対する後方互換性を維持する

## Impact

- **影響を受ける仕様**: `table-rendering`
- **影響を受けるコード**:
  - `typsphinx/translator.py` (テーブル訪問メソッド: `visit_thead`, `depart_thead`, `visit_entry`, `depart_entry`, `depart_table`)
- **破壊的変更**: なし - 既存のテーブル出力の拡張である
- **ユーザーメリット**:
  - 複数ページにわたるテーブルでの自動ヘッダー繰り返し
  - スクリーンリーダー向けの適切なアクセシビリティメタデータ
  - Typstベストプラクティスへの準拠
  - Typstのshow rulesを使用したヘッダーの差別化スタイリング

## Related Issues

- Fixes #40: Table headers are not wrapped in table.header()
- Related to #39: Cell spanning support will benefit from proper header/body distinction
