# Spec Delta: Document Conversion - codly Import

## NEW Requirements

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
