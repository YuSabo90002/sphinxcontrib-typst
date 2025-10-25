# Proposal: add-typst-universe-template-support

## Why

現在、Typst Universe テンプレート（charged-ieee, modern-cv など）を使用する際、以下の2つの重要な機能が不足している：

1. **著者の詳細情報を渡せない**
   - charged-ieeeは著者情報を辞書形式で要求: `authors: ((name: "John", department: "CS", email: "..."),)`
   - 現状はSphinxの`author`設定から文字列配列のみ生成: `authors: ("John Doe",)`
   - ユーザーがテンプレート内でTypstコードを書いて変換する必要がある

2. **テンプレート固有パラメータを設定できない**
   - charged-ieeeの`abstract`, `index-terms`, `paper-size`などのパラメータ
   - 現状はテンプレートファイル内でハードコーディングするしかない
   - `conf.py`から動的に設定したい

これらの機能を追加することで、Typst Universeテンプレートを設定ファイル（`conf.py`）だけで使用可能にする。

## What Changes

- **テンプレート関数設定の拡張**
  - `typst_template_function`を文字列または辞書として設定可能に
  - 文字列: 従来通り関数名のみ指定（後方互換性維持）
  - 辞書: `{"name": "関数名", "params": {パラメータ辞書}}`形式で関数とパラメータを一体的に設定
  - charged-ieeeの`abstract`, `index-terms`などを統合的に管理

- **著者情報設定の拡張**
  - 新設定オプション `typst_authors`: 著者名をキーとした詳細情報の辞書
  - charged-ieeeなどの辞書形式要求テンプレートに対応
  - 従来の`author`設定も引き続きサポート（後方互換性維持）
  - `typst_author_params`も後方互換性のために維持

- **charged-ieee テンプレートの動作例を追加**
  - `examples/charged-ieee/` ディレクトリを作成
  - 2つのアプローチを示す:
    - **アプローチ1**: `typst_template_function`辞書形式と`typst_authors`を使用（推奨・最もシンプル）
    - **アプローチ2**: カスタムテンプレート内でTypstコードで変換（柔軟性が必要な場合）

- **Typst Universe テンプレート使用ガイドをドキュメントに追加**
  - 外部テンプレートの設定方法（`typst_package`, `typst_template`の使い分け）
  - charged-ieee, modern-cv などの具体例
  - `typst_template_function`の文字列形式と辞書形式の使い分け
  - テンプレート内変換とconf.py設定の比較

## Impact

- **Affected specs**:
  - 新規作成: `template-system`（テンプレートシステム全体の仕様）

- **Affected code**:
  - `typsphinx/template_engine.py`: 著者パラメータマージ、テンプレートパラメータ追加
  - `typsphinx/builder.py`: 新設定オプションの登録
  - `examples/charged-ieee/`: 新規追加（2つのアプローチを含む）
  - `docs/configuration.rst`: 新設定オプションのドキュメント
  - `docs/`: Typst Universe テンプレート使用ガイド追加

- **Breaking changes**:
  - なし（既存の設定・動作はすべて維持）

## Related

- Issue #13: Support Typst Universe templates (charged-ieee, modern-cv, etc.)
- Typst Universe: https://typst.app/universe
- charged-ieee パッケージ: https://typst.app/universe/package/charged-ieee/
