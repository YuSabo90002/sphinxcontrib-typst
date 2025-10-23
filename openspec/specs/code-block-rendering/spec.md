# code-block-rendering Specification

## Purpose
TBD - created by archiving change fix-code-block-options. Update Purpose after archive.
## Requirements
### Requirement: コードブロック行番号の表示

code-blockディレクティブの`:linenos:`オプションが指定された場合、Typst出力でcodlyの行番号機能を使用して行番号を表示しなければならない (MUST)。

#### Scenario: 基本的な行番号の表示

- **GIVEN** code-blockディレクティブに`:linenos:`オプションが指定される
  ```rst
  .. code-block:: python
     :linenos:

     def hello():
         return "world"
  ```
- **WHEN** Typst形式に変換される
- **THEN** codlyの行番号機能が有効化される
- **AND** 生成されるTypstコードにcodlyの行番号設定が含まれる

#### Scenario: 行番号なしのコードブロック

- **GIVEN** code-blockディレクティブに`:linenos:`オプションが指定されない
  ```rst
  .. code-block:: python

     def hello():
         return "world"
  ```
- **WHEN** Typst形式に変換される
- **THEN** codlyの行番号機能は有効化されない
- **AND** 通常のコードブロックとして出力される

#### Scenario: 行番号と強調行の組み合わせ

- **GIVEN** code-blockディレクティブに`:linenos:`と`:emphasize-lines:`が両方指定される
  ```rst
  .. code-block:: python
     :linenos:
     :emphasize-lines: 1

     def hello():
         return "world"
  ```
- **WHEN** Typst形式に変換される
- **THEN** 行番号と強調行の両方が正しく処理される
- **AND** codlyの行番号と強調表示機能が同時に動作する

### Requirement: コードブロックキャプションとラベルの処理

code-blockディレクティブの`:caption:`および`:name:`オプションが指定された場合、コードブロックを`#figure()`でラップし、キャプションとラベルを追加しなければならない (MUST)。

#### Scenario: キャプション付きコードブロック

- **GIVEN** code-blockディレクティブに`:caption:`オプションが指定される
  ```rst
  .. code-block:: python
     :caption: Example function

     def example():
         pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** コードブロックが`#figure()`でラップされる
- **AND** キャプションが`caption:`パラメータとして設定される
- **AND** 生成されるTypstコードは以下の形式になる（trailing content block形式）：
  ```typst
  #figure(caption: [Example function])[
    ```python
    def example():
        pass
    ```
  ]
  ```

#### Scenario: キャプションとラベル付きコードブロック

- **GIVEN** code-blockディレクティブに`:caption:`と`:name:`オプションが両方指定される
  ```rst
  .. code-block:: python
     :caption: Example function
     :name: code-example

     def example():
         pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** コードブロックが`#figure()`でラップされる
- **AND** キャプションとラベルの両方が設定される
- **AND** 生成されるTypstコードは以下の形式になる（trailing content block形式）：
  ```typst
  #figure(caption: [Example function])[
    ```python
    def example():
        pass
    ```
  ] <code-example>
  ```

#### Scenario: ラベルのみのコードブロック

- **GIVEN** code-blockディレクティブに`:name:`オプションのみが指定される（`:caption:`なし）
  ```rst
  .. code-block:: python
     :name: code-example

     def example():
         pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** コードブロックが`#figure()`でラップされない
- **AND** 代わりにラベルのみが追加される
- **AND** 生成されるTypstコードは以下の形式になる：
  ```typst
  ```python
  def example():
      pass
  ``` <code-example>
  ```

#### Scenario: containerノードの処理

- **GIVEN** Sphinxが`:caption:`オプション付きcode-blockを`container`ノードでラップする
- **WHEN** `container`ノードが`literal-block-wrapper`クラスを持つ
- **THEN** `visit_container()`メソッドが呼び出される
- **AND** containerの子ノード（literal_blockとcaption）が適切に処理される
- **AND** 「unknown node type: container」警告が表示されない

#### Scenario: 複数のオプションの組み合わせ

- **GIVEN** code-blockディレクティブに`:linenos:`、`:caption:`、`:name:`、`:emphasize-lines:`が全て指定される
  ```rst
  .. code-block:: python
     :linenos:
     :caption: Example function
     :name: code-example
     :emphasize-lines: 1

     def example():
         pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** すべてのオプションが正しく処理される
- **AND** 行番号、キャプション、ラベル、強調行がすべて出力に含まれる
- **AND** `#figure()`内でcodlyの機能が正しく動作する

#### Scenario: キャプションテキストのエスケープ

