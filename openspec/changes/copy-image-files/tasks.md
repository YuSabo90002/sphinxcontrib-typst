# Implementation Tasks

## Phase 1: Core Implementation

- [x] `TypstBuilder`に`post_process_images()`メソッドを追加
  - `self.images`辞書を初期化
  - ドキュメントツリーから画像を収集
  - 画像パスを追跡

- [x] `copy_image_files()`メソッドを実装
  - `self.images`からソースパスを取得
  - ソースディレクトリから出力ディレクトリへコピー
  - ディレクトリ構造を保持

- [x] `finish()`メソッドを拡張
  - PDF生成前に`copy_image_files()`を呼び出し
  - 既存のPDF生成処理を維持

- [x] 画像パス解決の実装
  - 相対パスの正しい解決
  - 絶対パスの処理
  - 出力ディレクトリ内の正しい配置

## Phase 2: Testing

- [x] 画像コピーの基本テストを作成
  - 単一画像のコピー
  - 複数画像のコピー

- [x] パス処理のテストを作成
  - 相対パスの画像
  - サブディレクトリ内の画像

- [x] ビルド統合テストを作成
  - typstpdfビルダーで画像を含むドキュメントをビルド
  - コピーされた画像ファイルの存在確認
  - PDF生成の成功確認

- [x] エッジケースのテストを作成
  - 存在しない画像ファイル
  - 画像なしドキュメント（リグレッション）

## Phase 3: Quality Assurance

- [x] 型チェッカーを実行
  - `uv run mypy typsphinx/`
  - 型エラーを修正

- [x] リンターを実行
  - `uv run ruff check .`
  - 問題を修正

- [x] フォーマッターを実行
  - `uv run black .`
  - フォーマット変更をコミット

- [x] 全テストスイートを実行
  - `uv run pytest`
  - すべてのテストがパスすることを確認

## Phase 4: Documentation

- [x] CHANGELOG.mdに新機能を追加
- [x] 必要に応じて画像使用例をドキュメントに追加

## Validation

- [x] 実際の画像を含むドキュメントでの手動テスト
  - 画像ディレクティブを含むrstファイルを作成
  - typstpdfビルダーでビルド
  - 画像が出力ディレクトリにコピーされることを確認
  - PDF生成が成功することを確認

- [x] OpenSpec準拠を検証
  - `openspec validate copy-image-files --strict`
  - 検証エラーを解決
