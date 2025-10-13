# Requirements Document

## Introduction

sphinxcontrib-typst は、Sphinx ドキュメントジェネレータに Typst 組版システムのビルダー機能を追加する拡張パッケージです。本プロジェクトの目的は、Sphinx の強力なドキュメント管理機能と Typst のモダンで高速な組版エンジンを統合し、技術文書・学術文書の高品質な PDF 出力を実現することです。

既存の LaTeX ベースの PDF 生成に比べ、Typst は高速なコンパイル、シンプルな構文、デバッグの容易さを提供します。本拡張により、Sphinx ユーザーは既存のワークフローを維持しながら、これらの利点を享受できます。

## Requirements

### Requirement 1: Sphinx ビルダー統合

**Objective:** Sphinx 拡張開発者として、sphinxcontrib-typst を標準的な Sphinx ビルダーとして実装したい。これにより、ユーザーが既存の Sphinx ワークフローで Typst 出力を生成できるようにする。

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst がインストールされる THEN `pyproject.toml` の `[project.entry-points."sphinx.builders"]` SHALL `typst = "sphinxcontrib.typst"` エントリーポイントを定義する
2. WHEN Sphinx が起動 THEN entry points経由で TypstBuilder SHALL 自動的に検出され、`conf.py` の `extensions` リストへの追加なしで利用可能になる
3. WHEN ユーザーが `sphinx-build -b typst <source> <build>` コマンドを実行 THEN Typst Builder SHALL 指定されたソースディレクトリのドキュメントを Typst 形式でビルドディレクトリに出力する
4. WHEN Sphinx が拡張をロード THEN sphinxcontrib-typst SHALL `setup()` 関数で TypstBuilder を登録し、バージョン情報と並列処理の安全性を返す
5. WHERE Sphinx のビルダーシステム内 THE TypstBuilder SHALL `sphinx.builders.Builder` 基底クラスを継承して実装される
6. IF ビルダー名が `'typst'` で指定された THEN Sphinx SHALL TypstBuilder を選択してビルドプロセスを実行する
7. WHEN ユーザーが明示的に `conf.py` の `extensions` リストに `'sphinxcontrib.typst'` を追加 THEN sphinxcontrib-typst SHALL 拡張として正常にロードされる（後方互換性のため）

### Requirement 2: Doctree から Typst への変換

**Objective:** ドキュメント作成者として、Sphinx の reStructuredText/Markdown ドキュメントを Typst マークアップに変換したい。これにより、既存の Sphinx コンテンツをそのまま Typst 出力に利用できるようにする。

#### Acceptance Criteria

1. WHEN TypstBuilder がドキュメントを処理 THEN TypstWriter SHALL Sphinx の doctree (ドキュメントツリー) を Typst マークアップに変換する
2. WHEN TypstTranslator が doctree ノードを訪問 THEN 各ノードタイプ SHALL 対応する Typst 構文に変換される
3. WHEN `nodes.section` ノードが処理される THEN Typst SHALL セクションレベルに応じた見出し記法 (`=`, `==`, `===` など) で出力される
4. WHEN `nodes.paragraph` ノードが処理される THEN 通常テキスト SHALL Typst の段落として出力される
5. WHEN `nodes.bullet_list` または `nodes.enumerated_list` ノードが処理される THEN Typst SHALL `-` (箇条書き) または `+` (番号付き) を使用したリスト構文で出力される
6. WHEN `nodes.literal_block` ノードが処理される THEN Typst SHALL ` ```言語名 ` 形式のコードブロックで出力される
7. WHEN `nodes.emphasis` または `nodes.strong` ノードが処理される THEN Typst SHALL `*斜体*` または `*太字*` などの対応する構文で出力される
8. WHEN `nodes.note`, `nodes.warning`, `nodes.important`, `nodes.tip`, `nodes.caution`, `nodes.seealso` などのアドモニションノードが処理される THEN Typst SHALL gentle-clues パッケージ (`@preview/gentle-clues`) の対応する関数（`#info[]`, `#warning[]`, `#tip[]` など）で出力される
9. WHEN アドモニションノードにカスタムタイトルが必要な場合 THEN Typst SHALL `#info(title: "タイトル")[内容]` 形式で出力される
10. WHEN gentle-clues パッケージを使用する THEN 生成される Typst ファイル SHALL `#import "@preview/gentle-clues:1.2.0": *` をインポートする
11. WHEN 他の Sphinx 拡張が生成した doctree ノード (例: `mermaid` ノード) が処理される THEN TypstTranslator SHALL ノードタイプに基づいて適切な Typst 出力を生成する

