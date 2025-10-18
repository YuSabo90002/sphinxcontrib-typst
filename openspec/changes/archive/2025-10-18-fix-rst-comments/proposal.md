# 提案: RSTコメントの処理を追加

**Change ID:** `fix-rst-comments`
**ステータス:** 提案中
**作成日:** 2025-10-18
**関連Issue:** [#21](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/21)

## Why

reStructuredTextのコメント（`..` で始まる行）がTypst出力にプレーンテキストとして表示されてしまう問題が発生しています。この問題により：

- コメントとして記述した内容が最終ドキュメントに表示される
- コメントテキストが後続の段落と結合され、読みにくい出力になる
- Sphinx警告が発生する：`WARNING: unknown node type: <comment xml:space="preserve">...`

根本原因は`sphinxcontrib/typst/translator.py`に`comment`ノードタイプの処理メソッド（`visit_comment()`と`depart_comment()`）が存在しないためです。

## What Changes

`TypstTranslator`クラスに`visit_comment()`および`depart_comment()`メソッドを追加し、RSTコメントを完全にスキップします。

**変更内容:**
- `visit_comment()`: `raise nodes.SkipNode`でコメントノードをスキップ
- `depart_comment()`: パススルー実装

**影響するspec:**
- `specs/document-conversion/spec.md`: RSTコメントノード処理の要件を追加（新規ベースspec作成）

## 概要

RSTコメント（`.. comment text`）がTypst出力に表示されないよう、translatorにコメントノードのスキップ処理を追加します。

## 問題の詳細

### 現在の挙動

**RSTファイル:**
```rst
Test Comments
=============

Before comment paragraph.

.. This is a comment
   It spans multiple lines
   And should not appear in output

After comment paragraph.
```

**現在のTypst出力（誤り）:**
```typst
= Test Comments

Before comment paragraph.

This is a comment
It spans multiple lines
And should not appear in outputAfter comment paragraph.
```

**警告メッセージ:**
```
WARNING: unknown node type: <comment xml:space="preserve">This is a comment...
```

### 期待される挙動

**Typst出力（正しい）:**
```typst
= Test Comments

Before comment paragraph.

After comment paragraph.
```

**警告なし**

## 根本原因

`sphinxcontrib/typst/translator.py`の`TypstTranslator`クラスに以下のメソッドが存在しません：

- `visit_comment(self, node: nodes.comment)`
- `depart_comment(self, node: nodes.comment)`

docutilsのVisitorパターンでは、未実装のノードタイプに対して`unknown_visit()`が呼ばれ、デフォルトでノードのテキスト内容が出力されてしまいます。

## 提案する解決策

最小限の実装でコメントをスキップします：

```python
def visit_comment(self, node: nodes.comment) -> None:
    """
    Visit a comment node.

    Comments are skipped entirely in Typst output as they are meant
    for source-level documentation only.

    Args:
        node: The comment node

    Raises:
        nodes.SkipNode: Always raised to skip the comment
    """
    raise nodes.SkipNode

def depart_comment(self, node: nodes.comment) -> None:
    """
    Depart a comment node.

    Args:
        node: The comment node

    Note:
        This method is not called when SkipNode is raised in visit_comment.
    """
    pass
```

### 動作の変更点

- RSTコメントノード → 完全にスキップ（出力に含まれない）
- 警告メッセージが表示されなくなる
- コメント前後のテキストが正しく分離される

## 影響評価

### メリット

- コメントが正しく処理される（出力に含まれない）
- 意図しない内容の漏洩を防ぐ
- クリーンなTypst出力が生成される
- Sphinx警告が解消される

### リスク評価: 極めて低

- 変更箇所が限定的（2つのメソッド追加のみ）
- `SkipNode`は標準的なdocutils Visitorパターン
- 他のノードタイプへの影響なし
- コメントは元々出力されるべきではない内容

### 後方互換性

- ✅ 完全な後方互換性あり
- コメントが表示されていた既存の動作は誤り（バグ）
- 修正により正しい動作になる

## テスト戦略

**TDDアプローチ**でテストを先に書いてから実装します：

1. **基本コメントのテスト**: 単一行コメントがスキップされることを確認
2. **複数行コメントのテスト**: 複数行にわたるコメントがスキップされることを確認
3. **コメント前後のテキスト**: コメント前後のパラグラフが正しく分離されることを確認
4. **空コメント**: `..` のみの行が正しく処理されることを確認
5. **既存テストの実行**: 既存テストが全てパスすることを確認

## 検討した代替案

### 1. Typstコメントに変換

**アプローチ:** RSTコメントをTypstコメント構文（`//`）に変換

```python
def visit_comment(self, node: nodes.comment) -> None:
    comment_text = node.astext()
    for line in comment_text.split('\n'):
        self.add_text(f"// {line}\n")
    raise nodes.SkipNode
```

**却下理由:**
- RSTコメントはソースレベルのドキュメント用
- Typst出力に残す必要性がない
- ファイルサイズが不必要に増加
- パフォーマンスへの影響

### 2. 設定オプションで制御

**アプローチ:** `typst_preserve_comments` 設定でコメントの扱いを制御

**却下理由:**
- 複雑性が増す
- ほとんどのユースケースでコメントは不要
- 最小限の実装を優先（YAGNI原則）

## 参考資料

- **Issue:** [#21 - RST comments rendered as plain text in Typst output](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/21)
- **関連コード:** `sphinxcontrib/typst/translator.py` - TypstTranslatorクラス
- **docutils reference:** [docutils.nodes.comment](https://docutils.sourceforge.io/docs/ref/doctree.html#comment)
