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

