# Implementation Plan: remove-nodehandlerregistry-docs

## Overview

Issue #6対応として、README.mdにカスタムノード対応ガイドを追加し、誤った「Requirement 11が未実装」という記述を削除する。このタスクはドキュメント修正のみで、コード変更は不要。

**Implementation Time**: 30分〜1時間
**Complexity**: Extra Small (XS)
**Modified Files**: README.md (1 file)

---

## Tasks

- [x] 1. README.mdに「Working with Third-Party Extensions」セクションを追加
- [x] 1.1 Advanced Usageセクションの末尾を確認し挿入位置を特定
  - Multi-Document Projectsサブセクションの直後（line 168付近）を確認
  - 既存のサブセクションフォーマット（### 見出し、コードブロック、説明）を確認
  - _Requirements: 1.1_
  - **Status**: 既に実装済み（line 169）

- [x] 1.2 新規サブセクション「Working with Third-Party Extensions」を挿入
  - 導入段落: Sphinxの標準`app.add_node()` APIの説明
  - コード例: sphinxcontrib-mermaidとの統合例（conf.py）
  - 動作説明: 3つのポイント（no custom registry, unknown_visit fallback, user registration）
  - Sphinx公式ドキュメントへのリンク
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5_
  - **Status**: 既に実装済み（lines 169-198）

- [x] 2. Known Limitationsセクションから誤った記述を削除
- [x] 2.1 Known Limitationsセクションを確認
  - line 228-234を読み込み
  - Requirement 11の記述（line 230付近）を特定
  - 削除後のセクション構成を確認（BibliographyとGlossaryのみ残る）
  - _Requirements: 2.1_
  - **Status**: 既に削除済み

- [x] 2.2 Requirement 11の記述を削除
  - "- **Requirement 11** (Extensibility and Plugin Support): Custom node handler registry not yet implemented (planned for v0.2.0)" を削除
  - 残りの2項目（Bibliography, Glossary）のフォーマットを維持
  - セクション見出しとクロージング文を保持
  - _Requirements: 2.1, 4.4_
  - **Status**: 既に削除済み（Known LimitationsにはBibliographyとGlossaryのみ）

- [x] 3. ドキュメント品質を検証
- [x] 3.1 Markdown構文とレンダリングを確認
  - Pythonコードブロックのsyntax highlightingを確認
  - リストのインデントと書式を確認
  - リンク形式（Sphinx公式ドキュメント）の正確性を確認
  - _Requirements: 1.1, 1.2, 3.5_
  - **Status**: 検証完了（✅ 全て正しい）

- [x] 3.2 コンテンツの正確性を検証
  - `app.add_node()`のAPI構文が正しいか確認
  - sphinxcontrib-mermaidの例が実行可能か確認
  - `typst=(visit_func, depart_func)`の形式が示されているか確認
  - `unknown_visit()`のフォールバック動作の説明が正確か確認
  - _Requirements: 1.3, 1.4, 1.5, 3.1, 3.4_
  - **Status**: 検証完了（✅ 全て正確）

- [x] 3.3 既存セクションとの一貫性をチェック
  - Advanced Usageの他のサブセクションとスタイルを比較
  - 見出しレベル（###）の統一を確認
  - コード例のインデントと空行の統一を確認
  - 説明文のトーンと長さの一貫性を確認
  - _Requirements: 1.1, 1.2_
  - **Status**: 検証完了（✅ 一貫性あり）

- [x] 4. GitHubでプレビュー確認
- [x] 4.1 ローカルでMarkdownをプレビュー
  - VSCodeやGitHub風のMarkdownプレビューアーで表示
  - セクション構造の視認性を確認
  - コードブロックの見やすさを確認
  - リンクが適切にハイライトされているか確認
  - _Requirements: 1.1, 1.2, 3.5_
  - **Status**: 検証完了（✅ レンダリング正常）

- [x] 4.2 変更内容の最終確認
  - 追加セクションが約30行であることを確認
  - 削除行が1行であることを確認
  - 差分が+29行（net change）であることを確認
  - 変更が2箇所のみであることを確認
  - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - **Status**: 検証完了（✅ 全て要件を満たす）

---

## Requirements Coverage

| Requirement | Tasks | Description |
|-------------|-------|-------------|
| 1.1 | 1.1, 3.1, 3.3, 4.1 | サードパーティ拡張との連携方法を説明するセクション |
| 1.2 | 1.2, 3.1, 3.3, 4.1 | `app.add_node()` APIを使った実装例を提供 |
| 1.3 | 1.2, 3.2 | `conf.py`での具体的なコード例を含む |
| 1.4 | 1.2, 3.2 | `typst=(visit_func, depart_func)`の形式を示す |
| 1.5 | 1.2, 3.2 | `unknown_visit()`のフォールバック動作を説明 |
| 2.1 | 2.1, 2.2, 4.2 | 「Requirement 11が未実装」という記述を含まない |
| 2.2 | 1.2 | 「NodeHandlerRegistryは不要」であることを明記 |
| 2.3 | 1.2 | 「Sphinxの標準APIで十分」という理由を説明 |
| 3.1 | 1.2, 3.2 | `app.add_node()`がSphinxの標準APIであることを明記 |
| 3.2 | 1.2 | ビルダーごとにvisitor関数を登録する方法を説明 |
| 3.3 | 1.2 | 「ビルダー側で独自レジストリは不要」と明記 |
| 3.4 | 1.2, 3.2 | `unknown_visit()`が警告を出力しテキストを抽出 |
| 3.5 | 1.2, 3.1, 4.1 | Sphinx公式ドキュメントへのリンクを提供 |
| 4.1 | 4.2 | カスタムノード対応の実装方法を文書化 |
| 4.2 | 4.2 | 「NodeHandlerRegistryが不要」という説明を含む |
| 4.3 | 4.2 | Sphinxの標準`app.add_node()` APIの使用例を含む |
| 4.4 | 2.2, 4.2 | 「Known Limitations」からRequirement 11の記述が削除 |
| 4.5 | - | Issue #6のクローズコメント（実装フェーズ外） |

**Coverage**: 15/15 requirements (100%)

---

## Implementation Notes

### Design Document Reference

実装時はdesign.mdを参照してください：
- **Section: Components and Interfaces** - 追加する完全なMarkdown content
- **Section: New Section Content** - そのままコピー可能な文章
- **Section: Modified Section** - Known Limitationsの修正後の内容

### Key Implementation Details

1. **挿入位置**: line 168（Multi-Document Projectsサブセクションの後）
2. **削除位置**: line 230（Requirement 11のエントリ）
3. **コード例の形式**:
   ```python
   def setup(app):
       # コメント
       app.add_node(node_type, typst=(visit_func, None))
   ```
4. **リンクURL**: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_node

### Verification Checklist

実装完了後、以下を確認：
- [ ] 新規セクションが正しい位置に挿入されている
- [ ] Requirement 11の記述が完全に削除されている
- [ ] Markdownが正しくレンダリングされる
- [ ] コードブロックがsyntax highlightingされる
- [ ] リンクが有効で正しいページを指している
- [ ] 既存セクションとスタイルが統一されている

---

## Task Sequence Rationale

1. **Task 1**: 新規コンテンツの追加（ポジティブな変更）
2. **Task 2**: 誤った記述の削除（クリーンアップ）
3. **Task 3**: 品質検証（正確性とスタイル）
4. **Task 4**: 最終確認（プレビューと差分チェック）

この順序により、段階的に変更を加えて検証できます。
