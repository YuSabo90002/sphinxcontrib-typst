# Implementation Tasks

## Phase 1: Core Implementation

- [ ] translatorに`in_thead`状態フラグを追加
  - `__init__()`で`False`に初期化
  - `visit_thead()`で`True`に設定
  - `depart_thead()`で`False`に設定

- [ ] セルストレージを修正してヘッダー/ボディの区別を追跡
  - `table_cells`を文字列のリストから`{"content": str, "is_header": bool}`の辞書のリストに変更
  - `depart_entry()`を更新し、`in_thead`状態に基づいて`is_header`フラグを保存

- [ ] `depart_table()`を更新して`table.header()`ラッパーを生成
  - ヘッダーセルとボディセルを分離
  - ヘッダーセルに対して`table.header(...)`ラッパーを生成
  - ボディセルに対して通常のセルを生成
  - エッジケースの処理: ヘッダーのないテーブル（従来通り動作すべき）

## Phase 2: Testing

- [ ] ヘッダー追跡のユニットテストを作成
  - `visit_thead()`/`depart_thead()`の状態管理をテスト
  - `is_header`フラグを持つセルストレージをテスト

- [ ] テーブルレンダリングの統合テストを作成
  - ヘッダー付きgrid table
  - `:header-rows: 1`付きlist table
  - ヘッダー付きsimple table
  - `:header:`オプション付きCSV table
  - ヘッダーのないテーブル（リグレッションテスト）
  - 複数行ヘッダー（`:header-rows: 2`）

- [ ] テストカバレッジを検証
  - `uv run pytest --cov=typsphinx --cov-report=term-missing`を実行
  - 新しいコードが90%以上のカバレッジを持つことを確認

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
  - 317以上のテストがすべてパスすることを確認

## Phase 4: Documentation

- [ ] CHANGELOG.mdに新機能を追加
- [ ] ドキュメントに例を追加（該当する場合）

## Validation

- [ ] サンプルドキュメントでの手動テスト
  - 複数ページにわたるテーブルを含むテストドキュメントを作成
  - PDF出力でヘッダー繰り返しを検証
  - スクリーンリーダーでテスト（可能な場合）

- [ ] OpenSpec準拠を検証
  - `openspec validate wrap-table-headers --strict`
  - 検証エラーを解決
