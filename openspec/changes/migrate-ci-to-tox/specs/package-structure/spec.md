# Capability: package-structure

## MODIFIED Requirements

### Requirement: CI/CD設定

プロジェクトは、継続的インテグレーションとデプロイのための設定を提供しなければならない (SHALL)。

**変更内容**: GitHub ActionsワークフローをTox経由で実行するように変更し、ローカル/CI一貫性を向上させる。

#### Scenario: Toxベースのテスト実行

- **GIVEN** tox.iniにテスト環境が定義されている
- **WHEN** GitHub Actionsのtestジョブが実行される
- **THEN** `tox -e py{39,310,311,312}`コマンドが使用される
- **AND** ローカルで同じtoxコマンドを実行すると同じ結果が得られる

#### Scenario: Toxベースのlint実行

- **GIVEN** tox.iniにlint環境が定義されている
- **WHEN** GitHub Actionsのlintジョブが実行される
- **THEN** `tox -e lint`コマンドが使用される
- **AND** black、ruffチェックが実行される

#### Scenario: Toxベースの型チェック

- **GIVEN** tox.iniにtype環境が定義されている
- **WHEN** GitHub Actionsのtype-checkジョブが実行される
- **THEN** `tox -e type`コマンドが使用される
- **AND** mypyによる型チェックが実行される

#### Scenario: Toxベースのドキュメントビルド

- **GIVEN** tox.iniにdocs-html、docs-pdf環境が定義されている
- **WHEN** GitHub Actionsのdocsジョブが実行される
- **THEN** `tox -e docs-html`でHTMLが、`tox -e docs-pdf`でPDFがビルドされる
- **AND** ローカルで同じtoxコマンドを実行すると同じ出力が得られる

## ADDED Requirements

### Requirement: Tox環境定義

プロジェクトは、ドキュメントビルド用のTox環境を提供しなければならない (SHALL)。

#### Scenario: HTMLドキュメントビルド環境

- **GIVEN** tox.iniが存在する
- **WHEN** `tox -e docs-html`を実行する
- **THEN** Sphinxが実行されてHTMLドキュメントがビルドされる
- **AND** 出力は`docs/_build/html/`に生成される
- **AND** 必要な依存関係（furo、sphinx-autodoc-typehints）がインストールされる

#### Scenario: PDFドキュメントビルド環境

- **GIVEN** tox.iniが存在する
- **WHEN** `tox -e docs-pdf`を実行する
- **THEN** Sphinxがtypstpdfビルダーで実行される
- **AND** 出力は`docs/_build/pdf/`に生成される
- **AND** typsphinx拡張が正しくロードされる

#### Scenario: 統合ドキュメントビルド環境

- **GIVEN** tox.iniが存在する
- **WHEN** `tox -e docs`を実行する
- **THEN** HTMLとPDFの両方がビルドされる
- **AND** いずれかのビルドが失敗した場合、toxは非ゼロ終了コードを返す

### Requirement: ローカル/CI一貫性

プロジェクトは、ローカル開発環境とCI環境で同じコマンドが使用できなければならない (SHALL)。

#### Scenario: ローカルでCIと同じテスト実行

- **GIVEN** 開発者がローカル環境にいる
- **WHEN** `tox`を実行する
- **THEN** CI環境と同じテスト、lint、型チェックが実行される
- **AND** 結果はCI環境と一致する

#### Scenario: CI失敗のローカル再現

- **GIVEN** GitHub ActionsのCIジョブが失敗している
- **WHEN** 開発者がローカルで該当するtox環境（例: `tox -e py311`）を実行する
- **THEN** 同じエラーがローカルで再現できる
- **AND** デバッグがローカル環境で可能になる
