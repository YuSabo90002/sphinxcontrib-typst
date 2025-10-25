# Implementation Tasks

## Phase 1: Core Implementation

- [ ] `visit_entry()`でセル結合属性を読み取る
  - `morecols`属性を取得（デフォルト0）
  - `morerows`属性を取得（デフォルト0）
  - `colspan = morecols + 1`に変換
  - `rowspan = morerows + 1`に変換

- [ ] セルストレージに結合情報を追加
  - `depart_entry()`で`colspan`と`rowspan`をセル辞書に追加
  - 構造: `{"content": str, "is_header": bool, "colspan": int, "rowspan": int}`

- [ ] `depart_table()`で結合セル用のTypst構文を生成
  - 結合セル（colspan > 1 または rowspan > 1）: `table.cell(colspan: N, rowspan: M)[content]`
  - 通常セル: `[content]`
  - ヘッダー結合セルも`table.header()`内で正しく処理

## Phase 2: Testing

- [ ] 水平結合（colspan）のテストを作成
  - 2列結合のテスト
  - 3列以上の結合のテスト

- [ ] 垂直結合（rowspan）のテストを作成
  - 2行結合のテスト
  - 3行以上の結合のテスト

- [ ] 複合結合（colspan + rowspan）のテストを作成
  - 同時に水平・垂直結合するセル

- [ ] ヘッダー内の結合セルのテストを作成
  - `table.header()`内でのセル結合

- [ ] 複数の結合セルを持つテーブルのテストを作成
  - 同一テーブル内に複数の結合セル

- [ ] 結合なしテーブルのリグレッションテスト
  - 既存の動作が壊れていないことを確認

## Phase 3: Quality Assurance

- [ ] 型チェッカーを実行
  - `uv run mypy typsphinx/`
  - 型エラーを修正

- [ ] リンターを実行
  - `uv run ruff check .`
  - 問題を修正

- [ ] フォーマッターを実行
  - `uv run black .`
  - フォーマット変更をコミット

- [ ] 全テストスイートを実行
  - `uv run pytest`
  - すべてのテストがパスすることを確認

## Phase 4: Documentation

- [ ] CHANGELOG.mdに新機能を追加
- [ ] ドキュメントに例を追加（該当する場合）

## Validation

- [ ] 実際のgrid tableでの手動テスト
  - 結合セルを含むテーブルをビルド
  - 生成された`.typ`ファイルを確認
  - PDF出力で結合が正しくレンダリングされることを確認

- [ ] OpenSpec準拠を検証
  - `openspec validate support-cell-spanning --strict`
  - 検証エラーを解決
