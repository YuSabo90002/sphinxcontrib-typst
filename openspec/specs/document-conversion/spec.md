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

