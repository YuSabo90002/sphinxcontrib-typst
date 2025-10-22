# Implementation Tasks

## 1. Code Modification

- [x] `template_engine.py` の `generate_document()` メソッドを修正
  - File: `sphinxcontrib/typst/template_engine.py`
  - Location: lines 293-294 (essential imports section)
  - Changes:
    - Add `#import "@preview/codly:1.3.0": *`
    - Add `#import "@preview/codly-languages:0.1.1": *`
    - Place before existing `mitex` and `gentle-clues` imports
  - Expected result: Document files include codly imports

## 2. Verification Testing

**重要:** mainブランチの統合テストはcodly関数を使わないため、修正の効果を検証できない。
手動検証テストで修正の効果を確認する必要がある。

- [x] 手動検証テスト（修正前）- Issue #20ブランチで失敗を確認
  ```bash
  # Issue #20ブランチに切り替え（Issue #28の修正を適用しない状態）
  git stash  # 現在の変更を退避
  git checkout fix/issue-20-code-block-options

  # PDFビルド実行
  rm -rf /tmp/test-before
  uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test-before

  # 期待結果: エラー "Typst compilation failed: unknown variable: codly"
  ```
  **Expected:** Build fails with "unknown variable: codly" error

- [x] 手動検証テスト（修正後）- Issue #28ブランチで成功を確認
  ```bash
  # Issue #28ブランチに戻る（修正適用済み）
  git checkout fix/issue-28-codly-import
  git stash pop  # 変更を復元

  # 修正を適用（次のタスクで実施）
  # template_engine.pyを編集

  # PDFビルド実行
  rm -rf /tmp/test-after
  uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test-after

  # 期待結果: PDF生成成功
  ls -la /tmp/test-after/index.pdf
  ```
  **Expected:** Build succeeds, PDF file generated

- [x] 生成されたドキュメントファイルの確認
  ```bash
  cat /tmp/test-after/index.typ | head -10
  ```
  **Expected:** codly imports present in output:
  ```
  #import "@preview/codly:1.3.0": *
  #import "@preview/codly-languages:0.1.1": *
  ```

- [x] mainブランチでのPDFビルドテスト（後方互換性確認）
  ```bash
  # mainブランチに切り替え
  git checkout main

  # 修正を一時的に適用
  # ... template_engine.pyにcodly importを追加

  # PDFビルド実行
  uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test-main
  ```
  **Expected:** Build succeeds (no regression)

## 3. Integration Tests

**注意:** mainブランチの統合テストは現時点でcodly関数を使用しないため、修正前後で差が出ない。
統合テストは後方互換性の確認のみとなる。

- [x] PDF生成統合テストを実行（後方互換性確認）
  ```bash
  uv run pytest tests/test_integration_advanced.py::TestPDFGenerationIntegration -xvs
  ```
  **Expected:** All 4 PDF generation tests pass（修正前から既にパス）

  **テスト結果の解釈:**
  - ✅ パス → 後方互換性OK、既存コードに影響なし
  - ❌ 失敗 → 修正により既存機能が破壊された（要修正）

  **重要:** これらのテストは修正の効果を検証できない。
  Issue #20マージ後に初めて、このテストが真の検証となる。

## 4. Regression Testing

- [x] 全テストスイートを実行
  ```bash
  uv run pytest
  ```
  **Expected:** All 326 tests pass

  **注意:** mainブランチでは全テストが既にパスしている。
  この修正により新たにパスするテストはない（Issue #20マージ後に効果が現れる）。
  目的は既存テストの後方互換性確認のみ。

- [x] カバレッジチェック
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```
  **Expected:** Coverage maintained at 94%+

## 5. Quality Checks

- [x] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/template_engine.py
  ```
  **Expected:** No type errors

- [x] リンティング
  ```bash
  uv run ruff check sphinxcontrib/typst/template_engine.py
  ```
  **Expected:** No linting errors

- [x] フォーマットチェック
  ```bash
  uv run black --check sphinxcontrib/typst/template_engine.py
  ```
  **Expected:** No formatting errors

## 6. Documentation

- [x] CHANGELOG.mdに修正内容を記録
  - Section: `[Unreleased]`
  - Category: `Fixed`
  - Content: Issue #28 fix - codly import added to document files

- [x] Issue #28にクローズコメントを追加
  - Describe the fix
  - Include before/after examples
  - Show test results

## Task Dependencies

- Task 1 (Code Modification) must complete before Task 2 (Verification)
- Task 2 (Verification) must succeed before Task 3 (Integration Tests)
- Task 3 must pass before Task 4 (Regression Testing)
- Task 5 (Quality Checks) can run in parallel with Task 3-4
- Task 6 (Documentation) should be done after all tests pass

## Success Criteria

1. ✅ PDF builder successfully compiles documents with code blocks
2. ✅ All 3 previously failing integration tests pass
3. ✅ No new test failures introduced
4. ✅ Code quality checks pass (mypy, ruff, black)
5. ✅ Coverage maintained at 94%+
6. ✅ CHANGELOG.md updated
7. ✅ Issue #28 closed with detailed comment

## Estimated Effort

- Implementation: ~5 minutes (2 lines added)
- Testing: ~5 minutes (run existing tests)
- Documentation: ~10 minutes (CHANGELOG + Issue comment)
- **Total: ~20 minutes**

## Notes

- This is a minimal, low-risk fix
- Only adds 2 import lines to existing code
- No API changes or breaking changes
- Transparent to end users
- Enables proper PDF generation for all code blocks
