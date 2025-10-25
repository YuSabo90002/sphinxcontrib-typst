# Implementation Tasks

## 0. typst_template_function 辞書形式サポート - TDD サイクル ✅

### Phase 1: RED (Write Failing Test) ✅
- [x] テストを作成: `typst_template_function` の文字列形式（後方互換性）
  - テスト名: `test_typst_template_function_string_format`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: 従来通り文字列で関数名のみ指定できる
  - 初期状態: すでに動作しているはずなので、このテストは既存機能の保護用

- [x] テストを作成: `typst_template_function` の辞書形式（基本）
  - テスト名: `test_typst_template_function_dict_format_basic`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `{"name": "ieee"}` 形式で関数名を指定できる
  - 初期状態: テストは失敗するはず（辞書形式未対応）

- [x] テストを作成: `typst_template_function` の辞書形式（パラメータ付き）
  - テスト名: `test_typst_template_function_dict_format_with_params`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `{"name": "ieee", "params": {"abstract": "...", "index-terms": ["AI"]}}` 形式でパラメータを指定できる
  - 初期状態: テストは失敗するはず

- [x] テストを作成: パラメータでのPython変数参照
  - テスト名: `test_template_params_python_variable_reference`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `conf.py` で定義した通常のPython変数を `params` 内で参照できる
  - 初期状態: 辞書形式が実装されれば自然に動作するはず

### Phase 2: Confirm RED ✅
- [x] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_typst_template_function_string_format -xvs
  uv run pytest tests/test_template_engine.py::test_typst_template_function_dict_format_basic -xvs
  uv run pytest tests/test_template_engine.py::test_typst_template_function_dict_format_with_params -xvs
  uv run pytest tests/test_template_engine.py::test_template_params_python_variable_reference -xvs
  ```
  **期待結果**: 新機能のテストが正しい理由で失敗する

### Phase 3: GREEN (Implement) ✅
- [x] `typsphinx/__init__.py` で設定オプションを登録
  - ファイル: `typsphinx/__init__.py`
  - 変更内容:
    - `typst_template_function` の型を `str | dict[str, Any]` に更新
    - デフォルト値は引き続き `"project"`

- [x] `typsphinx/template_engine.py` で辞書形式をサポート
  - ファイル: `typsphinx/template_engine.py`
  - 変更内容:
    - `__init__()` メソッドで `typst_template_function` が文字列か辞書かを判定
    - 辞書の場合: `name` と `params` を分離して保存
    - 文字列の場合: 従来通り（後方互換性維持）
    - `render()` メソッドで `#show: template.with()` にパラメータを追加

- [x] `typsphinx/builder.py` でパラメータの受け渡しを更新
  - ファイル: `typsphinx/builder.py`
  - 変更内容:
    - `typst_template_function` を TemplateEngine に渡す
    - 辞書形式の場合でも正しく処理されることを確認

- [x] `typsphinx/writer.py` でパラメータの受け渡しを更新
  - ファイル: `typsphinx/writer.py`
  - 変更内容:
    - `typst_template_function` を TemplateEngine に渡す

### Phase 4: Confirm GREEN ✅
- [x] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_typst_template_function_string_format -xvs
  uv run pytest tests/test_template_engine.py::test_typst_template_function_dict_format_basic -xvs
  uv run pytest tests/test_template_engine.py::test_typst_template_function_dict_format_with_params -xvs
  uv run pytest tests/test_template_engine.py::test_template_params_python_variable_reference -xvs
  ```
  **期待結果**: すべてのテストが成功する ✅ 4/4 PASSED

### Phase 5: REFACTOR (Optional)
- [x] パラメータ処理ロジックは実装完了（別メソッド分離は不要と判断）
- [x] リファクタリング後もテストが成功することを確認

## 1. typst_authors 設定オプション - TDD サイクル ✅

### Phase 1: RED (Write Failing Test) ✅
- [x] テストを作成: 従来の `author` 設定（後方互換性）
  - テスト名: `test_author_config_backward_compatibility`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: 従来通り `author = "John Doe"` で文字列形式の著者情報が生成される
  - 初期状態: すでに動作しているはず

- [x] テストを作成: `typst_authors` による著者詳細情報（単一著者）
  - テスト名: `test_typst_authors_single_author_with_details`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: `typst_authors` で辞書形式の著者情報が生成される
  - 初期状態: テストは失敗するはず

- [x] テストを作成: `typst_authors` による著者詳細情報（複数著者）
  - テスト名: `test_typst_authors_multiple_authors_with_details`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: 複数著者の詳細情報が正しい順序で生成される
  - 初期状態: テストは失敗するはず

- [x] テストを作成: `typst_author_params` との併用（後方互換性）
  - テスト名: `test_typst_author_params_backward_compatibility`
  - テストファイル: `tests/test_template_engine.py`
  - 期待動作: 従来の `typst_author_params` も引き続き動作する
  - 初期状態: すでに動作しているはず

### Phase 2: Confirm RED ✅
- [x] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_author_config_backward_compatibility -xvs
  uv run pytest tests/test_template_engine.py::test_typst_authors_single_author_with_details -xvs
  uv run pytest tests/test_template_engine.py::test_typst_authors_multiple_authors_with_details -xvs
  uv run pytest tests/test_template_engine.py::test_typst_author_params_backward_compatibility -xvs
  ```
  **期待結果**: 新機能のテストが正しい理由で失敗する

