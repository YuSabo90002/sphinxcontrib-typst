# Implementation Plan

## Overview

本実装計画は、`simplify-toctree-content-block`機能の実装タスクを定義します。既存の`TypstTranslator.visit_toctree()`メソッドを変更し、複数の`#include()`ディレクティブを単一のコンテンツブロック内に配置することで、生成されるTypstコードの可読性を向上させます。

## Implementation Tasks

- [x] 1. toctree処理ロジックの変更
- [x] 1.1 コンテンツブロック生成位置の変更
  - ループ前に単一の開始コンテンツブロック`#[`を生成する処理を追加
  - ループ前に`#set heading(offset: 1)`ディレクティブを1回のみ生成
  - ループ内では各entryに対して`#include()`ディレクティブのみを生成
  - ループ後に単一の終了コンテンツブロック`]`を生成する処理を追加
  - 空のentriesの場合は何も生成せず`SkipNode`を発生させる既存動作を維持
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 1.2 相対パス計算ロジックの統合
  - Issue #5で実装済みの`_compute_relative_include_path()`メソッドを変更なしで使用
  - 各`#include()`生成時に相対パスを正確に計算
  - ネストされたtoctree構造での相対パス計算を正しく処理
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 1.3 デバッグログ出力の維持
  - toctree処理開始時にentries数をログ出力
  - 現在のドキュメント名とentry一覧をログ出力
  - 各`#include()`生成時に対象ドキュメント名と相対パスをログ出力
  - 既存のログ記録パターンを維持
  - _Requirements: Error Handling - Monitoring_

- [x] 2. ユニットテストの作成と更新
- [x] 2.1 新規ユニットテストの追加
  - 複数エントリーを持つtoctreeで単一コンテンツブロックが生成されることを検証
  - `#[`と`]`がそれぞれ1回のみ出現することを検証（`count()`メソッド使用）
  - 全ての`#include()`が同一ブロック内に存在することを検証（文字列スライスと`in`演算子使用）
  - `#set heading(offset: 1)`が1回のみ出現することを検証（正規表現カウント使用）
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2.2 行数削減の検証テスト
  - 3つのエントリーを持つtoctreeを処理
  - 生成される行数が期待値（5行: 開始1行 + offset1行 + includes3行 + 終了1行）と一致することを検証
  - 既存実装と比較して行数が削減されることを確認
  - _Requirements: 4.3_

- [x] 2.3 エッジケースのテスト
  - 空のentriesを持つtoctreeで何も生成されないことを検証（`SkipNode`発生）
  - 単一エントリーのtoctreeで単一ブロックが生成されることを検証
  - 10個以上のエントリーを持つtoctreeでも正しく処理されることを検証
  - _Requirements: 2.4, 5.3_

- [x] 2.4 既存ユニットテストの更新
  - `test_toctree_with_heading_offset()`のassertionを単一ブロック構造に更新
  - `test_toctree_generates_include_directives()`のassertionを更新
  - 複数ブロック想定のテストケースを単一ブロック想定に修正
  - 全てのassertionで生成される構造の変更を反映
  - _Requirements: 3.1, 5.4_

- [x] 3. 統合テストの実行と検証
- [x] 3.1 既存フィクスチャでのビルド検証
  - `integration_nested_toctree`フィクスチャでSphinxビルドを実行
  - `integration_multi_level`フィクスチャでビルドを実行
  - `integration_sibling`フィクスチャでビルドを実行
  - 全てのビルドが成功し、`.typ`ファイルが生成されることを確認
  - _Requirements: 3.4_

- [x] 3.2 生成Typstファイルの構造検証
  - 各フィクスチャで生成された`.typ`ファイルを読み込み
  - 正規表現で単一コンテンツブロック構造を検証（`#\[\s*#set heading.*?(?:#include.*?\n)+\]`パターン）
  - toctreeオプション（maxdepth, numbered, caption）が正しく処理されることを確認
  - _Requirements: 3.2, 4.1, 4.2_

- [x] 3.3 カスタムテンプレート互換性の検証
  - カスタムテンプレートを使用したプロジェクトでビルドを実行
  - テンプレート処理が既存実装と同じ動作をすることを確認
  - テンプレート変数のマッピングが正しく機能することを検証
  - _Requirements: 3.3_

- [x] 4. E2Eテストの実施
- [x] 4.1 Typstコンパイル成功の検証
  - 生成された`.typ`ファイルをtypst-pyでコンパイル
  - PDF生成が成功することを確認（ファイルサイズ > 0）
  - PDFマジックナンバー`%PDF`が存在することを検証
  - コンパイルエラーが発生しないことを確認
  - _Requirements: 2.1, 2.2_

- [x] 4.2 PDF出力の機能的等価性検証
  - 新実装で生成したPDFと既存実装のPDFを比較
  - ページ数が同一であることを確認
  - 見出しレベルが同一であることを確認（`#set heading(offset: 1)`の効果検証）
  - テキスト内容が同一であることを確認
  - _Requirements: 2.1, 2.3_

- [x] 5. コード品質チェックの実施
- [x] 5.1 Lintチェックの実行
  - `uv run ruff check sphinxcontrib/typst/translator.py`を実行
  - エラーが0件であることを確認
  - 警告があれば修正または抑制理由を明記
  - _Requirements: 6.1_

- [x] 5.2 フォーマットチェックの実行
  - `uv run black --check sphinxcontrib/typst/translator.py`を実行
  - フォーマット違反が0件であることを確認
  - 必要に応じて`uv run black sphinxcontrib/typst/translator.py`でフォーマット適用
  - _Requirements: 6.2_

- [x] 5.3 型チェックの実行
  - `uv run mypy sphinxcontrib/typst/translator.py`を実行
  - 型エラーが0件であることを確認
  - Python 3.9+互換の型ヒント記法を使用（`Optional[str]`形式）
  - _Requirements: 6.3_

