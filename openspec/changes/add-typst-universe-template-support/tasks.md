# Implementation Tasks

## 0. 設定名の変更 (Breaking Change) - TDD サイクル

### Phase 1: RED (Write Failing Test)
- [ ] テストを作成: `typst_template_package` 設定が動作することを確認
  - テスト名: `test_typst_template_package_config`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `typst_template_package` 設定で外部テンプレートが使用できる
  - 初期状態: テストは失敗するはず（設定名がまだ存在しない）

- [ ] テストを作成: `typst_package` 設定がエラーを出すことを確認
  - テスト名: `test_typst_package_deprecated_error`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `typst_package` 使用時にエラーメッセージが表示される
  - 初期状態: テストは失敗するはず

### Phase 2: Confirm RED
- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_typst_template_package_config -xvs
  uv run pytest tests/test_template_engine.py::test_typst_package_deprecated_error -xvs
  ```
  **期待結果**: テストが正しい理由で失敗する

### Phase 3: GREEN (Implement)
- [ ] `typsphinx/__init__.py` で設定オプションを更新
  - ファイル: `typsphinx/__init__.py:47`
  - 変更内容:
    - `typst_package` → `typst_template_package` に変更
    - `typst_package_imports` は変更なし（汎用パッケージ用として継続）

- [ ] `typsphinx/template_engine.py` で設定名を変更
  - ファイル: `typsphinx/template_engine.py`
  - 影響箇所:
    - Line 47: パラメータ名 `typst_package` → `typst_template_package`
    - Line 60: docstring 更新
    - Line 71: `self.typst_package` → `self.typst_template_package`
    - Line 186, 190, 193, 196, 199, 306: すべての `self.typst_package` 参照を更新
  - 変更内容:
    - すべての `typst_package` パラメータ/属性を `typst_template_package` に変更
    - `typst_package_imports` は変更なし
    - docstring を更新して「テンプレート専用」であることを明記

- [ ] `typsphinx/builder.py` で設定名を更新
  - ファイル: `typsphinx/builder.py`
  - 影響箇所:
    - Line 191-192: `typst_package` → `typst_template_package`
    - Line 200: パラメータ名更新
  - 変更内容:
    - config から `typst_template_package` を取得
    - TemplateEngine に渡すパラメータ名を更新

- [ ] `typsphinx/writer.py` で設定名を更新
  - ファイル: `typsphinx/writer.py:117`
  - 変更内容:
    - config から `typst_template_package` を取得
    - TemplateEngine に渡すパラメータ名を更新

- [ ] 既存テストを更新: `typst_package` → `typst_template_package`
  - 影響を受けるテストファイル:
    - `tests/test_config_other_options.py`: 4つのテスト関数
      - `test_typst_package_config_registered` → `test_typst_template_package_config_registered`
      - `test_typst_package_default_none` → `test_typst_template_package_default_none`
    - `tests/test_template_engine.py`: 複数のテスト
    - `tests/test_documentation_configuration.py`: 設定リスト
  - 変更内容:
    - すべての `typst_package` を `typst_template_package` に置換
    - テスト関数名も更新
    - docstring も更新
  - 注意: 既存テストはすべてテンプレート用途なので変更は適切（charged-ieee, diagraph など）

### Phase 4: Confirm GREEN
- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_typst_template_package_config -xvs
  uv run pytest tests/test_template_engine.py::test_typst_package_deprecated_error -xvs
  ```
  **期待結果**: テストが成功する

### Phase 5: REFACTOR (Optional)
- [ ] エラーメッセージの表示方法を改善（必要に応じて）
- [ ] リファクタリング後もテストが成功することを確認

## 1. 外部パッケージ使用時のテンプレートファイルインポートスキップ - TDD サイクル

### Phase 1: RED (Write Failing Test)
- [ ] テストを作成: 外部パッケージ使用時に `_template.typ` からのインポートが生成されないことを確認
  - テスト名: `test_skip_template_file_import_with_external_package`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `typst_template_package` 設定時は `#import "_template.typ"` が生成されない
  - 初期状態: テストは失敗するはず

