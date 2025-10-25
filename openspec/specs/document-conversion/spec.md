# Spec: ドキュメント変換

## Purpose

reStructuredTextドキュメントをTypstマークアップ形式に変換する機能を定義します。docutilsノードツリーをTraverseし、各ノードタイプに対応するTypst構文を生成します。
## Requirements
### Requirement: RSTコメントノードの処理

reStructuredTextコメント（`.. comment`）は出力から完全に除外されなければならない (MUST)。

#### Scenario: コメントノードのスキップ

- **GIVEN** RSTファイルにコメントノード（`.. This is a comment`）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** コメントはTypst出力に含まれない
- **AND** 警告メッセージは表示されない

#### Scenario: 複数行コメントのスキップ

- **GIVEN** RSTファイルに複数行にわたるコメントが含まれる
  ```rst
  .. This is a comment
     spanning multiple lines
     and should not appear
  ```
- **WHEN** Typst形式に変換される
- **THEN** すべてのコメント行がTypst出力に含まれない

#### Scenario: コメント前後のテキスト分離

- **GIVEN** コメントの前後にパラグラフが存在する
  ```rst
  Before paragraph.

  .. Comment here

  After paragraph.
  ```
- **WHEN** Typst形式に変換される
- **THEN** 前後のパラグラフが正しく分離される
- **AND** コメントテキストが後続パラグラフに結合されない

#### Scenario: 空コメントの処理

- **GIVEN** 空のコメントマーカー（`..` のみ）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** 空コメントもスキップされる
- **AND** 警告メッセージは表示されない

### Requirement: Rawディレクティブの処理

docutilsの`raw`ノードは、フォーマットに応じて適切に処理されなければならない (MUST)。`format='typst'`の場合はコンテンツをそのまま出力し、他のフォーマットの場合はコンテンツをスキップしなければならない。

#### Scenario: Typstフォーマットのrawコンテンツのパススルー

- **GIVEN** reStructuredTextファイルに`.. raw:: typst`ディレクティブが含まれる
  ```rst
  .. raw:: typst

     #rect(fill: red)[Custom Typst content]
  ```
- **WHEN** Typst形式に変換される
- **THEN** rawコンテンツがそのままTypst出力に含まれる
- **AND** Typstコンテンツの前後に適切な改行が追加される

#### Scenario: 他のフォーマットのrawコンテンツのスキップ

- **GIVEN** reStructuredTextファイルに`.. raw:: html`ディレクティブが含まれる
  ```rst
  .. raw:: html

     <div class="custom">HTML content</div>
  ```
- **WHEN** Typst形式に変換される
- **THEN** HTMLコンテンツはTypst出力に含まれない
- **AND** スキップされたフォーマットについてデバッグログが記録される

#### Scenario: 複数のrawディレクティブの混在

- **GIVEN** reStructuredTextファイルに複数のフォーマットのrawディレクティブが含まれる
  ```rst
  Before paragraph.

  .. raw:: typst

     #rect(fill: blue)[Typst content]

  .. raw:: html

     <div>HTML content</div>

  .. raw:: typst

     #circle(radius: 10pt)

  After paragraph.
  ```
- **WHEN** Typst形式に変換される
- **THEN** `format='typst'`のコンテンツのみがTypst出力に含まれる
- **AND** HTMLコンテンツはスキップされる
- **AND** 前後のパラグラフが正しく保持される

#### Scenario: Typst rawコンテンツの改行処理

- **GIVEN** rawディレクティブに複数行のTypstコードが含まれる
  ```rst
  .. raw:: typst

     #set text(size: 12pt)
     #rect(
       fill: gradient.linear(red, blue),
       [Multi-line Typst code]
     )
  ```
- **WHEN** Typst形式に変換される
- **THEN** すべてのTypstコードがそのまま保持される
- **AND** 元のインデントと改行が維持される
- **AND** コンテンツの後に適切な空行が追加される

#### Scenario: 空のrawディレクティブ

- **GIVEN** 空のrawディレクティブが含まれる
  ```rst
  .. raw:: typst
  ```
- **WHEN** Typst形式に変換される
- **THEN** 空のコンテンツはスキップされる
- **AND** エラーや警告は発生しない

#### Scenario: 大文字小文字の混在フォーマット名

- **GIVEN** フォーマット名が大文字小文字混在で指定される
  ```rst
  .. raw:: TYPST

     #text[Content]
  ```
- **WHEN** Typst形式に変換される
- **THEN** フォーマット名が大文字小文字を区別せずに処理される
- **AND** コンテンツが正しく出力される

### Requirement: ドキュメントレベルでのパッケージインポート

