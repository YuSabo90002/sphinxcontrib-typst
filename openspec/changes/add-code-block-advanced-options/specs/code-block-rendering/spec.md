# code-block-rendering Specification Delta

## ADDED Requirements

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
