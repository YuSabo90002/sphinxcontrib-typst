# Proposal: Add Documentation Site

## Why

typsphinxプロジェクトには現在、包括的なドキュメントサイトが存在しません。ユーザーは以下の課題に直面しています：

- インストール、設定、使用方法を学ぶ集約されたリソースがない
- サンプルやベストプラクティスを参照する場所がない
- API リファレンスが整理されていない
- オフライン参照用のPDF版ドキュメントがない

包括的なドキュメントサイトを提供することで：

- ユーザーのオンボーディング体験が向上
- サポート質問が減少
- プロジェクトの機能を効果的にショーケース
- より多くのユーザーを引き付けるプロフェッショナルな外観を提供

さらに、typsphinx自体を使用してドキュメントを生成することで、拡張機能の能力を実証（ドッグフーディング）できます。

## What Changes

### 1. Documentation Structure

`docs/` ディレクトリに包括的なドキュメントを作成：

- **Getting Started**: インストール、クイックスタートガイド
- **User Guide**: 設定オプション、ビルダー（typst/typstpdf）、テンプレート
- **Examples**: コード例とビジュアル出力
- **API Reference**: docstringから自動生成
- **Contributing Guide**: 開発セットアップ、テスト、ガイドライン
- **Changelog**: バージョン履歴とマイグレーションガイド

### 2. GitHub Pages Integration

- GitHub Pages（https://yusabo90002.github.io/typsphinx/）でドキュメントをホスト
- GitHub Actions ワークフローで自動的にドキュメントをビルド・デプロイ
- HTML版（Sphinxテーマ使用）とPDF版（typsphinxビルダー使用）の両方を生成

### 3. PDF Distribution

- `typstpdf` ビルダーでPDF版ドキュメントを生成
- 各バージョンのPDFをGitHub Releasesでホスト
- ドキュメントサイトにダウンロードリンクを提供

### 4. Documentation Stack

- Sphinx でドキュメントをビルド（typsphinx拡張を使用してドッグフーディング）
- HTML版にはSphinxテーマ（furo、sphinx-rtd-theme、sphinx-book-themeなど）を使用
- PDF版には `typstpdf` ビルダーを使用
- GitHub Actions で自動ビルド・デプロイ

## Impact

### Affected specs

新しいcapabilityを作成：
- `documentation-site`: ドキュメントサイトの構造、ビルド、デプロイ

### Affected code

新規ファイル：
- `docs/source/` - ドキュメントソース（.rstファイル）
- `docs/source/conf.py` - Sphinx設定
- `.github/workflows/docs.yml` - ドキュメントビルド・デプロイワークフロー
- `docs/Makefile` - ビルドコマンド

既存ファイル変更：
- `README.md` - ドキュメントサイトへのリンク追加
- `pyproject.toml` - ドキュメント依存関係追加（sphinx-themeなど）

### Breaking changes

なし - 既存機能に影響なし

## Alternatives Considered

1. **ReadTheDocs**: 人気があるが外部サービス登録が必要
2. **GitBook**: 無料枠に制限がある商用サービス
3. **MkDocs**: Sphinxベースではない別のドキュメントシステム
4. **手動PDF配布**: 自動化が少なく、メンテナンスが困難

GitHub Pagesを選択した理由：
- 無料でGitHubとよく統合されている
- GitHub Actionsとのシームレスな連携
- 既存のSphinxワークフローを活用できる
- typsphinxの能力を実証できる
