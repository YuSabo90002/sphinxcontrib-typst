# Proposal: Convert to Function Syntax

## Why

現在、typsphinxは Typst sugar syntax（`=`, `*`, `_`, `-`, `+`）と関数呼び出し構文（`#heading()`, `#strong()`, `#emph()` など）を混在させて使用しています。

この不統一により以下の問題が発生しています：

1. **保守性の低下**: Sugar syntax と関数呼び出しが混在し、コード構造が不明瞭
2. **構文エラーのリスク**: `*_text_*` のような sugar syntax の組み合わせで Typst コンパイルエラーが発生（Issue #55 で確認済み）
3. **1:1対応の欠如**: `visit_*/depart_*` メソッドと Typst 関数の対応が不明確
4. **一貫性の欠如**: 一部の要素（`#sub[]`, `#super[]`, `#quote[]` など）は既に関数構文を使用

**具体的な問題例**（前回の実装で確認）:
```typst
*_templates/custom_ieee.typ*:
```
このような sugar syntax の組み合わせが "unclosed delimiter" エラーを引き起こします。

## What Changes

### 変換対象要素

以下の6要素を sugar syntax から関数呼び出し構文に変換します：

| Element | Current Syntax | Target Syntax | 影響範囲 |
|---------|---------------|---------------|---------|
| Heading | `= Heading` | `#heading(level: 1)[Heading]` | translator.py:123-142 |
| Emphasis | `_text_` | `#emph[text]` | translator.py:328-345 |
| Strong | `*text*` | `#strong[text]` | translator.py:347-364 |
| Subtitle | `_subtitle_` | `#emph[subtitle]` | translator.py:144-161 |
| Bullet List | `- item` | `#list([item])` | translator.py:423-476 |
| Enum List | `+ item` | `#enum([item])` | translator.py:442-476 |

### 変更しない要素

以下は変更対象外です：

- ✅ **Code blocks / Inline code** (`` `code` ``, ` ```lang `)
  - Typst標準構文であり、sugar syntax ではない
- ✅ **Definition lists** (`/ term: definition`)
  - 既に Typst 標準の term list 構文を使用
- ✅ **既に関数構文を使用している要素**
  - `#sub[]`, `#super[]`, `#quote[]`, `#image()`, `#table()`, `#figure()`, `#link()`, admonitions など

### 実装方針

1. **段階的変換**: 要素ごとに変換し、各ステップでテスト
2. **テスト更新**: すべての期待値を新しい構文に更新
3. **後方互換性**: 生成される PDF 出力は同一（構文のみ変更）

## Impact

### Affected Specs

変更が必要な仕様：
- `document-conversion`: 各要素の出力構文を更新

### Affected Code

**変更ファイル**:
- `typsphinx/translator.py`: 6要素の `visit_*/depart_*` メソッド（約12メソッド）
- `tests/test_translator.py`: すべての期待値更新
- その他のテストファイル: 統合テスト、E2Eテストの期待値更新

**影響を受けるテスト**: 約50-100テストケース（期待値のみ更新）

### Breaking Changes

⚠️ **Breaking Change**: 生成される `.typ` ファイルの構文が変更されます

**影響範囲**:
- 既存ドキュメントを再ビルドすると、`.typ` ファイルの内容が変わる
- ただし、最終的なPDF出力は同一

**バージョニング**:
- Major version bump が必要（v0.2.0 → v0.3.0 または v1.0.0）

### User-Visible Changes

**変更前**:
```typst
= Introduction

This is _emphasized_ and *strong* text.

- First item
- Second item

+ Numbered 1
+ Numbered 2
```

**変更後**:
```typst
#heading(level: 1)[Introduction]

This is #emph[emphasized] and #strong[strong] text.

#list(
  [First item],
  [Second item],
)

#enum(
  [Numbered 1],
  [Numbered 2],
)
```

## Alternatives Considered

### 1. Sugar syntax を維持する（現状維持）

**却下理由**:
- 構文エラーのリスクが残る
- コードの保守性が低いまま
- 不統一が継続

### 2. 部分的に変換（一部の要素のみ）

**却下理由**:
- 問題は解決しない
- さらなる不統一を生む

### 3. すべての要素を関数構文に統一（選択）

**メリット**:
- ✅ 構文エラーのリスク解消
- ✅ コード構造の明確化
- ✅ 一貫性の確保
- ✅ 保守性の向上

**デメリット**:
- ⚠️ Breaking change
- 🔧 テストの大量更新が必要

## Implementation Notes

### Heading 実装の注意点

```python
# Before
def visit_title(self, node):
    heading_prefix = "=" * self.section_level
    self.add_text(f"{heading_prefix} ")

# After
def visit_title(self, node):
    self.add_text(f"#heading(level: {self.section_level})[")

def depart_title(self, node):
    self.add_text("]\n\n")
```

### List 実装の注意点

リストはネストに対応する必要があります：

```python
# ネストされたリストの例
#list(
  [First item],
  [Second item with nested:
    #list(
      [Nested 1],
      [Nested 2],
    )
  ],
)
```

実装では：
1. リスト項目を収集
2. リスト終了時に `#list()` / `#enum()` として出力
3. ネストレベルを適切に管理

### テスト戦略

1. **単体テスト**: 各要素の変換テスト
2. **統合テスト**: ネストされた構造のテスト
3. **回帰テスト**: 既存ドキュメントのPDF出力が同一であることを確認

### 移行ガイド

ユーザー向けドキュメントに以下を追加：
- Breaking change の説明
- 生成される `.typ` ファイルの変更内容
- PDF出力は同一であることの保証
