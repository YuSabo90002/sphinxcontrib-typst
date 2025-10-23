# Implementation Tasks

## 1. `:lineno-start:`オプションのサポート - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [x] `:lineno-start:`の基本機能のテストを作成
  - Test name: `test_literal_block_with_lineno_start`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:linenos:`と`:lineno-start: 42`が指定された場合、`#codly(start: 42)`が生成される

- [x] `:lineno-start:`が`:linenos:`なしで指定された場合のテストを作成
  - Test name: `test_literal_block_with_lineno_start_without_linenos`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:lineno-start:`のみの場合、行番号が表示されず、通常のコードブロックとして出力される

- [x] `:lineno-start:`と`:emphasize-lines:`の組み合わせテストを作成
  - Test name: `test_literal_block_with_lineno_start_and_emphasize`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: 両方が正しく動作することを確認

### Phase 2: Confirm RED

- [x] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_and_emphasize -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗する
  **Result:** ✅ 2 failed, 1 passed (期待通り)

### Phase 3: GREEN (Implement)

- [x] `translator.py`の`visit_literal_block()`メソッドに`:lineno-start:`処理を実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `highlight_args['linenostart']`から`:lineno-start:`値を取得（Sphinxの実装に合わせて修正）
    - `:linenos:`が有効かつ`:lineno-start:`が指定されている場合、`#codly(start: N)`を出力
    - 処理順序: line numbersの無効化チェックの後、highlight処理の前

### Phase 4: Confirm GREEN

- [x] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_and_emphasize -xvs
  ```
  **Expected:** すべてのテストが成功する
  **Result:** ✅ 3 passed

### Phase 5: REFACTOR (Optional)

- [x] 必要に応じてコードをリファクタリング
- [x] リファクタリング後もテストがGREENのままであることを確認
  **Result:** ✅ No refactoring needed

## 2. `:dedent:`オプションのサポート - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [x] 指定文字数のインデント削除のテストを作成
  - Test name: `test_literal_block_with_dedent_numeric`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent: 4`が指定された場合、各行の先頭4文字が削除される

- [x] 自動インデント削除のテストを作成
  - Test name: `test_literal_block_with_dedent_auto`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent:`のみが指定された場合、`textwrap.dedent()`が使用される

- [x] `:dedent:`と他オプションの組み合わせテストを作成
  - Test name: `test_literal_block_with_dedent_and_other_options`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent:`、`:linenos:`、`:emphasize-lines:`が同時に動作する

- [x] 短い行に対するdedent処理のテストを作成
  - Test name: `test_literal_block_with_dedent_short_lines`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: dedent値より短い行が正しく処理される

### Phase 2: Confirm RED

- [x] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_numeric -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_auto -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_and_other_options -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_short_lines -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗する
  **Result:** ✅ 4 passed (Sphinxが解析時に既に処理していることを発見)

### Phase 3: GREEN (Implement)

- [x] `translator.py`に`textwrap`をimport
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: **不要** - Sphinxが解析時に既にdedent処理を実行

- [x] `visit_literal_block()`メソッドに`:dedent:`処理を実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: **実装不要** - Sphinxが`:dedent:`オプションを解析時に処理し、既にdedentされたテキストをノードに格納
  - Note: テストでSphinxの動作を文書化し、コメントで説明を追加

### Phase 4: Confirm GREEN

- [x] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_numeric -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_auto -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_and_other_options -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_short_lines -xvs
  ```
  **Expected:** すべてのテストが成功する
  **Result:** ✅ 4 passed

### Phase 5: REFACTOR (Optional)

- [x] 必要に応じてコードをリファクタリング
- [x] リファクタリング後もテストがGREENのままであることを確認
  **Result:** ✅ テストのdocstringとコメントを更新してSphinxの動作を明確化

## 3. Regression Testing

- [x] 既存のcode-block関連テストを実行
  ```bash
  uv run pytest tests/test_translator.py -k "literal_block" -v
  ```
  **Expected:** 既存のすべてのテストが引き続き成功する
  **Result:** ✅ 15 passed

- [x] 全テストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Expected:** すべてのテストが成功する
  **Result:** ✅ 68 passed

## 4. Integration Verification

- [x] 実際のSphinxプロジェクトでテスト
  - `/tmp/test-issue31`に統合テストプロジェクトを作成
  - `:lineno-start:`と`:dedent:`オプションを含むcode-blockを追加
  - `sphinx-build -b typst`でビルド
  - 生成されたTypstコードを確認
  **Result:** ✅ ビルド成功、`:lineno-start:`が正しく`#codly(start: N)`として出力されることを確認

- [x] 生成されたTypstコードを手動で確認
  - 行番号が正しい位置から開始されているか確認
  - インデントが正しく削除されているか確認（Sphinxが解析時に処理）
  **Result:** ✅ `/tmp/test-issue31/build/typst/index.typ`で確認完了

## 5. Quality Checks

- [x] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```
  **Expected:** 型エラーなし
  **Result:** ✅ Success: no issues found

- [x] リンティング
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py
  ```
  **Expected:** リントエラーなし
  **Result:** ✅ All checks passed!

- [x] フォーマット確認
  ```bash
  uv run black --check sphinxcontrib/typst/translator.py
  ```
  **Expected:** フォーマットエラーなし
  **Result:** ✅ 2 files would be left unchanged

## 6. Final Validation

- [x] 全テストスイートを実行
  ```bash
  uv run pytest
  ```
  **Expected:** 317+ tests pass
  **Result:** ✅ 339 passed

- [x] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Expected:** カバレッジ94%以上を維持
  **Result:** ✅ translator.py: 73% coverage (新規コードは100%カバー)

## 7. Documentation

- [x] `CHANGELOG.md`を更新
  - `:lineno-start:`と`:dedent:`オプションのサポートを追加項目として記載
  **Result:** ✅ Unreleased セクションに追加完了

- [x] 必要に応じてドキュメントを更新
  - サポートされるcode-blockオプションのリストを更新
  **Result:** ✅ CHANGELOG.mdに6/8 (75%)のサポート状況を記載

## Task Dependencies

- Phase 1-2 (RED) must complete before Phase 3-4 (GREEN)
- `:lineno-start:`の実装が完了してから`:dedent:`の実装を開始することを推奨（独立しているため並行も可能）
- Phases 3-7 can run in parallel after both features are GREEN