- [ ] 6. 複数バージョンテストの実行
- [ ] 6.1 Toxによる統合テスト
  - `uv run tox`を実行してPython 3.9, 3.10, 3.11, 3.12で全テストを実行
  - 全てのPythonバージョンでテストが成功することを確認
  - 各環境で313テスト + 新規テストが全て成功することを検証
  - _Requirements: 6.4, 6.5_

- [x] 6.2 コードカバレッジの確認
  - `uv run pytest --cov=sphinxcontrib.typst --cov-report=term --cov-report=html`を実行
  - コードカバレッジが94%以上であることを確認
  - `visit_toctree()`メソッドの変更行が全てカバーされていることを確認
  - カバレッジレポートをHTMLで生成して詳細を確認
  - _Requirements: 5.1, 5.2_

- [x] 7. リグレッションテストの実行
- [x] 7.1 既存テストスイートの全実行
  - `uv run pytest`で全313テスト + 新規テストを実行
  - 全てのテストが成功することを確認
  - テスト実行時間が既存実装と同等かそれ以下であることを確認
  - _Requirements: 5.4_

- [x] 7.2 後方互換性の最終確認
  - toctreeオプション（maxdepth, numbered, caption）を使用したプロジェクトでテスト実行
  - 既存のSphinxプロジェクトで新バージョンを使用してビルド成功を確認
  - カスタムテンプレートを使用したプロジェクトで動作確認
  - 全ての既存ユーザーケースが動作することを検証
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

## Success Criteria

以下の全ての基準を満たすことで実装完了とします：

### 機能要件
- [ ] 単一コンテンツブロック内に全`#include()`が配置される
- [ ] `#set heading(offset: 1)`が1回のみ出力される
- [ ] 生成される行数が既存実装より削減される

### 品質要件
- [ ] ruff lint チェック: 0 errors
- [ ] black フォーマットチェック: すべてのファイルがフォーマット済み
- [ ] mypy 型チェック: 0 type errors
- [ ] pytest 全テスト: 313 + 新規テストすべて成功
- [ ] tox 統合テスト: Python 3.9-3.12 全バージョンで成功
- [ ] コードカバレッジ: 94%以上維持

### 後方互換性
- [ ] 既存の全313テストが成功
- [ ] PDF出力が既存実装と機能的に等価
- [ ] toctreeオプション（maxdepth, numbered, caption）が正常動作
- [ ] カスタムテンプレートとの互換性維持

### パフォーマンス
- [ ] `add_text()`呼び出し回数が削減（N×4回 → 2+N回）
- [ ] テスト実行時間が既存実装と同等以下

## Requirements Coverage

### Requirement 1: 単一コンテンツブロックによる toctree 出力生成
- **Tasks**: 1.1, 2.1
- **Acceptance Criteria**: 1.1, 1.2, 1.3, 1.4

### Requirement 2: 機能的等価性の保証
- **Tasks**: 1.2, 4.1, 4.2
- **Acceptance Criteria**: 2.1, 2.2, 2.3, 2.4

### Requirement 3: 後方互換性の維持
- **Tasks**: 7.2, 3.1, 3.2, 3.3
- **Acceptance Criteria**: 3.1, 3.2, 3.3, 3.4

### Requirement 4: コード可読性の向上
- **Tasks**: 1.1, 2.2, 3.2
- **Acceptance Criteria**: 4.1, 4.2, 4.3, 4.4

### Requirement 5: テストカバレッジの維持
- **Tasks**: 2.1, 2.2, 2.3, 2.4, 6.2, 7.1
- **Acceptance Criteria**: 5.1, 5.2, 5.3, 5.4

### Requirement 6: コード品質チェックの実施
- **Tasks**: 5.1, 5.2, 5.3, 6.1
- **Acceptance Criteria**: 6.1, 6.2, 6.3, 6.4, 6.5

## Implementation Notes

### 推奨実装順序
1. **Phase 1 (Tasks 1.1-1.3)**: コアロジック変更 - 約1時間
2. **Phase 2 (Tasks 2.1-2.4)**: ユニットテスト - 約2-3時間
3. **Phase 3 (Tasks 3.1-3.3)**: 統合テスト - 約2時間
4. **Phase 4 (Tasks 4.1-4.2)**: E2Eテスト - 約1-2時間
5. **Phase 5 (Tasks 5.1-5.3)**: コード品質チェック - 約30分
6. **Phase 6 (Tasks 6.1-6.2)**: 複数バージョンテスト - 約1-2時間
7. **Phase 7 (Tasks 7.1-7.2)**: リグレッションテスト - 約1時間

### TDD Approach
本実装では、以下のTDDサイクルを推奨します：
1. **Red**: 新規テストを作成（Task 2.1）
2. **Green**: 最小限の実装で成功させる（Task 1.1）
3. **Refactor**: コード品質を確認（Tasks 5.1-5.3）
4. **Repeat**: 統合テスト、E2Eテストで検証（Tasks 3.x, 4.x）

### Critical Path
- Task 1.1（コンテンツブロック生成位置の変更）が最も重要
- Task 2.4（既存テスト更新）が後続タスクの前提条件
- Task 6.1（Tox統合テスト）が最終的な品質保証

### 変更範囲
- **変更ファイル**: `sphinxcontrib/typst/translator.py` (lines 962-1018)
- **変更メソッド**: `visit_toctree()`
- **変更行数**: 約15行

### リスク管理
- 各タスク完了後に全テストスイートを実行（`uv run pytest`）
- コード品質チェックを早期に実施（Task 5完了後）
- E2Eテストで機能的等価性を確認（Task 4完了後）
