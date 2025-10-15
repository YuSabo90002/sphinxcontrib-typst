# Requirements Document

## Introduction

sphinxcontrib-typst の toctree 翻訳処理において、現在は toctree 内の各 `#include()` ディレクティブに対して個別のコンテンツブロック `#[...]` を生成しています。この実装は機能的には正しいものの、生成される Typst コードに不要な繰り返しが含まれ、可読性が低下しています。

本機能は、複数の `#include()` ディレクティブを単一のコンテンツブロックにまとめることで、生成される Typst コードの可読性と保守性を向上させます。この変更は、出力結果に影響を与えない純粋なコード品質改善 (Code Quality Improvement) であり、Typst のスコープルールに基づいて機能的等価性が保証されています。

**ビジネス価値:**
- 生成される `.typ` ファイルの可読性向上により、デバッグとトラブルシューティングが容易になる
- Typst の慣用的な書き方に準拠することで、ユーザーが生成コードを理解しやすくなる
- 不要な繰り返しを削減し、より簡潔なコード生成を実現する

## Requirements

### Requirement 1: 単一コンテンツブロックによる toctree 出力生成
**Objective:** As a sphinxcontrib-typst ユーザー, I want toctree 内のすべての `#include()` ディレクティブが単一のコンテンツブロックにまとめられた Typst コードが生成されることを望む, so that 生成される `.typ` ファイルの可読性が向上し、Typst の慣用的な書き方に準拠できる

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst が toctree ノードを処理する THEN sphinxcontrib-typst SHALL 単一の開始コンテンツブロック `#[` を生成する
2. WHEN toctree ノードに複数のエントリーが含まれる THEN sphinxcontrib-typst SHALL すべてのエントリーに対して `#include()` ディレクティブを同一コンテンツブロック内に連続して生成する
3. WHEN すべての `#include()` ディレクティブを生成した後 THEN sphinxcontrib-typst SHALL 単一の終了コンテンツブロック `]` を生成する
4. WHERE toctree ノードが処理される THE sphinxcontrib-typst SHALL `#set heading(offset: 1)` ディレクティブをコンテンツブロックの先頭に1回のみ配置する

### Requirement 2: 機能的等価性の保証
**Objective:** As a sphinxcontrib-typst 開発者, I want 新しい実装が既存の実装と機能的に等価であることを望む, so that ユーザーに影響を与えることなく改善を適用できる

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst が生成した Typst ファイルをコンパイルする THEN Typst Compiler SHALL 既存の実装と同一の PDF 出力を生成する
2. WHEN toctree 内のドキュメントが相互にインポートを含む THEN TypstTranslator SHALL 各 `#include()` が独立したスコープを維持することを保証する
3. WHERE heading offset が適用される THE sphinxcontrib-typst SHALL すべての included ドキュメントに対して既存実装と同じ heading レベル調整を適用する
4. IF toctree エントリーが空である THEN TypstTranslator SHALL 既存実装と同様にコンテンツブロックを生成しない

### Requirement 3: 後方互換性の維持
**Objective:** As a sphinxcontrib-typst ユーザー, I want 既存のプロジェクトが変更なく動作し続けることを望む, so that アップグレード時に追加作業が不要になる

#### Acceptance Criteria

1. WHEN 既存の Sphinx プロジェクトで新しいバージョンを使用する THEN sphinxcontrib-typst SHALL すべての既存テストが成功することを保証する
2. WHERE toctree オプション (maxdepth, numbered, caption) が使用される THE sphinxcontrib-typst SHALL これらのオプションを既存実装と同じ方法で処理する
3. IF ユーザーがカスタム toctree テンプレートを使用している THEN sphinxcontrib-typst SHALL テンプレートとの互換性を維持する
4. WHEN 統合テストスイートを実行する THEN すべての統合テスト SHALL 既存実装と同じ結果を生成する

### Requirement 4: コード可読性の向上
**Objective:** As a Typst ユーザー (sphinxcontrib-typst が生成したファイルを手動編集する場合), I want 生成される Typst コードが読みやすく、理解しやすいことを望む, so that 必要に応じて手動で調整できる

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst が `.typ` ファイルを生成する THEN 生成されたファイル SHALL `#set heading(offset: 1)` の繰り返しを含まない
2. WHERE 複数の `#include()` ディレクティブが存在する THE sphinxcontrib-typst SHALL それらを論理的にグループ化して生成する
3. WHEN 3つ以上のドキュメントを含む toctree を処理する THEN sphinxcontrib-typst SHALL 既存実装と比較して生成行数を削減する
4. WHERE Typst コードが生成される THE sphinxcontrib-typst SHALL Typst の公式ドキュメントで推奨される慣用的パターンに従ったコンテンツブロック構造を出力する

### Requirement 5: テストカバレッジの維持
**Objective:** As a sphinxcontrib-typst 開発者, I want 新しい実装が既存のテストカバレッジ基準を満たすことを望む, so that コード品質が維持される

#### Acceptance Criteria

1. WHEN 変更後にテストスイートを実行する THEN sphinxcontrib-typst SHALL 94% 以上のコードカバレッジを維持する
2. WHERE `visit_toctree()` メソッドが変更される THE sphinxcontrib-typst SHALL 変更された行をユニットテストでカバーする
3. IF 新しいエッジケースが特定される THEN sphinxcontrib-typst SHALL そのケースに対する追加テストを提供する
4. WHEN リグレッションテストを実行する THEN sphinxcontrib-typst SHALL 既存のすべてのテスト (313 tests) を成功させる

### Requirement 6: コード品質チェックの実施
**Objective:** As a sphinxcontrib-typst 開発者, I want テスト段階でコード品質チェックが自動的に実行されることを望む, so that 一貫したコード品質が保証される

#### Acceptance Criteria

1. WHEN テスト段階で品質チェックを実行する THEN sphinxcontrib-typst SHALL ruff による lint チェックをエラーなしで完了する
2. WHEN テスト段階で品質チェックを実行する THEN sphinxcontrib-typst SHALL black によるフォーマットチェックをエラーなしで完了する
3. WHEN テスト段階で品質チェックを実行する THEN sphinxcontrib-typst SHALL mypy による型チェックをエラーなしで完了する
4. WHERE 複数の Python バージョンでテストが必要な場合 THE sphinxcontrib-typst SHALL tox を使用して統合テストを実行する
5. WHEN tox で統合テストを実行する THEN sphinxcontrib-typst SHALL Python 3.9, 3.10, 3.11, 3.12 の全バージョンでテストを成功させる
