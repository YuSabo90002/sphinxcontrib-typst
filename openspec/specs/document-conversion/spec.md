# Spec: ドキュメント変換

## Purpose

reStructuredTextドキュメントをTypstマークアップ形式に変換する機能を定義します。docutilsノードツリーをTraverseし、各ノードタイプに対応するTypst構文を生成します。

## Requirements

### Requirement: RSTコメントノードの処理

reStructuredTextコメント（`.. comment`）は現在未処理の状態である (SHALL)。

#### Scenario: コメントノードの未処理

- **GIVEN** RSTファイルにコメントノード（`.. This is a comment`）が含まれる
- **WHEN** Typst形式に変換される
- **THEN** 警告メッセージ `WARNING: unknown node type: <comment>` が表示される
- **AND** コメントテキストがプレーンテキストとして出力される