### Requirement 3: 相互参照とリンク

**Objective:** ドキュメント作成者として、Sphinx の相互参照機能を Typst で再現したい。これにより、ドキュメント間の参照リンクが Typst 出力でも機能するようにする。

#### Acceptance Criteria

1. WHEN `addnodes.pending_xref` ノード (相互参照) が処理される THEN Typst SHALL `#link(<label>)[テキスト]` 形式の参照リンクを生成する
2. WHEN `nodes.target` ノード (ラベル定義) が処理される THEN Typst SHALL `<label-name>` 形式のラベルを該当要素に埋め込む
3. WHEN `addnodes.pending_xref` の `reftype` 属性が `'doc'` (ドキュメント参照) THEN Typst SHALL ドキュメント間リンクとして適切なパスで `#link()` を生成する
4. WHEN `addnodes.toctree` ノード (目次ツリー) が処理される THEN Typst SHALL `#outline()` または手動の目次構造を生成する
5. WHEN `nodes.reference` ノード (外部リンク) が処理される THEN Typst SHALL `#link("url")[リンクテキスト]` 形式で外部リンクを生成する
6. IF 相互参照の解決に失敗 (リンク先が不明) THEN Sphinx SHALL 警告を出力し、Typst 出力には未解決参照を示すプレースホルダーを含める

### Requirement 4: 数式サポート (mitex パッケージ活用)

**Objective:** 技術文書作成者として、Sphinx の数式 (LaTeX 形式) を Typst で表示したい。mitex パッケージ (`@preview/mitex`) を活用することで、LaTeX 数式をそのまま Typst で評価し、手動変換の複雑さを回避して高い互換性を実現する。

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst がドキュメントをビルド THEN 生成される Typst ファイル SHALL `#import "@preview/mitex:0.2.4": *` (または最新版) をインポートする
2. WHEN `nodes.math_block` ノード (ブロック数式) が処理される THEN Typst SHALL `#mitex(\`LaTeX数式内容\`)` または `#mimath(\`LaTeX数式内容\`)` 形式で出力する
3. WHEN `nodes.math` ノード (インライン数式) が処理される THEN Typst SHALL `#mi(\`LaTeX数式内容\`)` 形式でインライン数式を出力する
4. WHEN LaTeX 数式コマンド (`\frac`, `\sum`, `\int`, ギリシャ文字など) が doctree ノードに含まれる THEN mitex SHALL LaTeX コードをそのまま Typst で評価・表示する
5. WHEN ユーザー定義コマンド (`\newcommand`) が doctree に含まれる THEN sphinxcontrib-typst SHALL それらを mitex ブロック内に含めて出力する
6. WHEN 数式環境 (`aligned`, `matrix`, `cases` など) が doctree ノードに含まれる THEN mitex SHALL LaTeX 環境をそのまま処理して Typst で表示する
7. WHEN `nodes.math_block` または `nodes.math` にラベルや番号が付与される THEN Typst SHALL `#mitex(\`...\`) <eq:label>` 形式で番号付き数式を生成する
8. IF mitex がサポートしていない LaTeX 構文が検出される THEN Sphinx SHALL 警告を出力し、可能な限り代替表示または Typst ネイティブ数式への変換を試みる
9. WHEN `conf.py` で `typst_use_mitex = False` が設定される THEN sphinxcontrib-typst SHALL mitex を使用せず、Typst ネイティブ数式構文への基本的な変換を実行する (フォールバック機能)

