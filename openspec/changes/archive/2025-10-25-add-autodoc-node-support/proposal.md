# Proposal: Add Autodoc Node Support

## Why

現在、typsphinxはautodoc（Sphinx自動APIドキュメント生成拡張）が生成するノードタイプをサポートしていません。このため：

1. **PDFビルド失敗**: API referenceページを含むドキュメントのPDFビルドが失敗
2. **大量の警告**: 1896個の "unknown node type" 警告が発生
3. **dogfooding不可**: typsphinx自身のAPIドキュメントをtypstpdfで生成できない
4. **ユーザー体験の低下**: autodocを使用する一般的なSphinxプロジェクトでPDFが生成できない

Issue #55で報告された通り、以下の15種類のノードタイプが未対応：

**Core autodoc nodes (9種類):**
- `index` - APIインデックスエントリ
- `desc` - API説明コンテナ（class、method、attributeなど）
- `desc_signature` - 関数/クラスシグネチャ
- `desc_content` - 説明コンテンツ
- `desc_annotation` - 型注釈（`class`キーワードなど）
- `desc_addname` - モジュール名プレフィックス
- `desc_name` - 関数/クラス名
- `desc_parameterlist` - パラメータリスト
- `desc_parameter` - 個別のパラメータ

**Field list nodes (4種類):**
- `field_list` - パラメータ/返り値ドキュメントのコンテナ
- `field` - 個別のフィールド
- `field_name` - フィールド名（"Parameters", "Returns"など）
- `field_body` - フィールドコンテンツ

**Additional nodes (2種類):**
- `rubric` - APIドキュメント内のセクション見出し
- `title_reference` - タイトル参照

## What Changes

### 1. translator.pyの拡張

`typsphinx/translator.py`に以下のvisitor/departメソッドを追加：

#### Index nodes
- `visit_index()` / `depart_index()` - インデックスエントリをスキップ（Typstには不要）

#### Desc nodes (API descriptions)
- `visit_desc()` / `depart_desc()` - API説明ブロック全体のコンテナ
- `visit_desc_signature()` / `depart_desc_signature()` - シグネチャ部分（関数名、パラメータなど）
- `visit_desc_content()` / `depart_desc_content()` - 説明コンテンツ部分
- `visit_desc_annotation()` / `depart_desc_annotation()` - 型注釈・キーワード
- `visit_desc_addname()` / `depart_desc_addname()` - モジュール名プレフィックス
- `visit_desc_name()` / `depart_desc_name()` - 関数/クラス名
- `visit_desc_parameterlist()` / `depart_desc_parameterlist()` - パラメータリスト全体
- `visit_desc_parameter()` / `depart_desc_parameter()` - 個別パラメータ

#### Field list nodes
- `visit_field_list()` / `depart_field_list()` - フィールドリスト全体
- `visit_field()` / `depart_field()` - 個別フィールド
- `visit_field_name()` / `depart_field_name()` - フィールド名
- `visit_field_body()` / `depart_field_body()` - フィールドボディ

#### Additional nodes
- `visit_rubric()` / `depart_rubric()` - セクション見出し
- `visit_title_reference()` / `depart_title_reference()` - タイトル参照

### 2. Typst出力フォーマット

autodocノードのTypst表現：

- **クラス/関数シグネチャ**: `#strong[class TypstBuilder(app, env)]` 形式
- **パラメータリスト**: シンプルなテキスト表現
- **フィールドリスト**: 見出し（`*Parameters:*`）+ 箇条書きリスト
- **index**: 出力なし（PDFではインデックスを生成しない）

### 3. テストの追加

- autodocノードのユニットテスト（各ノードタイプ）
- 実際のAPIドキュメントビルドの統合テスト
- Issue #55で特定された問題の回帰テスト

## Impact

### Affected specs

既存specの修正：
- `document-conversion`: autodocノードサポートを追加

新規specの追加：
- なし（既存capabilityの拡張）

### Affected code

変更ファイル：
- `typsphinx/translator.py` - 30個の新しいvisitor/departメソッド（15ノードタイプ × 2）
- `tests/test_autodoc_nodes.py` - 新規テストファイル
- `tests/test_integration_autodoc.py` - 新規統合テストファイル

### Breaking changes

なし - 既存機能への影響なし、新機能の追加のみ

### User-visible changes

- ✅ autodocを使用するドキュメントのPDFビルドが成功
- ✅ API referenceページがPDFに含まれる
- ✅ typsphinx自身のドキュメントで完全なPDF生成が可能（dogfooding）
- ✅ "unknown node type" 警告が消える

## Alternatives Considered

### 1. autodocノードを無視する（現状維持）
- 問題: ユーザーはAPIドキュメントをPDFで生成できない
- 問題: typsphinx自身のドキュメントが不完全

### 2. HTMLのみサポート、PDFは諦める
- 問題: PDFビルダー（typstpdf）の価値が大幅に低下
- 問題: APIドキュメントが必要なプロジェクトでtypsphinxを使えない

### 3. 段階的実装（基本ノードのみ）
- メリット: より早くリリース可能
- デメリット: 不完全なサポートで依然として警告が出る
- **却下理由**: 15ノードタイプは相互依存しており、部分実装では効果が薄い

### 4. すべてのautodocノードを実装（選択）
- **メリット**: 完全なサポート、警告ゼロ、dogfooding可能
- **メリット**: 一般的なSphinxプロジェクトで広く使える
- **実装コスト**: 合理的（30メソッド、既存パターンに従う）

## Implementation Notes

### 実装方針

1. **シンプルさ優先**: 複雑なTypst書式設定より、読みやすさを重視
2. **既存パターン踏襲**: 他のノードと同じvisitor/departパターン
3. **段階的テスト**: ノードタイプごとにテストを追加

### Typst出力例

```typst
// Class signature
#strong[class TypstBuilder(app, env)]

Base class: Builder

Builder class for Typst output format.

*Parameters:*
- *app* (Sphinx) – Sphinx application
- *env* (BuildEnvironment) – Build environment

*Methods:*

#strong[init()]

Initialize the builder.

*Return type:* None
```

### 技術的考慮事項

- **ネスト構造**: desc_content内にfield_listがネストされる構造を正しく処理
- **空ノード**: 空のdesc_annotationなどを適切にスキップ
- **エスケープ**: Typst特殊文字のエスケープ処理
