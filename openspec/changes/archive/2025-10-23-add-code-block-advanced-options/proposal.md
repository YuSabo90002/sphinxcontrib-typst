# add-code-block-advanced-options

## Why

現在、sphinxcontrib-typstは`:linenos:`、`:emphasize-lines:`、`:caption:`、`:name:`の4つのcode-blockオプションをサポートしていますが、Sphinxが標準で提供する`:lineno-start:`と`:dedent:`オプションには未対応です。これらのオプションは、特定の行番号から始まるコードスニペットの表示や、インデントされたコード（クラスや関数内のコード）の引用時に便利な機能です。

Issue #31で報告されているように、これらのオプションのサポートを追加することで、Sphinxの標準code-blockディレクティブとの互換性が向上し、ユーザーの利便性が大幅に改善されます。

## What Changes

以下の2つの新機能を追加します：

- **`:lineno-start:`オプションのサポート**: 行番号の開始値を指定できるようにします。codlyパッケージの`start`パラメータを使用して実装します
- **`:dedent:`オプションのサポート**: コードブロックの先頭の空白を削除できるようにします。Pythonの`textwrap.dedent()`を使用して、コンテンツの前処理を行います

これらの変更により、Sphinx標準のcode-blockディレクティブで利用可能な8つの主要オプションのうち、6つ（75%）をサポートすることになります。

## Impact

- **影響を受ける仕様**: `code-block-rendering`
- **影響を受けるコード**:
  - `sphinxcontrib/typst/translator.py` - `visit_literal_block()`メソッドに`:lineno-start:`と`:dedent:`の処理を追加
  - `tests/test_translator.py` - 新機能のテストケースを追加

- **破壊的変更**: なし。既存の機能には影響せず、新しいオプションのサポートを追加するのみです
- **依存関係の変更**: なし。`textwrap`は標準ライブラリであり、codlyパッケージは既に使用されています