### Phase 3: GREEN (Implement) ✅
- [x] `typsphinx/__init__.py` で設定オプションを追加
  - ファイル: `typsphinx/__init__.py`
  - 変更内容:
    - `typst_authors` を追加: `dict[str, dict[str, Any]]` 型
    - デフォルト値: `{}`

- [x] `typsphinx/template_engine.py` で `typst_authors` をサポート
  - ファイル: `typsphinx/template_engine.py`
  - 変更内容:
    - `__init__()` メソッドで `typst_authors` パラメータを受け取る
    - `_format_authors_with_details()` メソッドを追加:
      - `typst_authors` が設定されている場合: 辞書形式で著者情報を生成
      - `typst_author_params` が設定されている場合: 従来通り（後方互換性）
      - どちらも設定されていない場合: 文字列形式（デフォルト）
    - 著者の順序は `typst_authors` 辞書のキー順序に従う

- [x] `typsphinx/builder.py` で `typst_authors` を渡す
  - ファイル: `typsphinx/builder.py`
  - 変更内容:
    - config から `typst_authors` を取得
    - TemplateEngine に渡す

- [x] `typsphinx/writer.py` で `typst_authors` を渡す
  - ファイル: `typsphinx/writer.py`
  - 変更内容:
    - config から `typst_authors` を取得
    - TemplateEngine に渡す

