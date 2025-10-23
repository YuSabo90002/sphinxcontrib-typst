# template-system Specification Delta

## ADDED Requirements

### Requirement: テンプレート設定名の明確化

テンプレート専用の設定は、その用途が明確にわかる名称を使用しなければならない（MUST）。

#### Scenario: typst_template_package 設定の使用

- **GIVEN** ユーザーが charged-ieee などの外部テンプレートを使用したい
- **WHEN** `conf.py` でテンプレート設定を行う
- **THEN** `typst_template_package` 設定を使用する
- **AND** 設定名から「テンプレート用」であることが明確にわかる

#### Scenario: 旧設定名 typst_package の非サポート

- **GIVEN** `conf.py` に `typst_package` 設定が存在する
- **WHEN** Sphinx ビルドを実行する
- **THEN** エラーメッセージが表示される
- **AND** エラーメッセージに「`typst_package` は `typst_template_package` に名称変更されました」と記載される
- **AND** 移行方法が明示される

#### Scenario: typst_package_imports は変更なし

- **GIVEN** `conf.py` に `typst_package_imports` 設定が存在する
- **WHEN** Sphinx ビルドを実行する
- **THEN** `typst_package_imports` は引き続き正常に動作する
- **AND** 複数の汎用パッケージが正しくインポートされる

### Requirement: 外部パッケージ使用時のテンプレートファイルインポートスキップ

外部 Typst パッケージ（`typst_template_package` 設定）を使用する場合、ローカルテンプレートファイル（`_template.typ`）からのインポートをスキップしなければならない（MUST）。

#### Scenario: 外部パッケージのみを使用する場合

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_package = "@preview/charged-ieee:0.1.4"
  typst_template_function = "ieee"
  ```
- **AND** ローカルテンプレートファイル `_template.typ` が存在しない
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルは `#import "@preview/charged-ieee:0.1.4": ieee` を含む
- **AND** `#import "_template.typ": ieee` は含まれない
- **AND** ビルドエラーが発生しない

#### Scenario: ローカルテンプレートのみを使用する場合

- **GIVEN** `conf.py` に `typst_template_package` 設定が存在しない
- **AND** `typst_template_function = "project"` が設定されている
- **AND** ローカルテンプレートファイル `_template.typ` が存在する
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルは `#import "_template.typ": project` を含む
- **AND** 外部パッケージのインポートは含まれない

#### Scenario: 外部パッケージとローカルテンプレートの併用

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_package = "@preview/gentle-clues:1.0.0"
  ```
- **AND** ローカルテンプレートファイル `_template.typ` が存在する
- **AND** `typst_template_function` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルは外部パッケージのインポートのみを含む
- **AND** `_template.typ` からのインポートは含まれない

### Requirement: 著者情報の辞書形式フォーマット

charged-ieee などのテンプレートが要求する辞書配列形式で著者情報をフォーマットできなければならない（MUST）。

#### Scenario: 文字列形式の著者情報（デフォルト）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe, Jane Smith"
  ```
- **AND** `typst_authors_format` が設定されていない（デフォルト: "string"）
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは `("John Doe", "Jane Smith")` となる

#### Scenario: 辞書形式の著者情報

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe"
  typst_authors_format = "dictionary"
  typst_author_fields = ["name", "department", "organization", "email"]
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは以下の形式となる
  ```typst
  authors: (
    (name: "John Doe"),
  )
  ```

#### Scenario: 辞書形式の複数著者情報

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe, Jane Smith"
  typst_authors_format = "dictionary"
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは以下の形式となる
  ```typst
  authors: (
    (name: "John Doe"),
    (name: "Jane Smith"),
  )
  ```