### Phase 2: Confirm RED
- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_skip_template_file_import_with_external_package -xvs
  ```
  **期待結果**: テストが正しい理由で失敗する（現在は `_template.typ` からのインポートが生成されている）

### Phase 3: GREEN (Implement)
- [ ] `typsphinx/template_engine.py:render()` メソッドを修正
  - ファイル: `typsphinx/template_engine.py`
  - 変更内容:
    - `typst_template_package` が設定されている場合、`_template.typ` からのインポートをスキップ
    - 条件: `if template_file and not self.typst_template_package:`
  - 位置: 約285-286行目付近

### Phase 4: Confirm GREEN
- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_skip_template_file_import_with_external_package -xvs
  ```
  **期待結果**: テストが成功する

### Phase 5: REFACTOR (Optional)
- [ ] コードの可読性を向上（必要に応じて）
- [ ] リファクタリング後もテストが成功することを確認

## 2. 著者情報の辞書形式フォーマット - TDD サイクル

### Phase 1: RED (Write Failing Test)
- [ ] テストを作成: 辞書形式の著者情報フォーマット
  - テスト名: `test_format_authors_as_dictionary`
  - テストファイル: `tests/test_template_engine.py`
  - テストケース:
    1. デフォルト（文字列形式）: `authors: ("John Doe",)`
    2. 辞書形式（基本）: `authors: ((name: "John Doe"),)`
    3. 辞書形式（完全）: name, department, organization, email を含む
  - 初期状態: テストは失敗するはず

### Phase 2: Confirm RED
- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_format_authors_as_dictionary -xvs
  ```
  **期待結果**: テストが正しい理由で失敗する

### Phase 3: GREEN (Implement)
- [ ] `typsphinx/template_engine.py` に著者情報フォーマット機能を実装
  - ファイル: `typsphinx/template_engine.py`
  - 変更内容:
    - `typst_authors_format` 設定オプションを追加
    - `typst_author_fields` 設定オプションを追加
    - `typst_author_params` 設定オプションを追加
    - `_format_authors()` メソッドを修正して辞書形式をサポート
  - 位置: 約162-163行目付近（既存の著者情報処理）

- [ ] `typsphinx/builder.py` に設定オプションを追加
  - ファイル: `typsphinx/builder.py`
  - 変更内容: 新しい設定オプションのデフォルト値を定義

### Phase 4: Confirm GREEN
- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_format_authors_as_dictionary -xvs
  ```
  **期待結果**: テストが成功する

### Phase 5: REFACTOR (Optional)
- [ ] 著者情報フォーマット処理を別メソッドに分離（可読性向上）
- [ ] リファクタリング後もテストが成功することを確認

## 3. テンプレート固有パラメータの設定 - TDD サイクル

### Phase 1: RED (Write Failing Test)
- [ ] テストを作成: テンプレート固有パラメータ
  - テスト名: `test_template_specific_params`
  - テストファイル: `tests/test_template_engine.py`
  - テストケース:
    1. abstract パラメータ
    2. index-terms パラメータ（配列）
    3. 複数のパラメータ
    4. パラメータ未設定時は生成されない
  - 初期状態: テストは失敗するはず

### Phase 2: Confirm RED
- [ ] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_template_specific_params -xvs
  ```
  **期待結果**: テストが正しい理由で失敗する

### Phase 3: GREEN (Implement)
- [ ] `typsphinx/template_engine.py` にテンプレート固有パラメータ機能を実装
  - ファイル: `typsphinx/template_engine.py`
  - 変更内容:
    - `typst_template_params` 設定オプションを追加
    - `render()` メソッドでテンプレートパラメータを処理
    - `#show: template.with()` 呼び出しにパラメータを追加
  - 位置: テンプレート関数呼び出し部分

- [ ] `typsphinx/builder.py` に設定オプションを追加
  - ファイル: `typsphinx/builder.py`
  - 変更内容: `typst_template_params` のデフォルト値を定義

