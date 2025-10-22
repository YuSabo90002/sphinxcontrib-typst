# Change Proposal: Raw Typst Directive Support

## Why

現在、reStructuredTextドキュメント内で`.. raw::`ディレクティブが使用された場合、トランスレータは`unknown node type: <raw>`という警告を生成し、コンテンツを出力しません。これにより、ユーザーはTypst固有の機能を直接使用できず、すべての機能をSphinx/docutilsディレクティブでカバーする必要があります。

ユーザーは以下のような場合にネイティブTypstコードを埋め込む必要があります：
- Sphinx/docutilsディレクティブでカバーされていないTypst固有の機能を使用したい
- トランスレータを拡張せずに高度なTypstフォーマットを有効にしたい
- Typst出力とHTML/LaTeX出力で条件付きコンテンツを含めたい
- 特定のフォーマット要件のためにカスタムTypstコードを埋め込みたい

例えば、カスタムボックススタイリングのためにTypstの`#rect()`関数を使用したり、同等のreStructuredTextディレクティブが存在しない他のTypst関数を使用したい場合があります。

## What Changes

- `TypstTranslator`クラスに`visit_raw`および`depart_raw`メソッドを実装
- `format='typst'`の場合、rawコンテンツをそのまま出力に渡す
- 他のフォーマット（html、latexなど）の場合、コンテンツをスキップ
- スキップされたコンテンツについて、ユーザーが何が無視されているかを理解できるようにログ警告を出力

**Note**: この変更は破壊的変更ではありません。既存の動作（警告を表示してスキップ）を改善し、`format='typst'`の場合に適切に処理するようになります。

## Impact

- **影響を受ける仕様**: `document-conversion`
- **影響を受けるコード**:
  - `sphinxcontrib/typst/translator.py` - `visit_raw`/`depart_raw`メソッドの追加
  - `tests/` - rawディレクティブのテストケースの追加
- **後方互換性**: 既存の機能には影響なし（新機能の追加）
- **ユーザーへの影響**: ポジティブ - ユーザーはTypst固有のコードを直接埋め込めるようになる
