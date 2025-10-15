# Requirements Document

## Introduction

このドキュメントは、sphinxcontrib-typst における Issue #5 の修正要件を定義します。ネストされたtoctreeディレクティブを含むドキュメントがサブディレクトリに配置された際に、生成される `#include()` ディレクティブのパスが不適切になる問題を解決します。

### 背景
現在の実装では、toctreeエントリに対して `#include()` パスを生成する際、プロジェクトルートからの絶対パス（docname）をそのまま使用しています。これにより、サブディレクトリ内のドキュメントから同じディレクトリ内の他のドキュメントを参照する場合、不正なパスが生成されます。

### ビジネス価値
- マルチレベルのドキュメント階層をサポートし、大規模プロジェクトでの使用を可能にする
- Typstコンパイルエラーを解消し、PDF生成の信頼性を向上させる
- ネストされたサブディレクトリによる論理的なドキュメント構造をサポート

## Requirements

### Requirement 1: 相対パス計算の実装
**Objective:** TypstTranslatorとして、toctreeエントリの `#include()` パスを現在のドキュメントからの相対パスとして生成したい、それによりネストされたディレクトリ構造で正しいTypstコンパイルが可能になるため。

#### Acceptance Criteria

1. WHEN toctree ノードを処理する際、TypstTranslator SHALL 現在のドキュメント（`self.builder.current_docname`）の位置を取得する
2. IF 現在のドキュメントがサブディレクトリ内にある場合、TypstTranslator SHALL 現在のドキュメントのディレクトリパスを抽出する
3. WHEN toctree エントリのパスを生成する際、TypstTranslator SHALL 現在のドキュメントディレクトリからtoctreeエントリへの相対パスを計算する
4. IF 現在のドキュメントとtoctreeエントリが同じディレクトリにある場合、TypstTranslator SHALL ファイル名のみを `#include()` パスとして使用する
5. IF toctreeエントリが異なるディレクトリにある場合、TypstTranslator SHALL 相対パス（`../` や `subdir/` を含む）を `#include()` パスとして使用する

### Requirement 2: 既存機能の互換性維持
**Objective:** 開発者として、既存の動作しているtoctreeパターンが引き続き正しく動作することを確認したい、それにより既存プロジェクトへの影響を防ぐため。

#### Acceptance Criteria

1. WHEN ルートディレクトリのドキュメントが同じディレクトリ内のドキュメントをtoctreeで参照する場合、TypstTranslator SHALL ファイル名のみを `#include()` パスとして生成する
2. WHEN ルートディレクトリのドキュメントがサブディレクトリ内のドキュメントをtoctreeで参照する場合、TypstTranslator SHALL サブディレクトリパスを含む相対パスを `#include()` パスとして生成する
3. WHERE 既存のテストケース（同じディレクトリ、サブディレクトリへの参照）において、TypstTranslator SHALL 現在と同じ出力を生成する

### Requirement 3: ネストされたtoctreeのサポート
**Objective:** ドキュメント作成者として、サブディレクトリ内のドキュメントで同じディレクトリ内の他のドキュメントをtoctreeで参照できるようにしたい、それにより論理的なドキュメント階層を構築できるため。

#### Acceptance Criteria

1. WHEN `chapter1/index.rst` が同じディレクトリ内の `section1.rst` と `section2.rst` をtoctreeで参照する場合、TypstTranslator SHALL `chapter1/index.typ` に `#include("section1.typ")` と `#include("section2.typ")` を生成する
2. WHEN サブディレクトリ内のドキュメントが別のサブディレクトリのドキュメントを参照する場合、TypstTranslator SHALL 適切な相対パス（`../other_dir/doc.typ` など）を生成する
3. IF toctreeエントリが親ディレクトリのドキュメントを参照する場合、TypstTranslator SHALL `../` プレフィックスを含む相対パスを生成する

### Requirement 4: Typstコンパイル検証
**Objective:** 品質保証担当者として、生成されたTypstファイルが正しくコンパイルできることを確認したい、それによりPDF生成の信頼性を保証するため。

#### Acceptance Criteria

1. WHEN 修正後のコードでネストされたtoctree構造を持つプロジェクトをビルドする場合、Typst SHALL エラーなくコンパイルを完了する
2. WHERE `chapter1/index.typ` が同じディレクトリ内のファイルを `#include()` する場合、Typst SHALL ファイルを正しく検出して読み込む
3. IF 生成されたTypstファイルに相対パスが含まれる場合、Typst SHALL ファイルシステム上の正しい位置からファイルを読み込む

### Requirement 5: テストカバレッジ
**Objective:** 開発チームとして、すべてのtoctreeパターンが適切にテストされることを確認したい、それにより将来的な回帰を防ぐため。

#### Acceptance Criteria

1. WHERE テストスイートにおいて、TypstTranslator SHALL 以下のシナリオをカバーする：
   - 同じディレクトリ内のtoctree参照
   - サブディレクトリへのtoctree参照
   - ネストされたtoctree（サブディレクトリ内のドキュメントから同じディレクトリへの参照）
   - 複数レベルのネスト（3階層以上のディレクトリ構造）
2. WHEN 各テストケースを実行する場合、テスト SHALL 生成された `#include()` パスが期待される相対パスと一致することを検証する
3. WHERE 統合テストにおいて、テスト SHALL 生成されたTypstファイルが実際にTypstコンパイラでコンパイル可能であることを検証する

## Technical Constraints

### 実装上の制約
- Python標準ライブラリの `pathlib.Path` を使用して相対パス計算を行う（`Path.relative_to()` または `os.path.relpath()` のpathlib版）
- `self.builder.current_docname` から現在のドキュメント位置を取得する
- 既存のコード構造（`visit_toctree` メソッド）内で実装を行う
- 型ヒント（Type Hints）を適切に使用する
- モダンなPythonスタイルとして `pathlib` を積極的に利用する

### 互換性の制約
- Sphinx 5.0+ との互換性を維持する
- 既存のテストケース（286テスト）がすべてパスする
- 既存のドキュメント構造に対する後方互換性を保つ

## Out of Scope

以下は本要件のスコープ外とします：

1. toctree以外のディレクティブにおける相対パス処理
2. Typstの `#include()` 以外のインポート機能のサポート
3. シンボリックリンクやハードリンクへの対応
4. 絶対パス指定のサポート
5. プロジェクトルート外のファイル参照

## Success Metrics

修正の成功を以下の指標で測定します：

1. Issue #5 で報告されたテストケースがすべてパスする
2. 既存のテストスイート（286テスト）がすべてパスする
3. 新規追加されたテストケースがネストされたtoctreeシナリオをカバーする
4. 生成されたTypstファイルがTypstコンパイラでエラーなくコンパイルできる
5. コードカバレッジが93%以上を維持する