### Phase 4: Confirm GREEN
- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_template_specific_params -xvs
  ```
  **期待結果**: テストが成功する

### Phase 5: REFACTOR (Optional)
- [ ] パラメータ処理ロジックを整理
- [ ] リファクタリング後もテストが成功することを確認

## 4. Regression Testing
- [ ] 既存のテストスイートを実行
  ```bash
  uv run pytest tests/test_template_engine.py -v
  ```
  **期待結果**: 既存のすべてのテストが成功する

- [ ] template_engine 以外の関連テストを実行
  ```bash
  uv run pytest tests/test_builder.py -v
  uv run pytest tests/test_writer.py -v
  ```
  **期待結果**: すべてのテストが成功する

## 5. Integration Verification

### charged-ieee テンプレートの動作例作成
- [ ] `examples/charged-ieee/` ディレクトリを作成
- [ ] `examples/charged-ieee/conf.py` を作成
  - charged-ieee の完全な設定
  - 辞書形式の著者情報
  - テンプレート固有パラメータ（abstract, index-terms, paper-size）
- [ ] `examples/charged-ieee/source/index.rst` を作成
  - サンプル論文コンテンツ
  - セクション、コードブロック、テーブルなどを含む
- [ ] charged-ieee example でビルドを実行
  ```bash
  cd examples/charged-ieee
  uv run sphinx-build -b typst source build/typst
  uv run sphinx-build -b typstpdf source build/typstpdf
  ```
  **期待結果**: PDF が正常に生成され、IEEE フォーマットが適用される

### 手動検証
- [ ] 生成された `.typ` ファイルを確認
  - `#import "@preview/charged-ieee:0.1.4": ieee` が含まれる
  - `#import "_template.typ"` が含まれない
  - 著者情報が辞書形式になっている
  - テンプレート固有パラメータが含まれる
- [ ] 生成された PDF を目視確認
  - IEEE フォーマットが正しく適用されている
  - 著者情報が正しく表示されている
  - abstract, index-terms が表示されている

## 6. Quality Checks
- [ ] 型チェック
  ```bash
  uv run mypy typsphinx/template_engine.py
  uv run mypy typsphinx/builder.py
  ```
- [ ] リンティング
  ```bash
  uv run ruff check typsphinx/template_engine.py
  uv run ruff check typsphinx/builder.py
  ```
- [ ] フォーマット確認
  ```bash
  uv run black --check typsphinx/template_engine.py
  uv run black --check typsphinx/builder.py
  ```

## 7. Final Validation
- [ ] フルテストスイート実行
  ```bash
  uv run pytest
  ```
  **期待結果**: すべてのテストが成功する

- [ ] カバレッジ確認
  ```bash
  uv run pytest --cov=typsphinx --cov-report=term-missing
  ```
  **期待結果**: カバレッジが維持または向上している

## 8. Documentation
- [ ] CHANGELOG.md を更新
  - Breaking Changes セクション:
    - **BREAKING**: `typst_package` → `typst_template_package` に名称変更
    - 移行方法を明記
  - 新機能セクション:
    - Typst Universe テンプレートの完全サポート
    - `typst_template_package` 設定（旧 `typst_package` から名称変更）
    - `typst_authors_format`, `typst_author_fields`, `typst_author_params` 設定オプション
    - `typst_template_params` 設定オプション
    - charged-ieee example の追加

- [ ] README.md を更新（必要に応じて）
  - Typst Universe テンプレートのサポートを言及
  - Breaking change の注意事項

- [ ] docs/configuration.rst を更新
  - **構成変更**: `typst_package` を "Typst Packages" セクションから "Template Configuration" セクションに移動
    - 現在: "Typst Packages" セクション (line 214-231)
    - 移動先: "Template Configuration" セクション (line 62-135)
  - `typst_package` → `typst_template_package` に名称変更
  - `typst_package_imports` は "Typst Packages" セクションに残す（汎用パッケージ用）
  - 新しい設定オプションを "Template Configuration" セクションに追加:
    - `typst_template_package`: 外部テンプレートパッケージの指定
    - `typst_authors_format`: 著者情報のフォーマット形式
    - `typst_author_fields`: 辞書形式の著者情報フィールド
    - `typst_author_params`: 著者ごとの詳細情報
    - `typst_template_params`: テンプレート固有パラメータ
  - 各設定オプションに charged-ieee などの使用例を追加

- [ ] charged-ieee example に README を追加
  - `examples/charged-ieee/README.md`
  - 設定方法と使用方法を説明

## Task Dependencies
- Section 0 (設定名変更) は最優先で実施（すべての後続タスクに影響）
- Phase 1-2 (RED) は Phase 3-4 (GREEN) より前に完了する必要がある
- Phase 5 (REFACTOR) はオプションだが推奨
- Section 4 (Regression Testing) は Section 0-3 の GREEN フェーズ後に実行
- Section 5 (Integration Verification) は Section 0-4 の後に実行
- Section 6-8 は Section 5 の後に並行実行可能
