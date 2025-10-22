# Implementation Tasks

## 1. Raw Directive Support - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [ ] Typstフォーマットのrawコンテンツパススルーのテストを作成
  - Test name: `test_raw_typst_passthrough`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（メソッド未実装）

- [ ] 他のフォーマット（HTML/LaTeX）のrawコンテンツスキップのテストを作成
  - Test name: `test_raw_other_formats_skip`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] 複数のrawディレクティブ混在のテストを作成
  - Test name: `test_raw_multiple_formats`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] Typst rawコンテンツの改行処理のテストを作成
  - Test name: `test_raw_typst_multiline`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] 空のrawディレクティブのテストを作成
  - Test name: `test_raw_empty_content`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] 大文字小文字混在フォーマット名のテストを作成
  - Test name: `test_raw_case_insensitive_format`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

### Phase 2: Confirm RED

- [ ] すべてのrawディレクティブテストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_raw_typst_passthrough -xvs
  uv run pytest tests/test_translator.py::test_raw_other_formats_skip -xvs
  uv run pytest tests/test_translator.py::test_raw_multiple_formats -xvs
  uv run pytest tests/test_translator.py::test_raw_typst_multiline -xvs
  uv run pytest tests/test_translator.py::test_raw_empty_content -xvs
  uv run pytest tests/test_translator.py::test_raw_case_insensitive_format -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗（メソッド未実装）

### Phase 3: GREEN (Implement)

- [ ] `TypstTranslator`に`visit_raw`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `format='typst'`の場合、rawコンテンツをそのまま出力
    - 他のフォーマットの場合、`nodes.SkipNode`を発生させる
    - フォーマット名の大文字小文字を区別しない処理
    - デバッグログの追加

- [ ] `TypstTranslator`に`depart_raw`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: 空のメソッド（クリーンアップ不要）

### Phase 4: Confirm GREEN

- [ ] すべてのrawディレクティブテストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_raw_typst_passthrough -xvs
  uv run pytest tests/test_translator.py::test_raw_other_formats_skip -xvs
  uv run pytest tests/test_translator.py::test_raw_multiple_formats -xvs
  uv run pytest tests/test_translator.py::test_raw_typst_multiline -xvs
  uv run pytest tests/test_translator.py::test_raw_empty_content -xvs
  uv run pytest tests/test_translator.py::test_raw_case_insensitive_format -xvs
  ```
  **Expected:** すべてのテストがパス

### Phase 5: REFACTOR (Optional)

- [ ] コードの可読性を改善
- [ ] 重複コードがあれば削除
- [ ] リファクタリング後にテストを再実行

## 2. Regression Testing

- [ ] 既存のトランスレータテストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Expected:** 既存のすべてのテストがパス

- [ ] コメントノード処理テストが影響を受けていないことを確認
  ```bash
  uv run pytest tests/test_translator.py -k comment -v
  ```
  **Expected:** コメント関連のすべてのテストがパス

## 3. Integration Verification

- [ ] 実際のRSTファイルでraw directiveをテスト
  - `tests/fixtures/`に新しいテストフィクスチャを作成
  - Typst、HTML、LaTeXのrawディレクティブを含む
  - `sphinx-build -b typst`でビルドして出力を確認

- [ ] 生成されたTypstファイルを手動で検証
  - rawコンテンツが正しく出力されているか
  - 不要なフォーマットがスキップされているか
  - 改行とインデントが保持されているか

- [ ] Typst PDFビルダーでの動作確認
  ```bash
  uv run pytest tests/test_pdf_builder.py -v
  ```
  **Expected:** PDFビルダーでもrawディレクティブが正しく処理される

## 4. Quality Checks

- [ ] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```
  **Expected:** 型エラーなし

- [ ] リンティング
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py
  ```
  **Expected:** リンティングエラーなし

- [ ] フォーマットチェック
  ```bash
  uv run black --check sphinxcontrib/typst/translator.py
  ```
  **Expected:** フォーマットエラーなし

## 5. Final Validation

- [ ] フルテストスイート実行
  ```bash
  uv run pytest
  ```
  **Expected:** すべてのテストがパス（317+ tests）

- [ ] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Expected:** カバレッジが94%以上を維持

- [ ] CI環境でのテスト
  ```bash
  uv run tox
  ```
  **Expected:** すべての環境でテストがパス

## 6. Documentation

- [ ] CHANGELOG.mdに追加内容を記録
  - セクション: `[Unreleased]` または次のバージョン
  - カテゴリ: `Added`
  - 内容: rawディレクティブのサポート追加

- [ ] Issue #25をクローズするコメントを追加
  - 実装内容の説明
  - 使用例の記載

## Task Dependencies

- Phase 1-2 (RED) はPhase 3-4 (GREEN) の前に完了する必要がある
- Phase 5 (REFACTOR) はオプションだが推奨
- Phases 2-6 は GREEN 達成後に並行実行可能

## Implementation Notes

- `visit_raw`と`depart_raw`の実装は、既存の`visit_comment`/`depart_comment`パターンに従う
- `nodes.SkipNode`を使用して不要なフォーマットをスキップ
- ログレベルはデバッグ（`logger.debug`）を使用
- コンテンツの後に`\n\n`を追加して適切な段落分離を確保
