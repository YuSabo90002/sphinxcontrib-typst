# Requirements Document

## Introduction

Issue #6は、`.kiro/specs/sphinxcontrib-typst/design.md`のSection 6.6で提案されている`NodeHandlerRegistry`コンポーネントが不要であることを指摘しています。Sphinxは既にカスタムノード登録のための標準API (`app.add_node()`) を提供しており、追加の独自レジストリを実装する必要はありません。

**ビジネス価値**:
- ユーザーがサードパーティ拡張（sphinxcontrib-mermaidなど）を使用する際の正しいアプローチを文書化
- 不要な実装を回避し、Sphinxの標準アーキテクチャに準拠
- 保守性とSphinxエコシステムとの互換性を向上

**対応範囲**:
- README.mdへのカスタムノード対応ガイドの追加
- 初期構築用の仕様書(`.kiro/specs/sphinxcontrib-typst/`)は変更しない（歴史的記録として保持）

## Requirements

### Requirement 1: カスタムノード対応ドキュメントの追加

**Objective:** ドキュメント利用者として、サードパーティ拡張のカスタムノードをsphinxcontrib-typstで扱う方法を理解したい。これにより、sphinxcontrib-mermaidなどの拡張と組み合わせて使用できるようにする。

#### Acceptance Criteria

1. WHEN ユーザーがREADME.mdを読む THEN README.md SHALL サードパーティ拡張との連携方法を説明するセクションを含む
2. WHERE カスタムノード対応セクション THE README.md SHALL Sphinxの標準`app.add_node()` APIを使った実装例を提供する
3. WHERE 実装例 THE README.md SHALL `conf.py`での具体的なコード例を含む（sphinxcontrib-mermaidなど）
4. WHERE 実装例 THE README.md SHALL `typst=(visit_func, depart_func)`の形式を示す
5. WHEN ユーザーが未知のノードに遭遇する THEN ドキュメント SHALL `unknown_visit()`のフォールバック動作を説明する

### Requirement 2: 誤解を招く記述の削除

**Objective:** プロジェクトメンテナーとして、README.mdから「Requirement 11が未実装」という誤った記述を削除したい。これにより、ユーザーが現在の実装状況を正しく理解できるようにする。

#### Acceptance Criteria

1. WHEN README.mdの「Known Limitations」セクションを読む THEN README.md SHALL 「Requirement 11 (Extensibility and Plugin Support): Custom node handler registry not yet implemented」という記述を含まない
2. IF README.mdがカスタムノード対応を説明する THEN README.md SHALL 「NodeHandlerRegistryは不要」であることを明記する
3. WHERE カスタムノード対応セクション THE README.md SHALL 「Sphinxの標準APIで十分」という理由を説明する

### Requirement 3: Sphinxアーキテクチャの正しい説明

**Objective:** 技術的な正確性を保つために、SphinxのNode登録メカニズムを正しく文書化したい。これにより、ユーザーがSphinxの標準パターンに従った実装ができるようにする。

#### Acceptance Criteria

1. WHEN ドキュメントがSphinxの拡張機能を説明する THEN ドキュメント SHALL `app.add_node()`がSphinxの標準APIであることを明記する
2. WHERE `app.add_node()`の説明 THE ドキュメント SHALL ビルダーごとにvisitor関数を登録する方法を説明する
3. WHERE 実装アーキテクチャの説明 THE ドキュメント SHALL 「ビルダー側で独自レジストリは不要」と明記する
4. IF ユーザーがカスタムノードを登録しない THEN ドキュメント SHALL `unknown_visit()`が警告を出力しテキストを抽出することを説明する
5. WHERE 参考情報 THE ドキュメント SHALL Sphinx公式ドキュメントへのリンクを提供する

### Requirement 4: Issue #6のクローズ条件

**Objective:** Issue #6を適切にクローズするために、対応内容がIssueの要求を満たしていることを確認したい。

#### Acceptance Criteria

1. WHEN PR for Issue #6がマージされる THEN README.md SHALL カスタムノード対応の実装方法を文書化している
2. WHEN PR for Issue #6がマージされる THEN README.md SHALL 「NodeHandlerRegistryが不要」という説明を含む
3. WHEN PR for Issue #6がマージされる THEN README.md SHALL Sphinxの標準`app.add_node()` APIの使用例を含む
4. IF PRがマージされる THEN README.md SHALL 「Known Limitations」からRequirement 11の誤った記述が削除されている
5. WHERE Issue #6のクローズコメント THE コメント SHALL 「現在の実装は正しい」ことを説明する
