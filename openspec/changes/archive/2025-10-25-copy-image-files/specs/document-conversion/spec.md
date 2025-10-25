# Spec Delta: document-conversion

## ADDED Requirements

### Requirement: 画像ファイルの出力ディレクトリへのコピー

ビルダーは、ドキュメント内で参照されている画像ファイルを出力ディレクトリに自動的にコピーしなければならない (MUST)。これにより、Typstコンパイル時に画像ファイルが利用可能になる。

#### Scenario: 単一画像のコピー

- **GIVEN** reStructuredTextドキュメントに`.. image:: sample.png`ディレクティブが含まれる
- **AND** `sample.png`がソースディレクトリに存在する
- **WHEN** `typstpdf`ビルダーでビルドする
- **THEN** `sample.png`が出力ディレクトリにコピーされる
- **AND** PDF生成が成功する

#### Scenario: 複数画像のコピー

- **GIVEN** ドキュメントに複数の画像ディレクティブが含まれる
- **AND** すべての画像ファイルがソースディレクトリに存在する
- **WHEN** ビルドを実行する
- **THEN** すべての画像ファイルが出力ディレクトリにコピーされる

#### Scenario: サブディレクトリ内の画像

- **GIVEN** `.. image:: images/sample.png`のように相対パスで画像が参照される
- **AND** `images/sample.png`がソースディレクトリに存在する
- **WHEN** ビルドを実行する
- **THEN** 出力ディレクトリに`images/`ディレクトリが作成される
- **AND** `images/sample.png`が正しくコピーされる

#### Scenario: 画像なしドキュメント（後方互換性）

- **GIVEN** ドキュメントに画像ディレクティブが含まれない
- **WHEN** ビルドを実行する
- **THEN** ビルドは正常に完了する
- **AND** 既存の動作が維持される

### Requirement: 画像追跡の実装

ビルダーは、ドキュメントツリーから画像参照を収集し、`self.images`辞書に追跡しなければならない (MUST)。

#### Scenario: post_process_images()の実装

- **GIVEN** ドキュメントに画像が含まれる
- **WHEN** `post_process_images()`が呼び出される
- **THEN** `self.images`辞書が初期化される
- **AND** ドキュメント内のすべての画像パスが`self.images`に追加される

#### Scenario: 画像パスの解決

- **GIVEN** 相対パスで画像が参照される
- **WHEN** 画像を追跡する
- **THEN** ソースディレクトリからの相対パスが正しく解決される
- **AND** 出力ディレクトリ内の対応するパスが計算される

## MODIFIED Requirements

なし

## REMOVED Requirements

なし