#### Scenario: charged-ieee 向けの完全な著者情報

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe"
  typst_authors_format = "dictionary"
  typst_author_params = {
      "John Doe": {
          "department": "Computer Science",
          "organization": "University of Example",
          "email": "john@example.com"
      }
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは以下の形式となる
  ```typst
  authors: (
    (
      name: "John Doe",
      department: "Computer Science",
      organization: "University of Example",
      email: "john@example.com"
    ),
  )
  ```

### Requirement: テンプレート固有パラメータの設定

charged-ieee などのテンプレートが要求する固有のパラメータ（abstract, index-terms, paper-size など）を設定できなければならない（MUST）。

#### Scenario: charged-ieee の abstract パラメータ

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_package = "@preview/charged-ieee:0.1.4"
  typst_template_function = "ieee"
  typst_template_params = {
      "abstract": "This paper presents novel approaches to neural network architectures."
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `#show: ieee.with()` 呼び出しに `abstract: [This paper presents...]` が含まれる

#### Scenario: charged-ieee の index-terms パラメータ

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_params = {
      "index-terms": ["Machine Learning", "Neural Networks", "Deep Learning"]
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `#show: ieee.with()` 呼び出しに以下が含まれる
  ```typst
  index-terms: ("Machine Learning", "Neural Networks", "Deep Learning")
  ```

#### Scenario: 複数のテンプレート固有パラメータ

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_params = {
      "abstract": "Research on AI systems.",
      "index-terms": ["AI", "Machine Learning"],
      "paper-size": "a4"
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `#show: ieee.with()` 呼び出しにすべてのパラメータが含まれる

#### Scenario: テンプレート固有パラメータが未設定の場合

- **GIVEN** `conf.py` に `typst_template_params` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** テンプレート固有パラメータは生成されない
- **AND** 基本パラメータ（title, authors など）のみが生成される

### Requirement: charged-ieee テンプレートの動作例

charged-ieee テンプレートを使用した完全な動作例を提供しなければならない（MUST）。

#### Scenario: charged-ieee の基本設定

- **GIVEN** `examples/charged-ieee/` ディレクトリが存在する
- **AND** `examples/charged-ieee/conf.py` に charged-ieee の完全な設定が含まれる
- **AND** `examples/charged-ieee/source/index.rst` にサンプルドキュメントが存在する
- **WHEN** `examples/charged-ieee/` で Typst ビルドを実行する
- **THEN** PDF が正常に生成される
- **AND** IEEE フォーマットが適用されている

#### Scenario: charged-ieee の example がドキュメント化されている

- **GIVEN** charged-ieee example が存在する
- **WHEN** プロジェクトドキュメントを確認する
- **THEN** Typst Universe テンプレートの使用方法が説明されている
- **AND** charged-ieee の設定例が記載されている
- **AND** 必要な設定オプションが明記されている

### Requirement: Typst Universe テンプレート使用ガイド

Typst Universe テンプレートの使用方法をドキュメントに記載しなければならない（MUST）。

#### Scenario: 外部テンプレートの基本的な使用方法

- **GIVEN** プロジェクトドキュメントが存在する
- **WHEN** Typst Universe テンプレートのセクションを確認する
- **THEN** 基本的な設定手順が説明されている
  - `typst_template_package` の指定方法
  - `typst_template_function` の指定方法
  - パッケージバージョンの指定方法

#### Scenario: charged-ieee テンプレートの使用ガイド

- **GIVEN** Typst Universe テンプレートのドキュメントが存在する
- **WHEN** charged-ieee の使用例を確認する
- **THEN** 完全な `conf.py` 設定例が記載されている
- **AND** 著者情報の辞書形式フォーマット設定が説明されている
- **AND** テンプレート固有パラメータの設定方法が説明されている

#### Scenario: modern-cv テンプレートの言及

- **GIVEN** Typst Universe テンプレートのドキュメントが存在する
- **WHEN** サポートされているテンプレートのリストを確認する
- **THEN** charged-ieee, modern-cv などの主要テンプレートが言及されている
- **AND** 各テンプレートの Typst Universe ページへのリンクが記載されている
