# Change Proposal: Code Block Directive Options Support

## Why

現在、reStructuredTextのcode-blockディレクティブで指定される複数のオプションが適切に処理されていません：

1. **`:linenos:`オプション** - 完全に無視され、行番号が出力されない
2. **`:caption:`と`:name:`オプション** - `container`ノードが作成され、「unknown node type」警告が発生し、キャプションが plain text として出力される
3. **`:emphasize-lines:`オプション** - 正しく動作している ✓

これにより、以下の問題が発生しています：

- ユーザーがコードブロックに行番号を表示できない
- コードブロックにキャプションやラベルを付けられない
- コードブロックを図として参照できない
- 不必要な警告メッセージが表示される

これらの機能は、技術文書やチュートリアルでコードを説明する際に非常に重要です。

## What Changes

### 1. `:linenos:`オプションのサポート
- `visit_literal_block()`メソッドで`node.get('linenos')`をチェック
- codlyの行番号機能を有効化（codlyは既にテンプレートで初期化されている）

### 2. `:caption:`と`:name:`オプションのサポート
- `visit_container()`と`depart_container()`メソッドを実装
- `literal-block-wrapper`クラスを持つcontainerノードを処理
- キャプション付きコードブロックを`#figure()`でラップ
- `:name:`オプションからラベルを生成

### 3. 既存機能の維持
- `:emphasize-lines:`オプションは既に動作しているため、影響を与えない
- 既存のコードブロック処理ロジックとの互換性を保つ

**Note**: これは破壊的変更ではありません。既存の動作を拡張し、より多くのreStructuredTextディレクティブオプションをサポートします。

## Impact

- **影響を受けるspec**: 新しいspec `code-block-rendering`を作成
- **影響を受けるコード**:
  - `sphinxcontrib/typst/translator.py` - `visit_literal_block()`の拡張、`visit_container()`/`depart_container()`の追加
  - `tests/test_translator.py` - コードブロックオプションのテストケース追加
- **後方互換性**: 既存の機能には影響なし（新機能の追加）
- **ユーザーへの影響**: ポジティブ - より多くのreStructuredTextコードブロックオプションが使用可能になる
- **修正されるIssue**: #20