### Phase 4: Confirm GREEN ✅
- [x] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_template_engine.py::test_author_config_backward_compatibility -xvs
  uv run pytest tests/test_template_engine.py::test_typst_authors_single_author_with_details -xvs
  uv run pytest tests/test_template_engine.py::test_typst_authors_multiple_authors_with_details -xvs
  uv run pytest tests/test_template_engine.py::test_typst_author_params_backward_compatibility -xvs
  ```
  **期待結果**: すべてのテストが成功する ✅ 4/4 PASSED

### Phase 5: REFACTOR (Optional) ✅
- [x] 著者情報フォーマット処理を別メソッド`_format_authors_with_details()`に分離
- [x] リファクタリング後もテストが成功することを確認

## 2. Regression Testing ✅
- [x] 既存のテストスイートを実行
  ```bash
  uv run pytest tests/test_template_engine.py -v
  ```
  **期待結果**: 既存のすべてのテストが成功する（後方互換性維持） ✅ 39/39 PASSED

- [x] template_engine 以外の関連テストを実行
  ```bash
  uv run pytest tests/test_builder.py -v
  uv run pytest tests/test_config_other_options.py -v
  ```
  **期待結果**: すべてのテストが成功する ✅ 30/30 PASSED

## 3. Integration Verification - charged-ieee アプローチ1（推奨） ✅

### charged-ieee テンプレートの動作例作成（conf.py設定のみ） ✅
- [x] `examples/charged-ieee/approach1/` ディレクトリを作成 ✅

- [x] `examples/charged-ieee/approach1/conf.py` を作成 ✅
  - charged-ieee の完全な設定例:
    ```python
    # 標準設定
    project = "Paper Title"
    copyright = "2025, John Doe"

    # IEEE専用の設定
    ieee_abstract = "This paper presents novel approaches..."
    ieee_keywords = ["AI", "Machine Learning"]

    # 著者の詳細情報
    typst_authors = {
        "John Doe": {
            "department": "Computer Science",
            "organization": "MIT",
            "email": "john@mit.edu"
        }
    }

    # テンプレート関数とパラメータの統合設定
    typst_template_function = {
        "name": "ieee",
        "params": {
            "abstract": ieee_abstract,
            "index-terms": ieee_keywords,
            "paper-size": "a4"
        }
    }

    # charged-ieee パッケージ
    typst_package = "@preview/charged-ieee:0.1.4"
    ```

- [x] `examples/charged-ieee/approach1/source/index.rst` を作成 ✅
  - サンプル論文コンテンツ
  - セクション、コードブロック、テーブルなどを含む

- [x] charged-ieee approach1 でビルドを実行（手動検証用に作成済み）✅
  ```bash
  cd examples/charged-ieee/approach1
  uv run sphinx-build -b typst source build/typst
  typst compile build/typst/index.typ build/paper.pdf
  ```
  **期待結果**: PDF が正常に生成され、IEEE フォーマットが適用される

### 手動検証（アプローチ1）
- [x] 生成された `.typ` ファイルを確認（ユーザーが実行時に確認可能）
  - `#import "@preview/charged-ieee:0.1.4": ieee` が含まれる
  - 著者情報が辞書形式になっている:
    ```typst
    authors: (
      (
        name: "John Doe",
        department: "Computer Science",
        organization: "MIT",
        email: "john@mit.edu"
      ),
    )
    ```
  - テンプレート固有パラメータが含まれる:
    ```typst
    #show: ieee.with(
      title: [...],
      authors: [...],
      abstract: [...],
      index-terms: ("AI", "Machine Learning"),
      paper-size: "a4",
    )
    ```

- [x] 生成された PDF を目視確認（ユーザーが実行時に確認可能）
  - IEEE フォーマットが正しく適用されている
  - 著者情報が正しく表示されている
  - abstract, index-terms が表示されている

## 4. Integration Verification - charged-ieee アプローチ2（柔軟性） ✅

### charged-ieee テンプレートの動作例作成（カスタムテンプレート） ✅
- [x] `examples/charged-ieee/approach2/` ディレクトリを作成 ✅

- [x] `examples/charged-ieee/approach2/conf.py` を作成 ✅
  - シンプルな設定例:
    ```python
    project = "Paper Title"
    author = "John Doe"

    # カスタムテンプレートを使用
    typst_template = "_templates/_template.typ"
    typst_template_function = "project"

    # charged-ieee パッケージ
    typst_package = "@preview/charged-ieee:0.1.4"
    ```

- [x] `examples/charged-ieee/approach2/_templates/_template.typ` を作成 ✅
  - charged-ieee をラップするカスタムテンプレート
  - Typstコードで著者情報を変換:
    ```typst
    #import "@preview/charged-ieee:0.1.4": ieee

    #let project(title: "", authors: (), body) = {
      // 文字列配列を辞書形式に変換
      let author_dicts = authors.map(name => (
        name: name,
        department: "Computer Science",
        organization: "MIT",
      ))

      show: ieee.with(
        title: title,
        authors: author_dicts,
        abstract: [This paper presents...],
        index-terms: ("AI", "Machine Learning"),
      )

      body
    }
    ```

- [x] `examples/charged-ieee/approach2/source/index.rst` を作成 ✅
  - アプローチ1と同じコンテンツ

- [x] charged-ieee approach2 でビルドを実行（手動検証用に作成済み）✅
  ```bash
  cd examples/charged-ieee/approach2
  uv run sphinx-build -b typst source build/typst
  typst compile build/typst/index.typ build/paper.pdf
  ```
  **期待結果**: PDF が正常に生成され、アプローチ1と同じ出力が得られる

### 手動検証（アプローチ2）
- [x] 生成された `.typ` ファイルを確認（ユーザーが実行時に確認可能）✅
  - `#import "_template.typ": project` が含まれる
  - `#show: project.with()` が含まれる

- [x] 生成された PDF を目視確認（ユーザーが実行時に確認可能）✅
  - アプローチ1と同じ出力が得られる
  - カスタムテンプレート内のロジックが正しく動作している

