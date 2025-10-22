# Implementation Tasks

## 1. Code Block Line Numbers Support - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [ ] `:linenos:`オプションなしのコードブロックのテストを作成
  - Test name: `test_code_block_without_linenos`
  - Test file: `tests/test_translator.py`
  - Expected: 行番号設定が含まれない

- [ ] `:linenos:`オプション付きコードブロックのテストを作成
  - Test name: `test_code_block_with_linenos`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（codly行番号設定が含まれない）

- [ ] `:linenos:`と`:emphasize-lines:`の組み合わせテストを作成
  - Test name: `test_code_block_linenos_with_highlights`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

### Phase 2: Confirm RED

- [ ] すべての行番号テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_code_block_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_with_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_linenos_with_highlights -xvs
  ```
  **Expected:** `:linenos:`関連のテストが失敗

### Phase 3: GREEN (Implement)

- [ ] `visit_literal_block()`メソッドを拡張
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `node.get('linenos')`をチェック
    - linenos が True の場合、codlyの行番号設定を追加
    - 既存の`:emphasize-lines:`処理と共存できるようにする

### Phase 4: Confirm GREEN

- [ ] すべての行番号テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_code_block_without_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_with_linenos -xvs
  uv run pytest tests/test_translator.py::test_code_block_linenos_with_highlights -xvs
  ```
  **Expected:** すべてのテストがパス

## 2. Code Block Caption and Label Support - TDD Cycle

### Phase 1: RED (Write Failing Tests)

- [ ] キャプション付きコードブロックのテストを作成
  - Test name: `test_code_block_with_caption`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（`#figure()`でラップされない）

- [ ] キャプションとラベル付きコードブロックのテストを作成
  - Test name: `test_code_block_with_caption_and_name`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] ラベルのみのコードブロックのテストを作成
  - Test name: `test_code_block_with_name_only`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] containerノード処理のテストを作成
  - Test name: `test_container_with_literal_block_wrapper`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗（メソッド未実装）

- [ ] 複数オプション組み合わせのテストを作成
  - Test name: `test_code_block_all_options`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

- [ ] キャプションテキストエスケープのテストを作成
  - Test name: `test_code_block_caption_escaping`
  - Test file: `tests/test_translator.py`
  - Expected: 初期状態では失敗

### Phase 2: Confirm RED

- [ ] すべてのキャプション/ラベルテストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py -k "caption or name or container" -xvs
  ```
  **Expected:** すべてのテストが正しい理由で失敗（メソッド未実装または機能不足）

### Phase 3: GREEN (Implement)

- [ ] `visit_container()`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `literal-block-wrapper`クラスを持つcontainerノードを検出
    - キャプションとコードブロックを抽出
    - `in_captioned_code_block`フラグを設定
    - キャプションテキストを保存

- [ ] `depart_container()`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes: クリーンアップ処理

- [ ] `visit_literal_block()`を拡張してキャプション/ラベル対応
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - `in_captioned_code_block`フラグをチェック
    - キャプションがある場合、`#figure()`でラップ
    - `:name:`からラベルを生成
    - キャプションテキストを適切にエスケープ

- [ ] `visit_caption()`と`depart_caption()`メソッドを実装
  - File: `sphinxcontrib/typst/translator.py`
  - Changes:
    - captionノードのテキストを抽出
    - container処理で使用するために保存

### Phase 4: Confirm GREEN

- [ ] すべてのキャプション/ラベルテストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py -k "caption or name or container" -xvs
  ```
  **Expected:** すべてのテストがパス

### Phase 5: REFACTOR (Optional)

- [ ] コードの可読性を改善
- [ ] 重複コードがあれば削除
- [ ] ヘルパーメソッドの抽出を検討
- [ ] リファクタリング後にテストを再実行

## 3. Regression Testing

- [ ] 既存のトランスレータテストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Expected:** 既存のすべてのテストがパス

- [ ] 既存のコードブロックテストが影響を受けていないことを確認
  ```bash
  uv run pytest tests/test_translator.py -k "literal_block" -v
  ```
  **Expected:** 既存のコードブロックテストがすべてパス

## 4. Integration Verification

- [ ] 実際のRSTファイルでcode-blockオプションをテスト
  - テストフィクスチャを作成または更新
  - `:linenos:`、`:caption:`、`:name:`、`:emphasize-lines:`を含む
  - `sphinx-build -b typst`でビルドして出力を確認

- [ ] 生成されたTypstファイルを手動で検証
  - 行番号設定が正しく出力されているか
  - `#figure()`構造が正しいか
  - キャプションとラベルが適切か
  - 特殊文字のエスケープが正しいか

- [ ] Typst PDFビルダーでの動作確認
  ```bash
  uv run pytest tests/test_pdf_builder.py -v
  ```
  **Expected:** PDFビルダーでも新機能が正しく処理される

- [ ] 「unknown node type: container」警告が消えることを確認
  - ビルドログに警告が表示されないことを確認

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
  **Expected:** リンティングエラーなし

- [ ] フォーマットチェック
  ```bash
  uv run black --check sphinxcontrib/typst/translator.py
  ```
  **Expected:** フォーマットエラーなし

## 6. Final Validation

- [ ] フルテストスイート実行
  ```bash
  uv run pytest
  ```
  **Expected:** すべてのテストがパス（325+ tests）

- [ ] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Expected:** カバレッジが94%以上を維持

## 7. Documentation

- [ ] CHANGELOG.mdに修正内容を記録
  - セクション: `[Unreleased]`
  - カテゴリ: `Fixed`
  - 内容: Issue #20の修正内容

- [ ] Issue #20をクローズするコメントを追加
  - 修正内容の説明
  - 使用例の記載
  - ビフォー・アフターの比較

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
