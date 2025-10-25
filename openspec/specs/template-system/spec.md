# template-system Specification

## Purpose
TBD - created by archiving change add-typst-universe-template-support. Update Purpose after archive.
## Requirements
### Requirement: テンプレート関数とパラメータの統合設定

`typst_template_function`を拡張し、関数名とテンプレート固有パラメータを一体的に設定できなければならない（MUST）。

#### Scenario: 文字列形式（後方互換性・シンプル）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_function = "project"
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルは `#show: project.with(...)` を含む
- **AND** 既存の動作と完全に互換性がある

#### Scenario: 辞書形式でテンプレート固有パラメータを設定

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_function = {
      "name": "ieee",
      "params": {
          "abstract": "This paper presents novel approaches.",
          "index-terms": ["AI", "Machine Learning"],
          "paper-size": "a4"
      }
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `#show: ieee.with()` に以下が含まれる
  ```typst
  abstract: [This paper presents novel approaches.],
  index-terms: ("AI", "Machine Learning"),
  paper-size: "a4",
  ```

#### Scenario: 辞書形式でパラメータなし

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_function = {
      "name": "project"
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルは `#show: project.with(...)` を含む
- **AND** テンプレート固有パラメータは追加されない

#### Scenario: パラメータのみ辞書に含める

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_template_function = {
      "name": "ieee",
      "params": {"abstract": "..."}
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** `abstract` パラメータのみが追加される
- **AND** 基本パラメータ（title, authors等）は通常通り生成される

#### Scenario: 他の設定値を参照（Python変数参照）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  project = "My Project"
  copyright = "2025, Author"

  # IEEE専用の設定
  ieee_abstract = "This paper presents novel approaches."
  ieee_keywords = ["AI", "Machine Learning"]

  # 通常のPython変数参照を使用
  typst_template_function = {
      "name": "ieee",
      "params": {
          "abstract": ieee_abstract,
          "index-terms": ieee_keywords,
          "copyright": copyright,  # 標準設定を再利用
      }
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 各パラメータに参照先の値が正しく展開される
- **AND** `conf.py`はPythonコードなので、特別な参照構文は不要

### Requirement: 著者の詳細情報設定

charged-ieeeなどのテンプレートが要求する著者の詳細情報（department, organization, emailなど）を`conf.py`から設定できなければならない（MUST）。

#### Scenario: 基本的な著者情報（デフォルト動作・後方互換性）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe, Jane Smith"
  ```
- **AND** `typst_author_params` が設定されていない
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは `("John Doe", "Jane Smith")` となる
- **AND** 既存の動作と完全に互換性がある

#### Scenario: typst_authors による著者詳細情報設定（推奨）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_authors = {
      "John Doe": {
          "department": "Computer Science",
          "organization": "MIT",
          "email": "john@mit.edu"
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
      organization: "MIT",
      email: "john@mit.edu"
    ),
  )
  ```
- **AND** `author`設定が不要（`typst_authors`のキーから自動生成）

#### Scenario: typst_author_params による著者詳細情報設定（後方互換性）

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe"
  typst_author_params = {
      "John Doe": {
          "department": "Computer Science",
          "organization": "MIT",
          "email": "john@mit.edu"
      }
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは `typst_authors` と同じ形式となる
- **AND** `author` 設定との組み合わせで動作する

#### Scenario: typst_authors で複数著者の詳細情報

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  typst_authors = {
      "John Doe": {
          "department": "Computer Science",
          "organization": "MIT",
          "email": "john@mit.edu"
      },
      "Jane Smith": {
          "department": "Electrical Engineering",
          "organization": "Stanford",
          "email": "jane@stanford.edu"
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
      organization: "MIT",
      email: "john@mit.edu"
    ),
    (
      name: "Jane Smith",
      department: "Electrical Engineering",
      organization: "Stanford",
      email: "jane@stanford.edu"
    ),
  )
  ```
- **AND** 著者の順序は`typst_authors`辞書のキー順序に従う

#### Scenario: 一部の著者のみ詳細情報を設定

- **GIVEN** `conf.py` に以下の設定が存在する
  ```python
  author = "John Doe, Jane Smith, Bob Wilson"
  typst_author_params = {
      "John Doe": {
          "department": "CS",
          "email": "john@mit.edu"
      }
  }
  ```
- **WHEN** Typst ビルドを実行する
- **THEN** 生成される `.typ` ファイルの `authors` パラメータは以下の形式となる
  ```typst
  authors: (
    (name: "John Doe", department: "CS", email: "john@mit.edu"),
    (name: "Jane Smith"),
    (name: "Bob Wilson"),
  )
  ```
- **AND** 詳細情報がない著者は名前のみの辞書となる

### Requirement: charged-ieee テンプレートの動作例

charged-ieeeテンプレートを使用した完全な動作例を2つのアプローチで提供しなければならない（MUST）。

#### Scenario: アプローチ1 - conf.pyでの統合設定（推奨）

- **GIVEN** `examples/charged-ieee/approach1/` ディレクトリが存在する
- **AND** `conf.py` に以下の設定が含まれる
  ```python
  typst_authors = {
      "John Doe": {"department": "CS", "organization": "MIT", "email": "john@mit.edu"}
  }
  typst_template_function = {
      "name": "ieee",
      "params": {
          "abstract": "...",
          "index-terms": ["AI", "ML"]
      }
  }
  ```
- **WHEN** `examples/charged-ieee/approach1/` で Typst ビルドを実行する
- **THEN** charged-ieee形式のPDFが正常に生成される
- **AND** 著者の詳細情報が正しく表示される
- **AND** abstract, index-termsが正しく表示される

#### Scenario: アプローチ2 - カスタムテンプレートでの変換

- **GIVEN** `examples/charged-ieee/approach2/` ディレクトリが存在する
- **AND** `_template.typ` 内でTypstコードによる著者情報変換関数が実装されている
- **WHEN** `examples/charged-ieee/approach2/` で Typst ビルドを実行する
- **THEN** charged-ieee形式のPDFが正常に生成される
- **AND** アプローチ1と同じ出力が得られる
- **AND** より柔軟なカスタマイズが可能であることが示される

#### Scenario: 2つのアプローチの比較ドキュメント

- **GIVEN** charged-ieee exampleが存在する
- **WHEN** `examples/charged-ieee/README.md` を確認する
- **THEN** 2つのアプローチの違いが説明されている
- **AND** それぞれの利点・欠点が記載されている
- **AND** ユーザーがどちらを選ぶべきかのガイドラインが示されている

### Requirement: Typst Universe テンプレート使用ガイド

Typst Universeテンプレートの使用方法と、`typst_package`/`typst_template`の使い分けをドキュメントに記載しなければならない（MUST）。

#### Scenario: 外部パッケージテンプレートの基本的な使用方法

- **GIVEN** プロジェクトドキュメントが存在する
- **WHEN** Typst Universeテンプレートのセクションを確認する
- **THEN** `typst_package`と`typst_template`の違いが説明されている
- **AND** charged-ieeeを使う場合の設定例が記載されている
- **AND** `typst_authors`の使用方法が説明されている
- **AND** `typst_template_function`の辞書形式の使用方法が説明されている
- **AND** 後方互換性のための`typst_author_params`についても言及されている

#### Scenario: テンプレート内変換アプローチの説明

- **GIVEN** Typst Universeテンプレートのドキュメントが存在する
- **WHEN** カスタムテンプレートによる変換方法のセクションを確認する
- **THEN** `_template.typ`内でTypstコードを書く方法が説明されている
- **AND** 著者情報変換関数の実装例が記載されている
- **AND** いつこのアプローチを使うべきかが説明されている

#### Scenario: サポートされているテンプレートのリスト

- **GIVEN** Typst Universeテンプレートのドキュメントが存在する
- **WHEN** サポートされているテンプレートのリストを確認する
- **THEN** charged-ieee, modern-cvなどの主要テンプレートが言及されている
- **AND** 各テンプレートのTypst UniverseページへのリンクがE載されている
- **AND** 各テンプレートで必要な設定の概要が説明されている

