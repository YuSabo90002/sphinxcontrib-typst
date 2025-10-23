# Proposal: add-typst-universe-template-support

## Why

現在、基本的なテンプレート機能（`typst_package`, `typst_template_function` 設定オプション）は実装されているが、Typst Universe テンプレート（charged-ieee, modern-cv など）を正しく動作させるための重要な機能が不足している。

Issue #13 で報告された3つの問題により、外部パッケージテンプレートが使用できない状態：
1. 存在しない `_template.typ` ファイルからのインポートエラー
2. charged-ieee が期待する辞書配列形式に対応していない著者情報フォーマット
3. テンプレート固有パラメータ（abstract, index-terms など）の設定不可

これらを解決することで、Typst Universe の豊富なテンプレートエコシステムとの統合が可能になる。

## What Changes

- **外部パッケージ使用時の不要なテンプレートファイルインポートを削除**
  - `typst_package` 設定時は `_template.typ` からのインポートをスキップ
  - `template_engine.py:render()` メソッドを修正

- **著者情報の辞書形式フォーマットをサポート**
  - 新設定オプション `typst_authors_format`: `"string"` (デフォルト) | `"dictionary"`
  - 新設定オプション `typst_author_fields`: 辞書に含めるフィールドリスト
  - charged-ieee など、辞書配列形式を要求するテンプレートに対応

- **テンプレート固有パラメータの設定機能を追加**
  - 新設定オプション `typst_template_params`: テンプレート固有のパラメータ辞書
  - abstract, index-terms, paper-size など任意のパラメータをサポート

- **charged-ieee テンプレートの動作例を追加**
  - `examples/charged-ieee/` ディレクトリを作成
  - 完全な設定ファイルとサンプルドキュメントを含む

- **Typst Universe テンプレート使用ガイドをドキュメントに追加**
  - 外部テンプレートの設定方法
  - charged-ieee, modern-cv などの具体例

## Impact

- **Affected specs**:
  - 新規作成: `template-system`（テンプレートシステム全体の仕様）

- **Affected code**:
  - `typsphinx/template_engine.py`: テンプレートレンダリングロジック
  - `typsphinx/builder.py`: 設定オプションの追加
  - `examples/charged-ieee/`: 新規追加
  - `docs/`: Typst Universe テンプレート使用ガイド追加

- **Breaking changes**: なし（既存動作はすべて保持、新機能は opt-in）

## Related

- Issue #13: Support Typst Universe templates (charged-ieee, modern-cv, etc.)
- Typst Universe: https://typst.app/universe
- charged-ieee パッケージ: https://typst.app/universe/package/charged-ieee/