### Requirement 5: Typst ネイティブ数式のサポート

**Objective:** 技術文書作成者として、Typst ネイティブの数式記法をそのまま使用したい。LaTeX 変換のオーバーヘッドなしで Typst 特有の数式機能を活用し、よりシンプルで高速な数式表示を実現する。

#### Acceptance Criteria

1. WHEN ユーザーが Typst ネイティブ数式を指定 THEN sphinxcontrib-typst SHALL その数式を変換せずにそのまま Typst 出力に含める
2. WHEN Typst ネイティブ数式が doctree ノードとして処理される THEN 生成される Typst ファイル SHALL その数式を `$...$` (インライン) または `$ ... $` (ブロック) 形式でそのまま出力する
3. WHEN Typst 特有の数式機能 (例: `attach`, `cal`, `bb` など) が使用される THEN それらの機能 SHALL Typst でそのまま評価される
4. WHEN Typst ネイティブ数式とラベルが指定される THEN Typst SHALL `$ ... $ <eq:label>` 形式で番号付き数式を生成する
5. WHEN ユーザーが LaTeX 数式と Typst ネイティブ数式を混在使用 THEN sphinxcontrib-typst SHALL 両方を適切に処理し、それぞれ mitex または Typst ネイティブ出力を生成する
6. IF Typst ネイティブ数式に構文エラーがある THEN Sphinx SHALL 警告を出力し、エラー位置を示す

### Requirement 6: 図表の埋め込みと参照

**Objective:** ドキュメント作成者として、画像・図・表を Typst ドキュメントに埋め込み、参照できるようにしたい。これにより、視覚的要素を含むドキュメントを Typst で出力できるようにする。

#### Acceptance Criteria

1. WHEN `nodes.image` ノードが処理される THEN Typst SHALL `#image("path/to/image.png")` 形式で画像を埋め込む
2. WHEN `nodes.figure` ノード (図+キャプション) が処理される THEN Typst SHALL `#figure()` で画像とキャプションを含む図を生成する
3. WHEN `nodes.table` ノードが処理される THEN Typst SHALL `#table()` 構文で表を生成する
4. WHEN `nodes.figure` または `nodes.table` にラベル (`nodes.target`) が含まれる THEN Typst SHALL `<fig:label>` または `<tab:label>` 形式のラベルを生成する
5. WHEN `addnodes.pending_xref` で図表を参照 (`reftype='numref'` など) THEN Typst SHALL 図表番号付きの参照リンク `#ref(<label>)` を生成する
6. WHEN sphinxcontrib-mermaid など他の拡張が生成した図ノード (例: `mermaid` ノード → `nodes.image`) が処理される THEN Typst SHALL ノードタイプに基づいて適切に画像として埋め込む
7. IF 画像ファイルのパスが解決できない THEN Sphinx SHALL 警告を出力し、Typst にはプレースホルダー画像または代替テキストを含める

### Requirement 7: コードハイライト

**Objective:** ソフトウェアドキュメント作成者として、ソースコードのシンタックスハイライトを Typst で実現したい。これにより、API ドキュメントや技術チュートリアルのコードが読みやすくなる。

#### Acceptance Criteria

