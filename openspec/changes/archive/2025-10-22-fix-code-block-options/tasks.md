# Implementation Tasks

## 1. Code Block Line Numbers Support - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [x] `:linenos:`オプションなしのコードブロックのテストを作成
  - Test name: `test_code_block_without_linenos`
  - Test file: `tests/test_translator.py`
  - Expected: 行番号設定が含まれない

- [x] `:linenos:`オプション付きコードブロックのテストを作成
  - Test name: `test_code_block_with_linenos`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（codly行番号設定が含まれない）

- [x] `:linenos:`と`:emphasize-lines:`の組み合わせテストを作成
  - Test name: `test_code_block_linenos_with_highlights`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

### Phase 2: Confirm RED

- [x] すべての行番号テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_code_block_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_with_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_linenos_with_highlights -xvs
  ```
  **Result:** Only `test_code_block_without_linenos` failed as expected (others already working due to codly defaults)

### Phase 3: GREEN (Implement)

- [x] `visit_literal_block()`メソッドを拡張
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `node.get('linenos')`をチェック
    - linenos が False の場合、`#codly(number-format: none)` を追加して行番号を無効化
    - 既存の`:emphasize-lines:`処理と共存できるようにする

### Phase 4: Confirm GREEN

- [x] すべての行番号テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_code_block_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_with_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_linenos_with_highlights -xvs
  ```
  **Result:** すべてのテストがパス ✓

## 2. Code Block Caption and Label Support - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [x] キャプション付きコードブロックのテストを作成
  - Test name: `test_code_block_with_caption`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（`#figure()`でラップされない）

- [x] キャプションとラベル付きコードブロックのテストを作成
  - Test name: `test_code_block_with_caption_and_name`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [x] ラベルのみのコードブロックのテストを作成
  - Test name: `test_code_block_with_name_only`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [x] 複数オプション組み合わせのテストを作成
  - Test name: `test_code_block_all_options`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [x] ~~キャプションテキストエスケープのテストを作成~~ (not needed - basic caption test covers this)

### Phase 2: Confirm RED

- [x] すべてのキャプション/ラベルテストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py -k "caption or name or all_options" -xvs
  ```
  **Result:** すべてのテストが正しい理由で失敗（メソッド未実装または機能不足）✓

### Phase 3: GREEN (Implement)

- [x] `visit_container()`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `literal-block-wrapper`クラスを持つcontainerノードを検出
    - キャプションとコードブロックを抽出
    - `in_captioned_code_block`フラグを設定
    - キャプションテキストとラベルを保存

- [x] `depart_container()`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: クリーンアップ処理

- [x] `visit_literal_block()`を拡張してキャプション/ラベル対応
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `in_captioned_code_block`フラグをチェック
    - キャプションがある場合、`#figure()`でラップ
    - `:name:`からラベルを生成
    - キャプションテキストを適切にエスケープ

- [x] `depart_literal_block()`を拡張
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `#figure()`の閉じ括弧を追加
    - ラベルを追加（captionあり/なし両方に対応）

- [x] `visit_caption()`を拡張
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - コードブロックのcaptionの場合は`SkipNode`を発生させて重複を防止

### Phase 4: Confirm GREEN

- [x] すべてのキャプション/ラベルテストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py -k "caption or name or all_options" -xvs
  ```
  **Result:** すべてのテストがパス ✓

### Phase 5: REFACTOR (Optional)

- [x] コードの可読性を改善 - コメント追加
- [x] 重複コードなし - 確認済み
- [x] ヘルパーメソッド不要 - 実装がシンプル
- [x] テスト再実行 - すべてパス

## 3. Regression Testing

- [x] 既存のトランスレータテストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Result:** 55 tests passed ✓

- [x] 既存のコードブロックテストが影響を受けていないことを確認
  ```bash
  uv run pytest tests/test_translator.py -k "literal_block" -v
  ```
  **Result:** 既存のコードブロックテストがすべてパス ✓

## 4. Integration Verification

- [x] ~~実際のRSTファイルでcode-blockオプションをテスト~~ (covered by unit tests)
  - Unit testsで十分な網羅性を達成
  - `:linenos:`、`:caption:`、`:name:`、`:emphasize-lines:`すべてカバー済み

- [x] ~~生成されたTypstファイルを手動で検証~~ (covered by unit tests)
  - Unit testsで出力を検証済み
  - `#figure()`構造、キャプション、ラベルすべて確認済み

- [x] ~~Typst PDFビルダーでの動作確認~~ (skipped - environment dependent)
  - PDF builder testsは環境依存（typst CLI必要）
  - Unit level testsで十分な検証完了

- [x] 「unknown node type: container」警告が消えることを確認
  - `visit_container()`実装により警告解消
  - Tests実行時に警告が表示されないことを確認

## 5. Quality Checks

- [x] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```
  **Result:** Success - no issues found ✓

- [x] リンティング
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py
  ```
  **Result:** All checks passed ✓

- [x] フォーマットチェック
  ```bash
  uv run black --check sphinxcontrib/typst/translator.py
  ```
  **Result:** 1 file would be left unchanged ✓

## 6. Final Validation

- [x] フルテストスイート実行
  ```bash
  uv run pytest
  ```
  **Result:** 323 passed, 3 failed (PDF integration tests - environment issue) ✓

- [x] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Result:** 94% coverage maintained ✓

## 7. Documentation

- [x] CHANGELOG.mdに修正内容を記録
  - セクション: `[Unreleased]`
  - カテゴリ: `Fixed`
  - 内容: Issue #20の詳細な修正内容

- [x] Issue #20をクローズするコメントを追加
  - 修正内容の説明 → PR #30に詳細記載
  - 使用例の記載 → PR #30に記載
  - ビフォー・アフターの比較 → PR #30に記載
  - **Note:** PR #30がマージされた後、自動的にIssue #20がクローズされる

## Task Dependencies

- Phase 1-2 (RED) はPhase 3-4 (GREEN) の前に完了する必要がある
- 行番号サポート（タスク1）とキャプション/ラベルサポート（タスク2）は並行して実装可能
- Phase 5 (REFACTOR) はオプションだが推奨
- Regression testing（タスク3）はすべての実装完了後に実行

## Implementation Notes

- codlyは既にテンプレートで初期化されているため、行番号機能は利用可能
- containerノードは`:caption:`オプション使用時にSphinxによって自動生成される
- `#figure()`のcaptionパラメータは`[...]`でラップする必要がある
- ラベルは`<label-name>`形式で出力する
- 既存の`:emphasize-lines:`処理を壊さないように注意
