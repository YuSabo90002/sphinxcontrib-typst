# 提案: PDFビルダーのcodlyインポート修正

**Change ID:** `fix-codly-import`
**ステータス:** 提案中
**作成日:** 2025-10-22
**関連Issue:** [#28](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/28)

## Why

`typstpdf`ビルダーが「`TypstError: unknown variable: codly`」エラーでPDF生成に失敗する問題が発生しています。この問題により：

- すべてのコードブロックを含むドキュメントのPDF生成が失敗する
- 3つの統合テストが失敗する（`test_pdf_file_generated`、`test_pdf_file_not_empty`、`test_pdf_has_magic_number`）
- Issue #20で修正したコードブロックオプション（`:linenos:`、`:caption:`、`:name:`）がPDF出力で検証できない

根本原因は、生成されるドキュメントファイル（`.typ`）にcodlyパッケージのインポートが含まれていないためです。テンプレートファイル（`_template.typ`）にはcodlyが正しくインポートされていますが、ドキュメントファイルでトランスレータが生成する`#codly()`や`#codly-range()`関数を使用する際、codlyがスコープ内に存在しません。

## What Changes

`template_engine.py`の`generate_document()`メソッドに、codlyパッケージのインポートを追加します。

**変更内容:**
- `template_engine.py`の293-294行目（essential imports section）に2行追加
- 既存の`mitex`と`gentle-clues`インポートと同様に、codlyをドキュメントレベルの必須インポートとして追加

**影響するspec:**
- `specs/document-conversion/spec.md`: ドキュメントレベルでのパッケージインポート要件を修正

## 概要

生成されるTypstドキュメントファイルにcodlyパッケージのインポートを追加し、PDF生成時にコードブロック関連の関数が正しく動作するようにします。

## 問題の検証結果

**検証日:** 2025-10-22

### mainブランチ（現在）

**動作:**
- トランスレータがcodly関数を使用しない
- PDFビルド: ✅ 成功
- 統合テスト: ✅ 全てパス

**結果:**
```bash
$ uv run pytest tests/test_integration_advanced.py::TestPDFGenerationIntegration -v
# 4 passed
```

### fix/issue-20ブランチ（Issue #20修正後）

**動作:**
- トランスレータが`#codly(number-format: none)`を生成
- ドキュメントファイルにcodly importなし

**PDFビルド結果:**
```bash
$ uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test
Typst compilation failed: TypstError: unknown variable: codly
ERROR: Failed to compile index.typ
```

**統合テスト結果:**
```bash
$ uv run pytest tests/test_integration_advanced.py::TestPDFGenerationIntegration::test_pdf_file_generated -xvs
# FAILED - AssertionError: index.pdf should be generated
```

**生成されたindex.typ:**
```typst
// Essential package imports
#import "@preview/mitex:0.2.4": mi, mitex
#import "@preview/gentle-clues:1.2.0": *
// ❌ codly importなし

== Code Example
#codly(number-format: none)  // ❌ エラー: unknown variable
```python
def hello():
    print("Hello, World!")
```
```

**結論:** Issue #20の修正により、codly関数が使用されるようになったため、ドキュメントファイルへのcodly import追加が必須となった。

## 問題の詳細

### 現在の挙動

**テンプレートファイル（`_template.typ`）:** ✅ codlyを正しくインポート
```typst
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#show: codly-init.with()
#codly(languages: codly-languages)
```

**ドキュメントファイル（`index.typ`など）:** ❌ codlyインポートが欠落
```typst
// Essential package imports
#import "@preview/mitex:0.2.4": mi, mitex
#import "@preview/gentle-clues:1.2.0": *

#import "_template.typ": project
// ここにcodlyインポートがない！
```

**トランスレータの出力:** codly関数を使用するがインポートがない
```typst
#codly(number-format: none)  // ❌ エラー: unknown variable
```python
def hello():
    return "world"
```
```

**エラーメッセージ:**
```
Typst compilation failed at /tmp/build/tmp2aov3kpp.typ: TypstError: unknown variable: codly
Location: /tmp/build/tmp2aov3kpp.typ
Details: unknown variable: codly
```

### 期待される挙動

**ドキュメントファイル（修正後）:**
```typst
// Essential package imports
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#import "@preview/mitex:0.2.4": mi, mitex
#import "@preview/gentle-clues:1.2.0": *

#import "_template.typ": project

#show: project.with(...)

// codly関数が正しく動作する
#codly(number-format: none)
```python
def hello():
    return "world"
```
```

**結果:** PDF生成成功、エラーなし

## 根本原因

`sphinxcontrib/typst/template_engine.py`の`generate_document()`メソッド（293-294行目）で、ドキュメントレベルの必須インポートとして`mitex`と`gentle-clues`のみが追加され、codlyが含まれていません。

```python
# 現在のコード（293-294行目）
output_parts.append("// Essential package imports")
output_parts.append('#import "@preview/mitex:0.2.4": mi, mitex')
output_parts.append('#import "@preview/gentle-clues:1.2.0": *')
# codlyが欠落！
```

トランスレータ（`translator.py`）は以下の場面でcodly関数を使用します：
1. `:linenos:`オプションなしのコードブロック → `#codly(number-format: none)`を生成
2. `:emphasize-lines:`オプション付きコードブロック → `#codly-range(...)`を生成
3. すべてのコードブロック → テンプレートでcodlyが初期化されているが、ドキュメントスコープで利用不可

## 提案する解決策

`template_engine.py`の必須インポートセクションにcodlyインポートを追加します：

```python
# 修正後のコード（293-296行目）
output_parts.append("// Essential package imports")
output_parts.append('#import "@preview/codly:1.3.0": *')
output_parts.append('#import "@preview/codly-languages:0.1.1": *')
output_parts.append('#import "@preview/mitex:0.2.4": mi, mitex')
output_parts.append('#import "@preview/gentle-clues:1.2.0": *')
```

### 変更のスコープ

**対象ファイル:**
- `sphinxcontrib/typst/template_engine.py` - 2行追加

**対象外:**
- `translator.py` - 変更不要（既に正しくcodly関数を使用）
- `templates/base.typ` - 変更不要（既にcodlyをインポート）
- `writer.py` - 変更不要（included documentsでは既にcodlyをインポート）

### 動作の変更点

- ドキュメントファイルにcodlyパッケージがインポートされる
- PDF生成が成功する
- 統合テストがパスする
- Issue #20の機能がPDF出力で検証可能になる

## 影響評価

### メリット

1. **PDF生成の修正** - すべてのコードブロックを含むドキュメントでPDF生成が成功
2. **統合テストの修正** - 3つの失敗していたテストがパス
3. **一貫性の向上** - codlyが`mitex`/`gentle-clues`と同様に扱われる（すべて必須インポート）
4. **破壊的変更なし** - インポートを追加するのみで、既存の動作を変更しない
5. **将来対応** - 現在および将来のすべてのコードブロック機能をサポート

### リスク評価: 極めて低

- 変更箇所が限定的（2行追加のみ）
- APIの変更なし（内部実装の詳細）
- ユーザー向けの変更なし（透過的な修正）
- パフォーマンスへの影響なし（インポートは軽量）

### 後方互換性

- ✅ 完全な後方互換性あり
- インポートを追加するのみ
- 既存の機能に影響なし
- ドキュメント再生成で自動的に修正される

## テスト戦略

### 重要な注意事項

**現在の統合テストの制限:**
- `tests/fixtures/integration_basic`はmainブランチのコード（codly関数を使わない）でテストされる
- したがって、**修正前後でテストが通ってしまう**（codly importがなくても問題なし）
- **Issue #20の修正をマージした後**に初めて、この修正の必要性が統合テストで検出される

**対応策:**
1. **手動検証テスト**: Issue #20ブランチでPDFビルドを実行し、修正前は失敗、修正後は成功することを確認
2. **新規テストフィクスチャ作成**: codly関数を含むTypstファイルを直接使用するテストを追加（オプション）
3. **Issue #20マージ後の検証**: Issue #20をマージした後、このPRで統合テストがパスすることを確認

### ユニットテスト
- `generate_document()`の出力にcodlyインポートが含まれることを確認
- インポートの順序が正しいことを確認（codly → mitex → gentle-clues）

### 統合テスト（現状）
- 既存テストはパスするが、修正の効果は検証できない:
  - `test_pdf_file_generated` - ✅ パス（codly使用なし）
  - `test_pdf_file_not_empty` - ✅ パス（codly使用なし）
  - `test_pdf_has_magic_number` - ✅ パス（codly使用なし）

### 手動検証テスト（必須）

**修正前（Issue #20ブランチ）:**
```bash
# Issue #20ブランチに切り替え
git checkout fix/issue-20-code-block-options

# PDFビルド実行
uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test-before

# 期待結果: エラー "unknown variable: codly"
```

**修正後（Issue #28 + Issue #20）:**
```bash
# Issue #28の修正を適用
# template_engine.pyにcodly importを追加

# PDFビルド実行
uv run sphinx-build -b typstpdf tests/fixtures/integration_basic /tmp/test-after

# 期待結果: PDF生成成功、codlyインポートが含まれる
cat /tmp/test-after/index.typ | head -10
# 確認: #import "@preview/codly:1.3.0": *
```

### 追加テスト（オプション）

codly関数を直接含むTypstファイルでテストする新しいフィクスチャを作成:

```python
def test_pdf_with_codly_functions(tmp_path):
    """Test PDF compilation with codly functions in output."""
    # Create a Typst file that uses codly functions
    typst_content = """
    #import "@preview/codly:1.3.0": *
    #codly(number-format: none)
    ```python
    def hello():
        print("world")
    ```
    """
    # Test compilation succeeds
```

### リグレッションテスト
- フルテストスイート実行（326テスト → すべてパス期待）
- カバレッジ維持（94%+）
- **重要**: Issue #20マージ後、統合テストが初めて真の検証となる

## 検討した代替案

### 1. テンプレートからcodlyをエクスポート

**アプローチ:** テンプレートファイルでcodlyをエクスポートし、ドキュメントファイルでインポート

```typst
// template.typ
#import "@preview/codly:1.3.0": *
// ... codlyをエクスポート

// index.typ
#import "_template.typ": project, codly, codly-range
```

**却下理由:**
- より複雑な実装
- テンプレート構造の変更が必要
- ユーザー定義テンプレートとの互換性問題
- 最小限の実装を優先

### 2. トランスレータでcodly使用を削除

**アプローチ:** `translator.py`でcodly関数を使用しないよう変更

**却下理由:**
- コードブロック機能の削減（Issue #20の修正を無効化）
- Typstのコードハイライト機能が失われる
- 後退的な解決策
- プロジェクトの目的に反する

### 3. 条件付きcodlyインポート

**アプローチ:** コードブロックが存在する場合のみcodlyをインポート

**却下理由:**
- より複雑な実装（ドキュメントツリーの事前スキャン必要）
- パフォーマンスへの影響
- 最小限の実装を優先（codlyインポートは軽量）
- 必要性が低い（ほとんどのドキュメントにコードブロックがある）

## 実装計画

### Phase 1: コード変更
1. `template_engine.py`の293行目の後に2行追加
2. コミットメッセージ: "fix: add codly imports to document-level essential imports"

### Phase 2: テスト
1. PDFビルドのテスト（`integration_basic`フィクスチャ）
2. 統合テストの実行
3. フルテストスイートの実行

### Phase 3: ドキュメント
1. CHANGELOG.mdに修正内容を記録
2. Issue #28にクローズコメントを追加

### 予想作業時間
- 実装: ~5分（2行追加）
- テスト: ~5分（既存テスト実行）
- ドキュメント: ~10分（CHANGELOG + Issueコメント）
- **合計: ~20分**

## 関連情報

- **修正するIssue:** [#28 - PDF builder fails with "unknown variable: codly" error](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/28)
- **有効化するIssue:** [#20 - Code block directive options support](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/20)
- **関連コード:**
  - `sphinxcontrib/typst/template_engine.py` - ドキュメント生成
  - `sphinxcontrib/typst/translator.py` - codly関数使用
  - `sphinxcontrib/typst/templates/base.typ` - テンプレートでのcodly初期化
- **関連テスト:**
  - `tests/test_integration_advanced.py::TestPDFGenerationIntegration`
