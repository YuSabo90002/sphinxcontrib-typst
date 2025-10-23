# Implementation Tasks

## 1. `:lineno-start:`オプションのサポート - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [ ] `:lineno-start:`の基本機能のテストを作成
  - Test name: `test_literal_block_with_lineno_start`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:linenos:`と`:lineno-start: 42`が指定された場合、`#codly(start: 42)`が生成される

- [ ] `:lineno-start:`が`:linenos:`なしで指定された場合のテストを作成
  - Test name: `test_literal_block_with_lineno_start_without_linenos`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:lineno-start:`のみの場合、行番号が表示されず、通常のコードブロックとして出力される

- [ ] `:lineno-start:`と`:emphasize-lines:`の組み合わせテストを作成
  - Test name: `test_literal_block_with_lineno_start_and_emphasize`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: 両方が正しく動作することを確認

### Phase 2: Confirm RED

- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_and_emphasize -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗する

### Phase 3: GREEN (Implement)

- [ ] `translator.py`の`visit_literal_block()`メソッドに`:lineno-start:`処理を実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `:lineno-start:`オプションを取得
    - `:linenos:`が有効かつ`:lineno-start:`が指定されている場合、`#codly(start: N)`を出力
    - 処理順序: line numbersの無効化チェックの後、highlight処理の前

### Phase 4: Confirm GREEN

- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_lineno_start_and_emphasize -xvs
  ```
  **Expected:** すべてのテストが成功する

### Phase 5: REFACTOR (Optional)

- [ ] 必要に応じてコードをリファクタリング
- [ ] リファクタリング後もテストがGREENのままであることを確認

## 2. `:dedent:`オプションのサポート - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [ ] 指定文字数のインデント削除のテストを作成
  - Test name: `test_literal_block_with_dedent_numeric`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent: 4`が指定された場合、各行の先頭4文字が削除される

- [ ] 自動インデント削除のテストを作成
  - Test name: `test_literal_block_with_dedent_auto`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent:`のみが指定された場合、`textwrap.dedent()`が使用される

- [ ] `:dedent:`と他オプションの組み合わせテストを作成
  - Test name: `test_literal_block_with_dedent_and_other_options`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: `:dedent:`、`:linenos:`、`:emphasize-lines:`が同時に動作する

- [ ] 短い行に対するdedent処理のテストを作成
  - Test name: `test_literal_block_with_dedent_short_lines`
  - Test file: `tests/test_translator.py`
  - Expected to fail initially
  - テスト内容: dedent値より短い行が正しく処理される

### Phase 2: Confirm RED

- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_numeric -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_auto -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_and_other_options -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_short_lines -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗する

### Phase 3: GREEN (Implement)

- [ ] `translator.py`に`textwrap`をimport
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: `import textwrap`を追加

- [ ] `visit_literal_block()`メソッドに`:dedent:`処理を実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `:dedent:`オプションを取得
    - コードブロックのテキストコンテンツを取得
    - dedent値に応じてテキストを処理（数値の場合は各行から指定文字数削除、それ以外は`textwrap.dedent()`）
    - 処理したテキストでノードの内容を更新
    - この処理はコードブロックの出力前に実行

### Phase 4: Confirm GREEN

- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_numeric -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_auto -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_and_other_options -xvs
  uv run pytest tests/test_translator.py::test_literal_block_with_dedent_short_lines -xvs
  ```
  **Expected:** すべてのテストが成功する

### Phase 5: REFACTOR (Optional)

- [ ] 必要に応じてコードをリファクタリング
- [ ] リファクタリング後もテストがGREENのままであることを確認

## 3. Regression Testing

- [ ] 既存のcode-block関連テストを実行
  ```bash
  uv run pytest tests/test_translator.py -k "literal_block" -v
  ```
  **Expected:** 既存のすべてのテストが引き続き成功する

- [ ] 全テストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Expected:** すべてのテストが成功する

## 4. Integration Verification

- [ ] 実際のSphinxプロジェクトでテスト
  - `examples/`ディレクトリ内の既存サンプルを使用
  - `:lineno-start:`と`:dedent:`オプションを含むcode-blockを追加
  - `uv run sphinx-build -b typst`でビルド
  - 生成されたTypstコードを確認

- [ ] 生成されたTypstコードを手動でコンパイルして確認
  ```bash
  typst compile <generated-file>.typ
  ```
  - 行番号が正しい位置から開始されているか確認
  - インデントが正しく削除されているか確認

## 5. Quality Checks

- [ ] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```
  **Expected:** 型エラーなし

- [ ] リンティング
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py
  ```
  **Expected:** リントエラーなし

- [ ] フォーマット確認
  ```bash
  uv run black --check sphinxcontrib/typst/translator.py
  ```
  **Expected:** フォーマットエラーなし

## 6. Final Validation

- [ ] 全テストスイートを実行
  ```bash
  uv run pytest
  ```
  **Expected:** 317+ tests pass

- [ ] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Expected:** カバレッジ94%以上を維持

## 7. Documentation

- [ ] `CHANGELOG.md`を更新
  - `:lineno-start:`と`:dedent:`オプションのサポートを追加項目として記載

- [ ] 必要に応じてドキュメントを更新
  - サポートされるcode-blockオプションのリストを更新

## Task Dependencies

- Phase 1-2 (RED) must complete before Phase 3-4 (GREEN)
- `:lineno-start:`の実装が完了してから`:dedent:`の実装を開始することを推奨（独立しているため並行も可能）
- Phases 3-7 can run in parallel after both features are GREEN