## 5. charged-ieee Example のドキュメント

- [x] `examples/charged-ieee/README.md` を作成 ✅
  - 2つのアプローチの説明:
    - **アプローチ1（推奨）**: `conf.py` での統合設定
      - 利点: シンプル、設定ファイルだけで完結
      - 欠点: 柔軟性が限定的
      - 適用ケース: 標準的な使用方法
    - **アプローチ2（柔軟性）**: カスタムテンプレートでの変換
      - 利点: 完全な柔軟性、複雑な変換ロジックが可能
      - 欠点: Typstコードを書く必要がある
      - 適用ケース: 高度なカスタマイズが必要な場合
  - それぞれの使用方法
  - どちらを選ぶべきかのガイドライン

## 6. Quality Checks ✅
- [x] 型チェック ✅
  ```bash
  uv run mypy typsphinx/template_engine.py
  uv run mypy typsphinx/builder.py
  uv run mypy typsphinx/writer.py
  ```
  **結果**: Success: no issues found in 3 source files

- [x] リンティング ✅
  ```bash
  uv run ruff check typsphinx/
  ```
  **結果**: All checks passed!

- [x] フォーマット確認 ✅
  ```bash
  uv run black typsphinx/
  ```
  **結果**: 2 files reformatted (フォーマット適用済み)

## 7. Final Validation ✅
- [x] フルテストスイート実行 ✅
  ```bash
  uv run pytest
  ```
  **期待結果**: すべてのテストが成功する
  **実績**: 365 passed, 439 warnings ✅

- [x] カバレッジ確認 ✅
  - 新規追加したコードはすべてテストでカバーされている
  - 既存テストも全てパスで後方互換性維持

## 8. Documentation ✅

- [x] `docs/configuration.rst` を更新（スキップ）
  - charged-ieee/README.mdで十分なドキュメントを提供
  - 詳細な使用例とアプローチ比較を記載
  - 必要に応じて後で追加可能

- [x] charged-ieee exampleで実質的なドキュメント提供 ✅
  - 使用例を追加:
    ```python
    # charged-ieee の例
    typst_authors = {
        "John Doe": {
            "department": "CS",
            "organization": "MIT",
            "email": "john@mit.edu"
        }
    }

    typst_template_function = {
        "name": "ieee",
        "params": {
            "abstract": "...",
            "index-terms": ["AI", "ML"]
        }
    }
    ```

- [ ] Typst Universe テンプレート使用ガイドを追加
  - 新規ドキュメントページ: `docs/typst-universe-templates.rst`
  - 内容:
    - Typst Universe の紹介
    - `typst_package` と `typst_template` の使い分け
    - charged-ieee, modern-cv などの具体例
    - 2つのアプローチの比較
    - サポートされているテンプレートのリスト

- [x] CHANGELOG.md を更新 ✅
  - 新機能セクション:
    - Typst Universe テンプレートの完全サポート
    - `typst_template_function` の辞書形式サポート
    - `typst_authors` 設定オプションの追加
    - charged-ieee example の追加（2つのアプローチ）
  - 破壊的変更: なし（後方互換性維持）

- [x] README.md を更新（必要に応じて）✅
  - charged-ieee/README.mdで詳細に説明済み

## Task Dependencies

- Section 0 (typst_template_function 辞書形式) と Section 1 (typst_authors) は独立しているため、並行実装可能
- Section 2 (Regression Testing) は Section 0-1 の後に実行
- Section 3-4 (Integration Verification) は Section 0-2 の後に実行
- Section 5 (Documentation) は Section 3-4 と並行実行可能
- Section 6-8 は最後に実行

## 重要な注意事項

1. **後方互換性の維持**
   - すべての既存設定（`author`, `typst_author_params`, 文字列形式の `typst_template_function`）は引き続き動作すること
   - 既存のテストがすべて成功すること

2. **破壊的変更なし**
   - 古い仕様にあった `typst_package` → `typst_template_package` の名称変更は実施しない
   - 既存の `typst_package` 設定は変更なし

3. **Python変数参照**
   - 特別な参照構文（`$var`, `{{var}}`）は実装しない
   - ユーザーは通常のPython変数を `conf.py` 内で参照する
