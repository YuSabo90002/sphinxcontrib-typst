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

