# Proposal: Copy Image Files to Output Directory

## Why

現在、`typstpdf`ビルダーでPDF出力を生成する際、reStructuredTextドキュメントで参照されている画像ファイルが出力ディレクトリにコピーされない。これにより、Typstコンパイル時に「file not found」エラーが発生し、PDFビルドが失敗する。

Sphinxの標準的なビルダー（LaTeX、HTML等）は`post_process_images()`と`copy_image_files()`メソッドを実装して画像ファイルを自動的にコピーする。`TypstBuilder`と`TypstPDFBuilder`でも同様の機能を実装することで、画像を含むドキュメントの正常なビルドが可能になる。

## What Changes

- `TypstBuilder`に`post_process_images()`メソッドを追加して`self.images`に画像を追跡
- `copy_image_files()`メソッドを実装して画像をソースから出力ディレクトリにコピー
- `finish()`メソッドを拡張して画像コピーを実行
- 画像パスの解決とコピー処理の実装

## Impact

- **影響を受ける仕様**: `document-conversion`
- **影響を受けるコード**:
  - `typsphinx/builder.py` (`TypstBuilder`, `TypstPDFBuilder`)
- **破壊的変更**: なし - 既存の動作に機能を追加
- **ユーザーメリット**:
  - 画像を含むドキュメントのPDFビルドが成功する
  - Sphinxの標準的なビルダーAPIに準拠
  - 追加設定不要で画像が自動的にコピーされる

## Related Issues

- Fixes #38: Image files are not copied to output directory
