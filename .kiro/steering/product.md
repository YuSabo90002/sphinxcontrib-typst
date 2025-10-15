# Product Overview

## Product Description

sphinx-typst は、Sphinx ドキュメントジェネレータと Typst タイプセッティングシステムを統合する拡張機能です。Sphinx の強力なドキュメント生成機能と Typst のモダンな組版機能を組み合わせ、高品質な技術文書の作成を可能にします。

## Core Features

- **Sphinx to Typst Conversion**: Sphinx ドキュメント(reStructuredText/Markdown)を Typst フォーマットに変換
- **Dual Builder Integration**:
  - `typst` ビルダー: Typst マークアップファイルを生成
  - `typstpdf` ビルダー: PDF を直接生成（外部 Typst CLI 不要）
- **Self-Contained PDF Generation**: typst-py による自己完結型 PDF 生成（外部ツール不要）
- **カスタマイズ可能な出力**: Typst テンプレートとスタイルのカスタマイズをサポート
- **相互参照とインデックス**: Sphinx の相互参照、インデックス、目次機能を Typst で再現
- **コードハイライト**: codly パッケージによるシンタックスハイライトと行番号表示
- **数式サポート**: mitex による LaTeX 数式またはネイティブ Typst 数式
- **図表管理**: 画像、表、図表の埋め込みと参照管理
- **マルチドキュメント対応**: toctree による `#include()` 統合
- **ネストされたtoctreeサポート**: 相対パスによる正確な `#include()` 生成（Issue #5対応）

## Target Use Case

### Primary Use Cases

1. **技術文書の高品質組版**
   - API ドキュメント、技術仕様書などを Typst でプロフェッショナルな PDF として出力
   - Sphinx の自動生成機能と Typst の美しい組版を組み合わせる

2. **学術的ドキュメント作成**
   - 研究論文、技術レポートなどの執筆で Sphinx のドキュメント管理と Typst の組版品質を活用
   - LaTeX の複雑さを避けつつ高品質な出力を実現

3. **マルチフォーマット出力**
   - 同一ソースから HTML、PDF(Typst)、ePub などの複数フォーマットを生成
   - Sphinx のエコシステムを活用しながら Typst の利点を享受

### Target Users

- Python ドキュメント作成者で、より美しい PDF 出力を求める開発者
- Sphinx を使用しているが LaTeX の設定に苦労しているチーム
- モダンな組版システム(Typst)を既存の Sphinx ワークフローに統合したいユーザー
- 技術文書と学術文書の両方を扱うドキュメンテーションチーム

## Key Value Proposition

### Unique Benefits

1. **モダンな組版エンジン**
   - LaTeX より高速で、より直感的な Typst を Sphinx から利用可能
   - コンパイル時間の大幅な短縮

2. **自己完結型 PDF 生成**
   - typst-py 統合により外部 Typst CLI のインストール不要
   - `sphinx-build -b typstpdf` で直接 PDF を生成

3. **既存 Sphinx エコシステムの活用**
   - Sphinx の豊富な拡張機能、ディレクティブ、ドメインをそのまま使用
   - 既存の Sphinx プロジェクトに容易に統合
   - 自動検出による拡張登録（`extensions` リストへの追加はオプショナル）

4. **保守性の向上**
   - Typst のシンプルな記法により、テンプレートのカスタマイズが容易
   - LaTeX に比べてデバッグとトラブルシューティングが簡単

5. **一貫したワークフロー**
   - Sphinx の標準的なビルドコマンドで Typst 出力を生成
   - CI/CD パイプラインへの統合が容易

### Differentiators

- **Sphinx + Typst の初の統合**: Sphinx と Typst を繋ぐ専用ソリューション
- **Python エコシステム統合**: Python プロジェクトのドキュメントワークフローにシームレスに統合
- **拡張性**: Sphinx と Typst 両方の拡張メカニズムを活用可能
- **高品質実装**: 313 テスト、94% カバレッジで検証済み（Issue #5実装により27テスト追加）
- **ベータリリース**: PyPI で配布中 (v0.1.0b1)、早期採用とフィードバックを歓迎

## Release Status

**Current Version**: v0.1.0b1 (Beta)
- **Status**: ベータ版 - テストと早期採用に適している
- **Test Coverage**: 94% (313 tests)
  - ユニットテスト: 10件（相対パス計算）
  - 統合テスト: 10件（Sphinxビルド検証）
  - E2Eテスト: 4件（PDF生成検証）
  - カバレッジテスト: 3件（パラメータ変換）
- **Distribution**: PyPI で利用可能
- **Production Readiness**: 12/13 要件を実装、エンタープライズ使用には v1.0 待機を推奨
- **Recent Improvements**:
  - Issue #5修正: ネストされたtoctreeの相対パス生成
  - デバッグログ機能追加: `-vv`フラグで詳細ログ出力
  - E2Eコンパイルテスト: typst-pyによるPDF生成検証