1. WHEN `nodes.literal_block` ノードの `language` 属性が設定されている THEN Typst SHALL ` ```言語名 ` 形式でコードブロックを生成する
2. WHEN `nodes.literal_block` に Pygments などの強調表示情報が含まれる THEN Typst SHALL 可能な限り対応するハイライト情報を保持する
3. WHEN `nodes.literal_block` に `linenos` (行番号) 属性が設定されている THEN Typst SHALL 行番号付きコードブロックを生成する (Typst のサポート範囲内)
4. WHEN `nodes.literal_block` に `highlight_args` でハイライト行が指定されている THEN Typst SHALL 該当行を視覚的に強調する (Typst の機能に応じて)
5. IF Typst が `nodes.literal_block` の `language` 属性に対応していない THEN プレーンなコードブロックとして出力し、警告を記録する

### Requirement 8: テンプレートとカスタマイズ

**Objective:** ドキュメント管理者として、Typst 出力のスタイルとレイアウトをカスタマイズしたい。各 Typst テンプレートが持つ異なるパラメータ仕様を吸収し、組織のブランディングや文書規格に合わせた出力を生成できるようにする。

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst がインストールされる THEN デフォルトの Typst テンプレート SHALL パッケージに含まれる
2. WHEN ユーザーがカスタム Typst テンプレートを指定 THEN sphinxcontrib-typst SHALL そのテンプレートを使用して出力を生成する
3. WHEN Sphinx のメタデータ (`project`, `author`, `release` など) が存在 THEN sphinxcontrib-typst SHALL それらをテンプレートに渡す
4. WHEN Typst テンプレートが異なるパラメータ名を要求 (例: `title` vs `doc-title`) THEN ユーザー SHALL Sphinx メタデータとテンプレートパラメータのマッピングを定義できる
5. WHEN マッピング設定が未指定 THEN sphinxcontrib-typst SHALL 標準的なメタデータ名の変換を自動的に適用する
6. WHEN Typst Universe の外部テンプレートパッケージを使用 THEN ユーザー SHALL パッケージとテンプレート関数を指定できる
7. WHERE ユーザーのプロジェクトディレクトリ THE sphinxcontrib-typst SHALL カスタムテンプレートファイルを優先的に検索する
8. WHEN テンプレートパラメータが配列や複雑な構造を要求 THEN ユーザー SHALL Sphinx メタデータから必要な形式に変換するマッピングを定義できる
9. IF 指定されたテンプレートが見つからない THEN sphinxcontrib-typst SHALL デフォルトテンプレートを使用し、警告を出力する
10. WHEN 用紙サイズ、フォントサイズなどの文書設定が指定される THEN それらの値 SHALL テンプレートに渡されて反映される
11. WHEN デフォルトテンプレートが使用される THEN テンプレート SHALL `#outline()` を含み、マスタードキュメントの目次を自動生成する
12. WHEN `toctree` のオプション (`:maxdepth:`, `:numbered:`, `:caption:` など) が指定される THEN それらの値 SHALL テンプレートパラメータとして渡される
13. WHEN テンプレートが `#outline()` をカスタマイズ THEN テンプレート SHALL 受け取ったパラメータ (maxdepth, numbered など) を `#outline()` の引数に反映する
14. WHERE ドキュメント本文 THE `#outline()` SHALL 含まれず、テンプレートレベルでのみ管理される

### Requirement 9: 自己完結型 PDF 生成

**Objective:** ドキュメント管理者として、外部依存なしで Typst から PDF への変換を完結させたい。ユーザーは `pip install sphinxcontrib-typst` だけで PDF 生成まで実行でき、追加のツールインストールが不要になる。

#### Acceptance Criteria

1. WHEN sphinxcontrib-typst がインストールされる THEN Typst コンパイラ機能 SHALL 依存関係として自動的に利用可能になる
2. WHEN PDF 生成が要求される THEN sphinxcontrib-typst SHALL 外部 CLI ツールに依存せず、Python 環境内で Typst コンパイルを実行する
3. WHEN `sphinx-build -b typstpdf` コマンドが実行される THEN ビルダー SHALL Typst マークアップを PDF に変換し、ビルドディレクトリに出力する
4. WHEN PDF 生成が成功 THEN ビルドディレクトリ SHALL `.typ` ファイルと対応する `.pdf` ファイルの両方を含む
5. WHEN CI/CD 環境で実行される THEN sphinxcontrib-typst のインストールのみで PDF 生成が動作する (追加セットアップ不要)
6. IF Python バインディング経由での PDF 生成が失敗 THEN 外部 Typst CLI へのフォールバック SHALL 試行され、見つからない場合は明確なエラーメッセージを表示する
7. WHEN Typst の新しいバージョンが必要 THEN 依存パッケージの更新 SHALL 自動的に新しいコンパイラを提供する

