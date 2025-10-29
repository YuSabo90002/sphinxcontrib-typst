# Document Conversion Spec (Modified)

## ADDED Requirements

### Requirement: 画像パスの相対パス調整

ネストされたドキュメント内の画像参照は、出力ファイルの位置に基づいて相対パスを調整しなければならない (MUST)。Sphinxはすべての画像URIをソースルート相対パスに正規化するが、Typst出力では各出力ファイルの位置からの相対パスに変換する必要がある。

**Related Issue**: #69

#### Scenario: ルートドキュメントの画像パス

- **GIVEN** ルートディレクトリ（`index.rst`）に画像参照がある
- **AND** Sphinxが画像URIを`images/logo.png`として正規化する
- **WHEN** `visit_image()`が呼び出される
- **THEN** 出力パスは`images/logo.png`のまま（調整不要）
- **AND** Typstは`images/logo.png`を正しく解決する

```typst
// File: index.typ
image("images/logo.png", width: 200px)
```

#### Scenario: ネストされたドキュメントの画像パス

- **GIVEN** ネストされたドキュメント（`chapter1/section1.rst`）に画像参照がある
- **AND** Sphinxが画像URIを`images/logo.png`として正規化する（ソースルート相対）
- **WHEN** `visit_image()`が呼び出される
- **AND** `current_docname`が`chapter1/section1`である
- **THEN** 画像パスが`../images/logo.png`に調整される
- **AND** Typstは`chapter1/section1.typ`から`images/logo.png`を正しく解決する

```typst
// File: chapter1/section1.typ
image("../images/logo.png", width: 200px)
```

#### Scenario: 深くネストされたドキュメントの画像パス

- **GIVEN** 深くネストされたドキュメント（`part1/chapter1/section1.rst`）に画像参照がある
- **AND** Sphinxが画像URIを`images/logo.png`として正規化する
- **WHEN** `visit_image()`が呼び出される
- **AND** `current_docname`が`part1/chapter1/section1`である
- **THEN** 画像パスが`../../images/logo.png`に調整される
- **AND** Typstは正しい階層を遡って画像を解決する

```typst
// File: part1/chapter1/section1.typ
image("../../images/logo.png", width: 200px)
```

#### Scenario: 同一ディレクトリ内の画像参照

- **GIVEN** `chapter1/section1.rst`から`chapter1/image.jpeg`を参照する
- **AND** Sphinxが画像URIを`chapter1/image.jpeg`として正規化する
- **WHEN** `visit_image()`が呼び出される
- **AND** `current_docname`が`chapter1/section1`である
- **THEN** 画像パスが`image.jpeg`に調整される（`../`不要）
- **AND** Typstは同一ディレクトリ内の画像を正しく解決する

```typst
// File: chapter1/section1.typ
image("image.jpeg", width: 150px)
```

#### Scenario: サブディレクトリ内の画像参照（子フォルダ）

- **GIVEN** `chapter1/section1.rst`から`chapter1/img/diagram.jpeg`を参照する
- **AND** Sphinxが画像URIを`chapter1/img/diagram.jpeg`として正規化する
- **WHEN** `visit_image()`が呼び出される
- **AND** `current_docname`が`chapter1/section1`である
- **THEN** 画像パスが`img/diagram.jpeg`に調整される（子フォルダへの相対パス）
- **AND** Typstはサブディレクトリ内の画像を正しく解決する

```typst
// File: chapter1/section1.typ
image("img/diagram.jpeg", width: 250px)
```

#### Scenario: クロスディレクトリの画像参照

- **GIVEN** `chapter1/section1.rst`から`chapter2/images/diagram.png`を参照する
- **AND** Sphinxが画像URIを`chapter2/images/diagram.png`として正規化する
- **WHEN** `visit_image()`が呼び出される
- **AND** `current_docname`が`chapter1/section1`である
- **THEN** 画像パスが`../chapter2/images/diagram.png`に調整される
- **AND** Typstはクロスディレクトリ参照を正しく解決する

