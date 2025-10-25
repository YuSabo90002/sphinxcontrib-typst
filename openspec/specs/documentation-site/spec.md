# documentation-site Specification

## Purpose
TBD - created by archiving change add-documentation-site. Update Purpose after archive.
## Requirements
### Requirement: ドキュメント構造

システムは、包括的なドキュメントサイトの構造を提供しなければならない (SHALL)。

#### Scenario: 基本的なドキュメント構造

- **GIVEN** プロジェクトルートに `docs/` ディレクトリが存在する
- **WHEN** ドキュメントディレクトリを確認する
- **THEN** 以下のファイルとディレクトリが存在する：
  - `docs/source/` - ドキュメントソースファイル
  - `docs/source/conf.py` - Sphinx設定ファイル
  - `docs/Makefile` - ビルドコマンド

#### Scenario: コンテンツセクション

- **GIVEN** `docs/source/` ディレクトリが存在する
- **WHEN** ドキュメントソースを確認する
- **THEN** 以下のセクションが存在する：
  - `index.rst` - ランディングページ
  - `installation.rst` - インストールガイド
  - `quickstart.rst` - クイックスタート
  - `user_guide/` - ユーザーガイドセクション
  - `examples/` - サンプル集
  - `api/` - APIリファレンス
  - `contributing.rst` - コントリビューションガイド
  - `changelog.rst` - 変更履歴

### Requirement: HTML出力生成

システムは、Sphinxを使用してHTML形式のドキュメントを生成しなければならない (SHALL)。

#### Scenario: HTML ビルド成功

- **GIVEN** ドキュメントソースが `docs/source/` に存在する
- **AND** Sphinx設定が適切に設定されている
- **WHEN** `make html` コマンドを実行する
- **THEN** HTML ファイルが `docs/_build/html/` に生成される
- **AND** すべての内部リンクが正しく機能する

#### Scenario: Sphinxテーマ適用

- **GIVEN** `docs/source/conf.py` にテーマ設定が存在する
- **WHEN** HTML ドキュメントをビルドする
- **THEN** 指定されたSphinxテーマ（furo、sphinx-rtd-theme等）が適用される
- **AND** ナビゲーション、検索、目次が正しく表示される

### Requirement: PDF出力生成

システムは、typsphinx拡張を使用してPDF形式のドキュメントを生成しなければならない (SHALL)。

#### Scenario: PDF ビルド成功

- **GIVEN** ドキュメントソースが `docs/source/` に存在する
- **AND** `conf.py` に `typstpdf` ビルダー設定が存在する
- **WHEN** `make typstpdf` コマンドを実行する
- **THEN** PDF ファイルが `docs/_build/typstpdf/` に生成される
- **AND** PDF の品質が高く、読みやすい

#### Scenario: typsphinxドッグフーディング

- **GIVEN** プロジェクトが typsphinx 拡張機能を提供している
- **WHEN** ドキュメントのPDFをビルドする
- **THEN** typsphinx拡張が使用される
- **AND** 生成されたPDFがtypsphinxの能力を実証する

### Requirement: GitHub Pages デプロイ

システムは、GitHub Actionsを使用してドキュメントを自動的にGitHub Pagesにデプロイしなければならない (SHALL)。

#### Scenario: 自動デプロイワークフロー

- **GIVEN** `.github/workflows/docs.yml` ワークフローが存在する
- **WHEN** `main` ブランチにプッシュする
- **THEN** GitHub Actions がドキュメントをビルドする
- **AND** ビルドされたHTMLが GitHub Pages にデプロイされる
- **AND** ドキュメントが `https://yusabo90002.github.io/typsphinx/` でアクセス可能になる

#### Scenario: プルリクエストでのビルド検証

- **GIVEN** プルリクエストが作成される
- **WHEN** GitHub Actions ワークフローが実行される
- **THEN** ドキュメントのビルドが成功する
- **AND** ビルドエラーがあればプルリクエストで報告される
- **BUT** GitHub Pages へのデプロイは実行されない（mainブランチのみ）

### Requirement: PDF配布

システムは、GitHub Releasesを通じてPDF版ドキュメントを配布しなければならない (SHALL)。

#### Scenario: リリースタグでのPDFアップロード

- **GIVEN** バージョンタグ（例: `v0.3.0`）がプッシュされる
- **WHEN** GitHub Actions ワークフローが実行される
- **THEN** PDF ドキュメントがビルドされる
- **AND** PDF が GitHub Release にアップロードされる
- **AND** リリースページからPDFをダウンロードできる

#### Scenario: ドキュメントサイトからのPDFダウンロード

- **GIVEN** ドキュメントサイトが公開されている
- **AND** 最新リリースにPDFが存在する
- **WHEN** ドキュメントサイトを訪問する
- **THEN** PDF版ドキュメントへのダウンロードリンクが表示される
- **AND** リンクをクリックするとPDFがダウンロードされる

### Requirement: ドキュメント依存関係

システムは、ドキュメント生成に必要な依存関係を適切に管理しなければならない (SHALL)。

#### Scenario: 依存関係定義

- **GIVEN** `pyproject.toml` が存在する
- **WHEN** ファイルを確認する
- **THEN** ドキュメント関連の依存関係が定義されている：
  - Sphinx テーマ（furo、sphinx-rtd-theme等）
  - sphinx-autodoc-typehints（型ヒントサポート）
  - その他必要なSphinx拡張

#### Scenario: ドキュメントビルド環境

- **GIVEN** ドキュメント依存関係が定義されている
- **WHEN** `uv sync --extra docs` を実行する
- **THEN** すべてのドキュメント依存関係がインストールされる
- **AND** ドキュメントのビルドが成功する