### Requirement 10: エラーハンドリングと警告

**Objective:** 拡張開発者として、変換エラーや警告を適切にユーザーに伝えたい。これにより、ユーザーがドキュメントの問題を迅速に特定・修正できるようにする。

#### Acceptance Criteria

1. WHEN 変換できない doctree ノードが検出される THEN Sphinx の警告システム SHALL 該当ノードの種類と場所を含む警告を出力する
2. WHEN Typst 構文として無効な文字や構造が検出される THEN エスケープ処理または代替出力 SHALL 適用され、警告が記録される
3. WHEN テンプレートやリソースファイルが見つからない THEN 明確なエラーメッセージ SHALL ファイルパスと原因を含めて表示される
4. WHEN ビルドプロセス中に例外が発生 THEN Sphinx SHALL 例外の詳細とトレースバックを出力し、ビルドを中断する
5. WHERE デバッグモード (`SPHINX_TYPST_DEBUG=1`) THE 詳細なログ SHALL 変換の各ステップと中間データを出力する

### Requirement 11: 拡張性とプラグイン対応

**Objective:** 拡張開発者として、他の Sphinx 拡張や独自のカスタムノードに対応できるようにしたい。これにより、sphinxcontrib-typst が既存の Sphinx エコシステムと共存できるようにする。

#### Acceptance Criteria

1. WHEN カスタム doctree ノードが存在 THEN TypstTranslator SHALL ノードタイプごとに登録された変換ハンドラーを呼び出す
2. WHEN ユーザーが独自の Typst 変換関数を登録 THEN Sphinx の `app.add_node()` または類似の API SHALL カスタム変換ロジックを受け入れる
3. WHEN 他の Sphinx 拡張 (例: sphinx-autodoc) と併用される THEN sphinxcontrib-typst SHALL 他の拡張が生成した doctree を正しく処理する
4. WHERE Sphinx のイベントフック (例: `doctree-resolved`) THE sphinxcontrib-typst SHALL 必要に応じてイベントハンドラーを登録してカスタム処理を実行する
5. IF 未知のノードタイプが検出される THEN デフォルトの変換動作 SHALL ノードのテキストコンテンツを抽出し、警告を出力する

### Requirement 12: テストとドキュメント

**Objective:** プロジェクトメンテナーとして、sphinxcontrib-typst の品質を保証し、ユーザーが容易に使用できるようにしたい。これにより、信頼性の高い拡張として提供できるようにする。

#### Acceptance Criteria

1. WHEN 新しい機能が実装される THEN 対応するユニットテスト SHALL pytest で実行可能な形で追加される
2. WHEN ビルドプロセス全体をテスト THEN 統合テスト SHALL サンプル Sphinx プロジェクトをビルドし、生成された Typst 出力を検証する
3. WHEN ドキュメントが更新される THEN 使用例 SHALL `examples/` ディレクトリに実際に動作するサンプルプロジェクトとして含まれる
4. WHEN ユーザーがインストールガイドを参照 THEN `docs/installation.rst` SHALL インストール手順、依存関係、動作環境を明記する
5. WHEN ユーザーが設定オプションを確認 THEN `docs/configuration.rst` SHALL すべての `conf.py` 設定項目とその説明を含む
6. WHERE プロジェクトの CI/CD パイプライン THE 自動テスト SHALL すべてのテストを実行し、コードカバレッジレポートを生成する

### Requirement 13: 複数ドキュメントの統合と toctree 処理

