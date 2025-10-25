# Proposal: Migrate CI to Tox

## Why

現在、GitHub Actionsワークフローは各ジョブで個別にコマンドを実行しており、以下の課題があります：

1. **重複したコマンド定義**: テスト、lint、type checkなどのコマンドがGitHub ActionsとローカルTODOで重複
2. **ローカル再現性の問題**: CI失敗時にローカルで同じ環境を再現しにくい
3. **メンテナンスコスト**: 変更時に複数のワークフローファイルを更新する必要がある
4. **ドキュメントビルドの未検証**: 現在、ドキュメントビルド（HTML/PDF）がtoxで実行できない

toxを活用することで：

- **単一の真実の源**: tox.iniでコマンドを一元管理
- **ローカル/CI一貫性**: 同じtoxコマンドをローカルとCIで実行
- **簡潔なワークフロー**: GitHub Actionsは`tox`コマンドを呼ぶだけ
- **検証容易性**: ローカルで`tox`を実行すればCI環境を再現

## What Changes

### 1. tox.iniの拡張

新しいtox環境を追加：

- `docs-html`: HTMLドキュメントビルド
- `docs-pdf`: PDFドキュメントビルド（typstpdf）
- `docs`: 両方のドキュメントビルド

### 2. GitHub Actionsワークフローの簡素化

**ci.yml**: 既存のtest/lint/type-checkジョブをtox経由に変更

**docs.yml**: ドキュメントビルドをtox経由に変更

### 3. conf.pyの修正

`docs/source/conf.py`の`extensions`に`typsphinx`を追加（PDFビルドに必要）

## Impact

### Affected specs

既存specの修正：
- `package-structure`: CI/CD設定の変更

新規specの追加：
- なし（既存の範囲内）

### Affected code

変更ファイル：
- `tox.ini` - 新しいdocs環境追加
- `.github/workflows/ci.yml` - toxコマンド経由に変更
- `.github/workflows/docs.yml` - toxコマンド経由に変更
- `docs/source/conf.py` - typsphinx extension追加

### Breaking changes

なし - 外部APIや動作に変更なし

## Alternatives Considered

1. **現状維持**: GitHub Actionsで直接コマンド実行
   - 問題: ローカル再現性が低く、メンテナンスコストが高い

2. **Makefileの使用**: makeコマンドでタスク管理
   - 問題: Python環境管理がtoxより弱い

3. **カスタムスクリプト**: scripts/ディレクトリにシェルスクリプト
   - 問題: 標準化されていない、toxのような環境分離がない

toxを選択した理由：
- Pythonプロジェクトの標準的なツール
- 環境分離が優れている
- 既存のtox設定を活用できる
- ローカル/CI両方で同じコマンド