生成されるTypstドキュメントファイル（`.typ`）は、コンテンツで使用されるすべての必須パッケージをインポートしなければならない (MUST)。

#### Scenario: codlyパッケージのインポート

- **GIVEN** テンプレートファイルを使用するドキュメント生成
- **WHEN** `generate_document()` メソッドでドキュメントファイルが生成される
- **THEN** 生成されたドキュメントファイルに以下のインポートが含まれる:
  ```typst
  #import "@preview/codly:1.3.0": *
  #import "@preview/codly-languages:0.1.1": *
  ```
- **AND** これらのインポートは `mitex` と `gentle-clues` のインポートの前に配置される

#### Scenario: コードブロックでのcodly関数の使用

- **GIVEN** ドキュメントにコードブロックが含まれる
- **WHEN** トランスレータが `#codly()` または `#codly-range()` 関数を生成する
- **THEN** ドキュメントファイルがcodlyパッケージをインポートしているため、Typstコンパイルが成功する
- **AND** 「unknown variable: codly」エラーが発生しない

#### Scenario: PDFビルダーでのコード ブロック処理

- **GIVEN** `:linenos:` オプション付きコードブロックを含むRSTファイル
  ```rst
  .. code-block:: python
     :linenos:

     def hello():
         return "world"
  ```
- **WHEN** `typstpdf` ビルダーでPDFを生成する
- **THEN** PDFが正常に生成される
- **AND** コードブロックに行番号が表示される
- **AND** Typstコンパイルエラーが発生しない

#### Scenario: 必須インポートの順序

- **GIVEN** ドキュメントファイルの生成
- **WHEN** 必須パッケージインポートが追加される
- **THEN** インポートの順序は以下の通りである:
  1. `codly:1.3.0` と `codly-languages:0.1.1`
  2. `mitex:0.2.4`
  3. `gentle-clues:1.2.0`
- **AND** すべてのインポートがテンプレートインポートの前に配置される

#### Scenario: 既存ドキュメントとの互換性

- **GIVEN** codlyインポートを追加する前に生成された既存ドキュメント
- **WHEN** 新しいバージョンで再生成される
- **THEN** すべての既存機能が正常に動作する
- **AND** codlyインポートの追加による破壊的変更はない

### Requirement: 画像ファイルの出力ディレクトリへのコピー

ビルダーは、ドキュメント内で参照されている画像ファイルを出力ディレクトリに自動的にコピーしなければならない (MUST)。これにより、Typstコンパイル時に画像ファイルが利用可能になる。

#### Scenario: 単一画像のコピー

- **GIVEN** reStructuredTextドキュメントに`.. image:: sample.png`ディレクティブが含まれる
- **AND** `sample.png`がソースディレクトリに存在する
- **WHEN** `typstpdf`ビルダーでビルドする
- **THEN** `sample.png`が出力ディレクトリにコピーされる
- **AND** PDF生成が成功する

#### Scenario: 複数画像のコピー

- **GIVEN** ドキュメントに複数の画像ディレクティブが含まれる
- **AND** すべての画像ファイルがソースディレクトリに存在する
- **WHEN** ビルドを実行する
- **THEN** すべての画像ファイルが出力ディレクトリにコピーされる

#### Scenario: サブディレクトリ内の画像

- **GIVEN** `.. image:: images/sample.png`のように相対パスで画像が参照される
- **AND** `images/sample.png`がソースディレクトリに存在する
- **WHEN** ビルドを実行する
- **THEN** 出力ディレクトリに`images/`ディレクトリが作成される
- **AND** `images/sample.png`が正しくコピーされる

#### Scenario: 画像なしドキュメント（後方互換性）

- **GIVEN** ドキュメントに画像ディレクティブが含まれない
- **WHEN** ビルドを実行する
- **THEN** ビルドは正常に完了する
- **AND** 既存の動作が維持される

### Requirement: 画像追跡の実装

ビルダーは、ドキュメントツリーから画像参照を収集し、`self.images`辞書に追跡しなければならない (MUST)。

#### Scenario: post_process_images()の実装

- **GIVEN** ドキュメントに画像が含まれる
- **WHEN** `post_process_images()`が呼び出される
- **THEN** `self.images`辞書が初期化される
- **AND** ドキュメント内のすべての画像パスが`self.images`に追加される

#### Scenario: 画像パスの解決

- **GIVEN** 相対パスで画像が参照される
- **WHEN** 画像を追跡する
- **THEN** ソースディレクトリからの相対パスが正しく解決される
- **AND** 出力ディレクトリ内の対応するパスが計算される

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

