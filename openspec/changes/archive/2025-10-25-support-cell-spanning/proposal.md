# Proposal: Support Cell Spanning (colspan/rowspan)

## Why

現在、typsphinxはgrid tableのセル結合（`morecols`と`morerows`属性）を無視しており、結合されたセルが正しくレンダリングされない。これにより、複雑なテーブルレイアウトを持つドキュメントをTypst/PDFに変換すると、テーブル構造が崩れる。

reStructuredTextのgrid tableは`morecols`（水平結合）と`morerows`（垂直結合）をサポートしており、これらは複雑なヘッダーやデータの視覚的整理に広く使用されている。Typstも`table.cell(colspan: N, rowspan: M)`でセル結合をサポートしているため、この機能を実装することでドキュメントの忠実な変換が可能になる。

## What Changes

- `visit_entry()`でセル結合情報（`morecols`, `morerows`属性）を検出する
- セルストレージに`colspan`と`rowspan`情報を追加する（現在の`{"content": str, "is_header": bool}`を拡張）
- `depart_table()`で結合セルに対して`table.cell(colspan: N, rowspan: M)[content]`を生成する
- 通常セル（結合なし）は従来通り`[content]`として出力する

## Impact

- **影響を受ける仕様**: `table-rendering`
- **影響を受けるコード**:
  - `typsphinx/translator.py` (`visit_entry`, `depart_entry`, `depart_table`)
- **破壊的変更**: なし - 既存のテーブル出力との後方互換性を維持
- **ユーザーメリット**:
  - 複雑なテーブルレイアウトの正確な再現
  - 結合ヘッダーセルのサポート
  - reStructuredText文書の忠実な変換

## Related Issues

- Fixes #39: Support for grid table cell spanning
- Builds on #40: Header wrapping implementation (uses the same cell dictionary structure)
