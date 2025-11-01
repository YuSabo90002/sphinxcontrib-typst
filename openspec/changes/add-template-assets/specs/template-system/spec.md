# template-system Spec Delta

## ADDED Requirements

### Requirement: テンプレートアセットの自動コピー

カスタムTypstテンプレート(`typst_template`)使用時に、テンプレートが参照するアセット(フォント、画像、ロゴ等)を出力ディレクトリに自動的にコピーしなければならない（MUST）。

#### Scenario: テンプレートディレクトリの自動コピー（デフォルト動作）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template = "_templates/corporate/template.typ"
  ```
- **AND** `_templates/corporate/` ディレクトリに以下のファイルが存在する
  ```
  _templates/corporate/
    ├── template.typ
    ├── logo.png
    └── assets/
        └── font.otf
  ```
- **AND** `typst_template_assets` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** `_templates/corporate/` ディレクトリ全体が出力ディレクトリにコピーされる
- **AND** `template.typ` 内の `#image("logo.png")` 参照が正常に動作する
- **AND** `#set text(font: "assets/font.otf")` 参照が正常に動作する

#### Scenario: 明示的なアセット指定

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template = "_templates/template.typ"
  typst_template_assets = [
      "_templates/logo.png",
      "_templates/fonts/"
  ]
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** `logo.png` ファイルがコピーされる
- **AND** `fonts/` ディレクトリ全体がコピーされる
- **AND** リストに含まれないファイルはコピーされない

#### Scenario: Globパターンによるアセット指定

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template = "_templates/template.typ"
  typst_template_assets = [
      "_templates/assets/*.png",
      "_templates/fonts/*.otf"
  ]
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** `_templates/assets/` 内のすべての `.png` ファイルがコピーされる
- **AND** `_templates/fonts/` 内のすべての `.otf` ファイルがコピーされる
- **AND** パターンに一致しないファイルはコピーされない

#### Scenario: 相対パス構造の保持

- **GIVEN** テンプレートが以下のディレクトリ構造を持つ
  ```
  _templates/
    ├── template.typ
    └── assets/
        └── nested/
            └── logo.png
  ```
- **AND** `template.typ` 内で `#image("assets/nested/logo.png")` を参照している
- **WHEN** Typst ビルドを実行する
- **THEN** 出力ディレクトリに以下の構造が作成される
  ```
  output/
    └── _templates/
        ├── template.typ
        └── assets/
            └── nested/
                └── logo.png
  ```
- **AND** テンプレート内の相対パス参照が正常に動作する

#### Scenario: 存在しないアセットの処理

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_assets = [
      "_templates/existing.png",
      "_templates/missing.png"
  ]
  ```
- **AND** `missing.png` が存在しない
- **WHEN** Typst ビルドを実行する
- **THEN** `existing.png` は正常にコピーされる
- **AND** `missing.png` について警告がログに記録される
- **AND** ビルドは失敗しない（警告のみ）

#### Scenario: アセットコピーの無効化

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template = "_templates/template.typ"
  typst_template_assets = []  # 空のリスト
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** テンプレートディレクトリの自動コピーは実行されない
- **AND** `template.typ` のみがコピーされる（既存の動作）

### Requirement: Typst Universeパッケージとの区別

`typst_package`で指定されたTypst Universeパッケージについては、アセットの自動コピーを実行してはならない（MUST NOT）。パッケージのアセットはTypstコンパイラが自動的に処理する。

#### Scenario: Typst Universeパッケージ使用時

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_package = "@preview/charged-ieee:0.1.0"
  ```
- **AND** `typst_template` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** アセットコピー処理は実行されない
- **AND** パッケージのアセット(ロゴ、フォント等)はTypstコンパイラが自動的に処理する

#### Scenario: ローカルテンプレートとパッケージの併用

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_package = "@preview/codly:1.3.0"  # パッケージ（アセット自動）
  typst_template = "_templates/custom.typ"  # ローカルテンプレート（アセット要コピー）
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** `_templates/` ディレクトリのアセットのみがコピーされる
- **AND** `codly` パッケージのアセットは Typst コンパイラが処理する

### Requirement: 後方互換性の保証

アセット自動コピー機能は、既存プロジェクト（`typst_template` を使用していないプロジェクト）に影響を与えてはならない（MUST NOT）。

#### Scenario: typst_template 未設定のプロジェクト

- **GIVEN** `conf.py` に `typst_template` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** アセットコピー処理は実行されない
- **AND** 既存の動作と完全に互換性がある

#### Scenario: テンプレートのみでアセットなしのプロジェクト

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template = "_templates/simple.typ"
  ```
- **AND** `_templates/` ディレクトリに `simple.typ` のみが存在する（アセットなし）
- **WHEN** Typst ビルドを実行する
- **THEN** `simple.typ` が正常にコピーされる（既存の動作）
- **AND** 追加のアセットコピーは発生しない（アセットがないため）
- **AND** ビルドは成功する

### Requirement: 設定値の定義

テンプレートアセット指定用の新しい設定値 `typst_template_assets` を提供しなければならない（MUST）。

#### Scenario: 設定値の型と デフォルト値

- **GIVEN** Sphinx 拡張が初期化される
- **WHEN** `typst_template_assets` 設定値を確認する
- **THEN** 以下の仕様を満たす
  - 型: `list` または `None`
  - デフォルト値: `None`
  - rebuild タイプ: `html`（テンプレート変更時に再ビルドが必要）

#### Scenario: 設定値のドキュメント

- **GIVEN** ユーザーガイドが存在する
- **WHEN** `typst_template_assets` の説明を確認する
- **THEN** 以下の情報が含まれる
  - 設定の目的（テンプレートアセットの明示的指定）
  - デフォルト動作（`None` の場合はテンプレートディレクトリ全体をコピー）
  - 例（ファイル指定、ディレクトリ指定、Globパターン）
  - 空リストでの無効化方法

### Requirement: コピー処理の実装

`TypstBuilder` クラスに `copy_template_assets()` メソッドを実装し、`finish()` メソッドから呼び出さなければならない（MUST）。

#### Scenario: ビルドプロセスへの統合

- **GIVEN** Typst ビルダーが実行される
- **WHEN** `finish()` メソッドが呼び出される
- **THEN** `copy_image_files()` の後に `copy_template_assets()` が呼び出される
- **AND** 両方のメソッドが正常に実行される

#### Scenario: copy_template_assets() の動作

- **GIVEN** `copy_template_assets()` メソッドが実装されている
- **WHEN** メソッドが呼び出される
- **THEN** 以下の処理が実行される
  1. `typst_template` 設定を確認
  2. テンプレートが設定されていない場合は早期リターン
  3. `typst_template_assets` 設定を確認
  4. アセットが明示的に指定されている場合は、それらのみをコピー
  5. アセットが指定されていない場合は、テンプレートディレクトリ全体をコピー
  6. コピー処理中のエラーは警告としてログ記録し、ビルドは継続

#### Scenario: ログ出力

- **GIVEN** テンプレートアセットが存在する
- **WHEN** `copy_template_assets()` が実行される
- **THEN** 以下のログが出力される
  - `INFO: Copying template assets...`（コピー開始時）
  - `DEBUG: Copied template asset: {path}`（各ファイルごと）
  - `WARNING: Template asset not found: {path}`（存在しないアセット）
