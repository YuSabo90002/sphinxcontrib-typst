## ADDED Requirements

### Requirement: API説明ノードの処理

docutilsの`desc`ノードファミリー（API説明用の汎用ノード）、`field_list`ノード（構造化フィールド）、`index`ノード（索引エントリー）、`rubric`ノード（小見出し）、`title_reference`ノード（タイトル参照）を適切に処理し、Typst形式に変換しなければならない (MUST)。これらのノードはsphinx.ext.autodocなど複数の拡張で使用される汎用ノードである。

#### Scenario: インデックスノードのスキップ

- **GIVEN** `index`ノード（索引エントリー）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** `index`ノードは出力に含まれない（PDFではインデックスを生成しない）
- **AND** "unknown node type: index" 警告が表示されない

#### Scenario: API説明ブロックの変換

- **GIVEN** `desc`ノード（API説明用コンテナ）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** `desc`ノードが適切なTypst構造として出力される
- **AND** ネストされた`desc_signature`と`desc_content`が正しく処理される
- **AND** "unknown node type: desc" 警告が表示されない

#### Scenario: 関数/クラスシグネチャの書式設定

- **GIVEN** `desc_signature`ノード（API要素のシグネチャ）が含まれる
  ```python
  class TypstBuilder(app, env):
      ...
  ```
- **WHEN** Typst形式に変換される
- **THEN** シグネチャが`#strong[class TypstBuilder(app, env)]`形式で出力される
- **AND** `desc_annotation`（"class"キーワード）、`desc_name`（クラス名）、`desc_parameterlist`（パラメータ）がすべて正しく結合される
- **AND** 関連する警告が表示されない

#### Scenario: パラメータリストの処理

- **GIVEN** `desc_parameterlist`と複数の`desc_parameter`ノードが含まれる
  ```python
  def example(arg1, arg2, arg3):
      ...
  ```
- **WHEN** Typst形式に変換される
- **THEN** パラメータが`(arg1, arg2, arg3)`形式で出力される
- **AND** パラメータ間のカンマと括弧が正しく処理される
- **AND** "unknown node type: desc_parameter" 警告が表示されない

#### Scenario: モジュール名プレフィックスの処理

- **GIVEN** `desc_addname`ノード（モジュール名プレフィックス）が含まれる
  ```python
  typsphinx.builder.TypstBuilder
  ```
- **WHEN** Typst形式に変換される
- **THEN** モジュール名プレフィックスが出力に含まれる
- **AND** クラス名との結合が正しく行われる
- **AND** "unknown node type: desc_addname" 警告が表示されない

#### Scenario: フィールドリストの変換

- **GIVEN** `field_list`ノード（構造化フィールド、Parameters・Returnsなど）が含まれる
  ```rst
  :param app: Sphinx application
  :param env: Build environment
  :return: None
  ```
- **WHEN** Typst形式に変換される
- **THEN** フィールドリストが適切な見出しと箇条書きリストとして出力される
  ```typst
  *Parameters:*
  - *app* (Sphinx) – Sphinx application
  - *env* (BuildEnvironment) – Build environment

  *Returns:* None
  ```
- **AND** "unknown node type: field_list" 警告が表示されない

#### Scenario: フィールド名とボディの処理

- **GIVEN** `field_name`と`field_body`ノードが含まれる
- **WHEN** Typst形式に変換される
- **THEN** フィールド名が強調表示される（例: `*Parameters:*`）
- **AND** フィールドボディが適切にフォーマットされる
- **AND** 関連する警告が表示されない

#### Scenario: Rubricノードの処理

- **GIVEN** `rubric`ノード（セクション小見出し）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** rubricが適切な見出しとして出力される
- **AND** "unknown node type: rubric" 警告が表示されない

#### Scenario: タイトル参照の処理

- **GIVEN** `title_reference`ノードが含まれる
- **WHEN** Typst形式に変換される
- **THEN** タイトル参照が適切にフォーマットされる
- **AND** "unknown node type: title_reference" 警告が表示されない

#### Scenario: ネストされたAPI説明ノード構造

- **GIVEN** 複雑にネストされたdescノード構造が含まれる
  ```
  desc
    desc_signature
      desc_annotation: "class"
      desc_addname: "typsphinx.builder."
      desc_name: "TypstBuilder"
      desc_parameterlist
        desc_parameter: "app"
        desc_parameter: "env"
    desc_content
      paragraph: "Builder class for Typst output format."
      field_list
        field
          field_name: "Parameters"
          field_body: ...
  ```
- **WHEN** Typst形式に変換される
- **THEN** すべてのネストレベルが正しく処理される
- **AND** 親子関係が維持される
- **AND** すべてのAPI説明ノードタイプについて警告が表示されない

#### Scenario: 完全なAPIドキュメントのPDFビルド

- **GIVEN** sphinx.ext.autodoc、sphinx.ext.napoleon、sphinx_autodoc_typehintsを使用したAPIドキュメント
- **WHEN** `typstpdf`ビルダーでPDFを生成する
- **THEN** PDFビルドが成功する
- **AND** すべてのAPIドキュメント（クラス、メソッド、関数、属性）がPDFに含まれる
- **AND** API説明ノード関連の "unknown node type" 警告が0件である
- **AND** 生成されたPDFが読みやすい形式でフォーマットされている

#### Scenario: typsphinx自身のドキュメントでのdogfooding

- **GIVEN** typsphinxプロジェクトのAPIドキュメント（`docs/source/api/`）
- **WHEN** `uv run tox -e docs-pdf`でPDFビルドを実行する
- **THEN** ビルドが警告なしで成功する
- **AND** 生成されたPDFにtypsphinxのすべてのモジュール、クラス、関数のドキュメントが含まれる
- **AND** Issue #55で報告された1896件の警告が発生しない