```typst
// File: chapter1/section1.typ
image("../chapter2/images/diagram.png", width: 300px)
```

### Requirement: 相対パス計算メソッドの実装

`TypstTranslator`は、画像URIの相対パス計算を行う`_compute_relative_image_path()`メソッドを提供しなければならない (MUST)。このメソッドは、Issue #5で実装された`_compute_relative_include_path()`と同様のロジックを使用する。

**Related**: Issue #5, `_compute_relative_include_path()` method

#### Scenario: パス計算メソッドの実装

- **GIVEN** `_compute_relative_image_path(image_uri, current_docname)`メソッドが実装されている
- **WHEN** `image_uri="images/logo.png"`, `current_docname="chapter1/section1"`で呼び出される
- **THEN** `"../images/logo.png"`を返す

#### Scenario: ルートドキュメントのケース

- **GIVEN** `current_docname`が`None`または`"index"`である
- **WHEN** `_compute_relative_image_path()`が呼び出される
- **THEN** 元の`image_uri`をそのまま返す（調整不要）

#### Scenario: 同一ディレクトリ内の画像

- **GIVEN** `image_uri="chapter1/local-image.png"`, `current_docname="chapter1/section1"`
- **WHEN** `_compute_relative_image_path()`が呼び出される
- **THEN** `"local-image.png"`を返す（同一ディレクトリ）

#### Scenario: visit_image()の統合

- **GIVEN** `visit_image()`メソッドが画像ノードを処理する
- **WHEN** ノードから`uri`を取得する
- **THEN** `_compute_relative_image_path(uri, current_docname)`を呼び出す
- **AND** 調整されたパスを`image()`関数に出力する
- **AND** `current_docname`は`self.builder.current_docname`から取得する

### Requirement: 後方互換性の維持

既存のルートドキュメントの画像参照は、変更前と同じ動作を維持しなければならない (MUST)。パス調整は、ネストされたドキュメントでのみ適用され、ルートドキュメントでは影響を与えない。

#### Scenario: 既存テストの互換性

- **GIVEN** 既存の画像関連テストが存在する
- **WHEN** パス調整機能を実装する
- **THEN** すべての既存テストが引き続きパスする
- **AND** ルートドキュメントの画像出力は変更されない

## Implementation Notes

### Reference Implementation

Issue #5の`_compute_relative_include_path()`メソッドが参考実装を提供している:
- `PurePosixPath`を使用したOS非依存のパス計算
- 共通親ディレクトリの検出
- `../`プレフィックスの計算ロジック
- 詳細なロギング

### Path Calculation Logic

```python
from pathlib import PurePosixPath

def _compute_relative_image_path(
    self, image_uri: str, current_docname: Optional[str]
) -> str:
    """
    画像URIを出力ファイル位置に基づいて相対パスに調整

    Args:
        image_uri: Sphinxから提供されたソースルート相対パス
        current_docname: 現在のドキュメント名 (例: "chapter1/section1")

    Returns:
        Typst image()用の調整された相対パス
    """
    # Similar logic to _compute_relative_include_path()
    # 1. Handle None/root document case
    # 2. Calculate relative path from current file to image
    # 3. Return adjusted path
```

### Integration Points

- **`visit_image()` method**: 画像パス調整を統合
- **`self.builder.current_docname`**: 現在のドキュメント名を取得
- **Logger**: デバッグ情報を記録（既存パターンに従う）

### Testing Strategy

1. **Unit Tests** (`test_translator.py`):
   - `test_compute_relative_image_path_root()`: ルートドキュメント
   - `test_compute_relative_image_path_nested()`: ネストされたドキュメント
   - `test_compute_relative_image_path_deep_nested()`: 深いネスト
   - `test_compute_relative_image_path_cross_directory()`: クロスディレクトリ

2. **Integration Tests** (`test_integration_advanced.py`):
   - `test_nested_documents_with_images()`: ネストされたドキュメントと画像のフルビルド
   - Typstコンパイル成功の検証
   - 画像が正しく解決されることの検証