**Objective:** ドキュメント作成者として、複数の reStructuredText ファイルを含むプロジェクトを Typst で適切にビルドしたい。各 .rst ファイルは独立した .typ ファイルとして生成され、`toctree` ディレクティブは Typst の `#include()` を使用してドキュメントを統合する。目次（`#outline()`）はテンプレートで管理し、ドキュメント本文には含めない。

#### Acceptance Criteria

1. WHEN 各 reStructuredText ファイルがビルドされる THEN TypstBuilder SHALL 対応する独立した .typ ファイルを生成する
2. WHEN `addnodes.toctree` ノードが TypstTranslator で処理される THEN 参照された各ドキュメントに対して `#include("relative/path/to/doc.typ")` SHALL 生成される
3. WHEN `toctree` の `entries` 属性から参照ドキュメントのリストを取得 THEN 各エントリー SHALL ビルド出力ディレクトリを基準とした相対パスに変換される
4. WHEN `toctree` で参照されたドキュメントパスが "intro" の場合 THEN Typst SHALL `#include("intro.typ")` を生成する
5. WHEN `toctree` で参照されたドキュメントパスが "chapter1/section" の場合 THEN Typst SHALL `#include("chapter1/section.typ")` を生成する
6. WHEN マスタードキュメント (例: index.rst) がビルドされる THEN 生成される .typ ファイル SHALL `#include()` ディレクティブを含み、参照された全ドキュメントを統合する
7. WHEN Typst がマスタードキュメントをコンパイル THEN `#include()` により参照された .typ ファイル SHALL 順次読み込まれ、単一の PDF として出力される
8. WHEN `#outline()` (目次) が必要 THEN Typst テンプレート SHALL `#outline()` を含み、ドキュメント本文には含めない
9. WHEN `toctree` オプション (`:maxdepth:`, `:numbered:` など) が指定される THEN それらのオプション SHALL テンプレートパラメータとして渡され、テンプレート側で `#outline()` の設定に反映される
10. IF `toctree` で参照されたドキュメントファイルが存在しない THEN Sphinx SHALL 警告を出力し、該当の `#include()` はコメントアウトまたはスキップされる
11. WHEN `toctree` ノード処理時に `addnodes.toctree` ノードが `raise nodes.SkipNode` を実行 THEN 子ノードの処理 SHALL スキップされる (toctree 自体はドキュメント内容を持たない)
12. WHERE ビルド出力ディレクトリ THE すべての .typ ファイル SHALL フラットまたはソースと同じディレクトリ構造で配置され、`#include()` の相対パスはその構造に従う
13. WHEN `toctree` で参照されたドキュメントが `#include()` で挿入される THEN 見出しレベル SHALL Sphinx の toctree 動作に合わせて1レベル下げられる
14. WHEN `#include()` を生成する際に見出しレベルを調整 THEN Typst SHALL `{ #set heading(offset: 1); #include("doc.typ") }` のようにブロックスコープ内で `#set heading(offset: 1)` を適用する
15. WHERE `#include()` のスコープ THE 見出しレベルのオフセット SHALL `#include()` ブロック内でのみ適用され、マスタードキュメントの見出しレベルには影響しない

**補足説明:**
- 各 .rst ファイルは独立した .typ ファイルとして生成されます
- `toctree` は Typst の `#include()` に変換され、Typst コンパイル時にファイルが統合されます
- `#outline()` (目次) はテンプレートファイルで管理し、ドキュメント本文には含めません
- toctree のオプション (`:maxdepth:`, `:numbered:` など) はテンプレートパラメータとして渡し、テンプレート側で `#outline()` に反映します
- **見出しレベル調整**: Sphinx の toctree では参照されたドキュメントの見出しが1レベル下がります。Typst の `#include()` は単純なファイル挿入のため、`#set heading(offset: 1)` を使用して見出しレベルを調整します
- この方式により、Typst の機能を最大限活用し、ファイル分割とモジュール性を維持できます
