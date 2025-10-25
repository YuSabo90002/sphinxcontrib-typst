# convert-to-function-syntax

Document MODIFIED and ADDED requirements only. Structure follows the same organization as `openspec/specs/document-conversion/spec.md`. Explain the requirement's intent and reason in "Why", then present the changed spec in "What".

## MODIFIED Requirements

### Requirement: 見出しの変換

見出しノードは Typst の `#heading()` 関数として出力されなければならない (MUST)。Sugar syntax (`=`, `==`, `===`) による出力は使用してはならない (MUST NOT)。

#### Scenario: 第1レベル見出しの変換

- **GIVEN** reStructuredTextファイルに第1レベル見出しが含まれる
  ```rst
  Title
  =====
  ```
- **WHEN** Typst形式に変換される
- **THEN** 見出しが `#heading(level: 1)[Title]` 形式で出力される
- **AND** sugar syntax (`= Title`) は使用されない

#### Scenario: ネストされた見出し

- **GIVEN** 複数レベルの見出しが含まれる
  ```rst
  Main Title
  ==========

  Subtitle
  --------

  Subsubtitle
  ^^^^^^^^^^^
  ```
- **WHEN** Typst形式に変換される
- **THEN** すべての見出しが関数形式で出力される
  ```typst
  #heading(level: 1)[Main Title]

  #heading(level: 2)[Subtitle]

  #heading(level: 3)[Subsubtitle]
  ```

### Requirement: 強調と太字の変換

強調ノードは `#emph[]` として、太字ノードは `#strong[]` として出力されなければならない (MUST)。Sugar syntax (`_text_`, `*text*`) による出力は使用してはならない (MUST NOT)。

#### Scenario: 強調テキストの変換

- **GIVEN** reStructuredTextファイルに強調テキストが含まれる
  ```rst
  This is *emphasized* text.
  ```
- **WHEN** Typst形式に変換される
- **THEN** 強調が `#emph[emphasized]` 形式で出力される
- **AND** sugar syntax (`_emphasized_`) は使用されない

#### Scenario: 太字テキストの変換

- **GIVEN** reStructuredTextファイルに太字テキストが含まれる
  ```rst
  This is **strong** text.
  ```
- **WHEN** Typst形式に変換される
- **THEN** 太字が `#strong[strong]` 形式で出力される
- **AND** sugar syntax (`*strong*`) は使用されない

#### Scenario: 強調と太字のネスト

- **GIVEN** 強調と太字がネストされている
  ```rst
  This is ***emphasized and strong*** text.
  ```
- **WHEN** Typst形式に変換される
- **THEN** ネストが正しく処理される
  ```typst
  This is #strong[#emph[emphasized and strong]] text.
  ```
- **AND** sugar syntax の組み合わせによる構文エラーが発生しない

#### Scenario: アンダースコアを含む太字テキスト

- **GIVEN** 太字テキスト内にアンダースコアが含まれる
  ```rst
  **_templates/custom.typ**
  ```
- **WHEN** Typst形式に変換される
- **THEN** `#strong[_templates/custom.typ]` として出力される
- **AND** `*_templates/custom.typ*` のような構文エラーを引き起こす出力は生成されない

### Requirement: リストの変換

箇条書きリストは `#list()` 関数として、番号付きリストは `#enum()` 関数として出力されなければならない (MUST)。Sugar syntax (`- item`, `+ item`) による出力は使用してはならない (MUST NOT)。

#### Scenario: 単純な箇条書きリスト

- **GIVEN** reStructuredTextファイルに箇条書きリストが含まれる
  ```rst
  - First item
  - Second item
  - Third item
  ```
- **WHEN** Typst形式に変換される
- **THEN** リストが関数形式で出力される
  ```typst
  #list(
    [First item],
    [Second item],
    [Third item],
  )
  ```
- **AND** sugar syntax (`- item`) は使用されない

#### Scenario: 単純な番号付きリスト

- **GIVEN** reStructuredTextファイルに番号付きリストが含まれる
  ```rst
  1. First item
  2. Second item
  3. Third item
  ```
- **WHEN** Typst形式に変換される
- **THEN** リストが関数形式で出力される
  ```typst
  #enum(
    [First item],
    [Second item],
    [Third item],
  )
  ```
- **AND** sugar syntax (`+ item`) は使用されない

#### Scenario: ネストされたリスト

- **GIVEN** ネストされたリスト構造が含まれる
  ```rst
  - First item
  - Second item with nested:

    - Nested item 1
    - Nested item 2

  - Third item
  ```
- **WHEN** Typst形式に変換される
- **THEN** ネスト構造が正しく出力される
  ```typst
  #list(
    [First item],
    [Second item with nested:

      #list(
        [Nested item 1],
        [Nested item 2],
      )
    ],
    [Third item],
  )
  ```

#### Scenario: リスト項目内の複雑なコンテンツ

- **GIVEN** リスト項目内に段落や強調が含まれる
  ```rst
  - Item with **bold** and *emphasis*
  - Item with multiple paragraphs

    Second paragraph
  ```
- **WHEN** Typst形式に変換される
- **THEN** リスト項目内のコンテンツが正しく処理される
  ```typst
  #list(
    [Item with #strong[bold] and #emph[emphasis]],
    [Item with multiple paragraphs

    Second paragraph],
  )
  ```

## ADDED Requirements

### Requirement: サブタイトルの変換

サブタイトルノードは `#emph[]` 関数として出力されなければならない (MUST)。Sugar syntax (`_subtitle_`) による出力は使用してはならない (MUST NOT)。

#### Scenario: サブタイトルの変換

- **GIVEN** reStructuredTextファイルにサブタイトルが含まれる
  ```rst
  Title
  =====

  :subtitle: Document Subtitle
  ```
- **WHEN** Typst形式に変換される
- **THEN** サブタイトルが `#emph[Document Subtitle]` 形式で出力される
- **AND** sugar syntax (`_Document Subtitle_`) は使用されない

#### Scenario: サブタイトル内の特殊文字

- **GIVEN** サブタイトルにアンダースコアなどの特殊文字が含まれる
  ```rst
  :subtitle: API_Reference_v2.0
  ```
- **WHEN** Typst形式に変換される
- **THEN** `#emph[API_Reference_v2.0]` として正しく出力される
- **AND** sugar syntax による構文エラーが発生しない