- **GIVEN** キャプションに特殊文字（`[`, `]`, `#`など）が含まれる
  ```rst
  .. code-block:: python
     :caption: Example [with #special] characters

     def example():
         pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** キャプションテキストが適切にエスケープされる
- **AND** Typst構文エラーが発生しない

### Requirement: 行番号開始位置のカスタマイズ

code-blockディレクティブの`:lineno-start:`オプションが指定された場合、指定された行番号から行番号を開始しなければならない (MUST)。この機能はcodlyパッケージの`start`パラメータを使用して実装される。

#### Scenario: 行番号の開始位置を指定

- **GIVEN** code-blockディレクティブに`:linenos:`と`:lineno-start: 42`オプションが指定される
  ```rst
  .. code-block:: python
     :linenos:
     :lineno-start: 42

     def my_function():
         return "This is line 42"
  ```
- **WHEN** Typst形式に変換される
- **THEN** codlyの`start`パラメータが42に設定される
- **AND** 生成されるTypstコードに`#codly(start: 42)`が含まれる
- **AND** コードブロックの行番号が42から始まる

#### Scenario: lineno-startが指定されているがlinenosが無い場合

- **GIVEN** code-blockディレクティブに`:lineno-start:`のみが指定され、`:linenos:`が指定されない
  ```rst
  .. code-block:: python
     :lineno-start: 42

     def my_function():
         return "This is line 42"
  ```
- **WHEN** Typst形式に変換される
- **THEN** 行番号は表示されない
- **AND** `:lineno-start:`オプションは無視される
- **AND** 通常のコードブロックとして出力される

#### Scenario: lineno-startと強調行の組み合わせ

- **GIVEN** code-blockディレクティブに`:linenos:`、`:lineno-start: 100`、`:emphasize-lines: 2`が指定される
  ```rst
  .. code-block:: python
     :linenos:
     :lineno-start: 100
     :emphasize-lines: 2

     def process_data(data):
         result = transform(data)  # This is line 101
         return result
  ```
- **WHEN** Typst形式に変換される
- **THEN** 行番号が100から始まる
- **AND** 2行目（実際の行番号101）が強調表示される
- **AND** codlyの`start`パラメータと`highlight`パラメータが両方設定される

### Requirement: コードブロックのインデント削除

code-blockディレクティブの`:dedent:`オプションが指定された場合、コードブロックの内容から先頭の空白を削除しなければならない (MUST)。この機能はPython標準ライブラリの`textwrap.dedent()`を使用して実装される。

#### Scenario: 指定文字数のインデントを削除

- **GIVEN** code-blockディレクティブに`:dedent: 4`オプションが指定される
  ```rst
  .. code-block:: python
     :dedent: 4

         def nested_function():
             print("This was indented 4 spaces")
  ```
- **WHEN** Typst形式に変換される
- **THEN** 各行の先頭から4文字が削除される
- **AND** 相対的なインデントは維持される
- **AND** 生成されるTypstコードのコードブロック内容は以下のようになる：
  ```typst
  ```python
  def nested_function():
      print("This was indented 4 spaces")
  ```
  ```

#### Scenario: 自動インデント削除

- **GIVEN** code-blockディレクティブに`:dedent:`オプションが値なしで指定される
  ```rst
  .. code-block:: python
     :dedent:

         def nested_function():
             print("auto dedent")
  ```
- **WHEN** Typst形式に変換される
- **THEN** `textwrap.dedent()`が使用され、共通の先頭空白が自動的に削除される
- **AND** 相対的なインデントは維持される

#### Scenario: dedentとその他のオプションの組み合わせ

- **GIVEN** code-blockディレクティブに`:dedent: 8`、`:linenos:`、`:emphasize-lines: 1`が指定される
  ```rst
  .. code-block:: python
     :dedent: 8
     :linenos:
     :emphasize-lines: 1

             def inner_function():
                 return "dedented"
  ```
- **WHEN** Typst形式に変換される
- **THEN** まずdedent処理が行われ、その後行番号と強調表示が適用される
- **AND** 処理順序が正しく保たれる
- **AND** すべての機能が正しく動作する

#### Scenario: 短い行に対するdedent処理

- **GIVEN** code-blockディレクティブに`:dedent: 4`が指定され、一部の行が4文字未満である
  ```rst
  .. code-block:: python
     :dedent: 4

         def foo():

             pass
  ```
- **WHEN** Typst形式に変換される
- **THEN** 4文字以上ある行からは4文字削除される
- **AND** 4文字未満の行はそのまま保持される（負のインデックスにならない）
- **AND** 空行は空行のまま維持される

