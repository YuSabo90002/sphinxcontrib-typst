# タスク: RSTコメント処理の追加

## 実装タスク

### 1. RSTコメント処理 - TDDサイクル

#### Phase 1: RED (Failingテストの作成)

- [x] RSTコメントスキップのテストを作成
  - テスト名: `test_comment_skipped`
  - テストファイル: `tests/test_translator.py`
  - 単一行コメント、複数行コメント、前後のテキスト分離を検証
  - 初期状態では失敗することが期待される

#### Phase 2: Confirm RED

- [x] テストを実行して失敗を確認
  ```bash
  uv run pytest tests/test_translator.py::test_comment_skipped -xvs
  ```
  **Expected:** テストが失敗（コメントが出力に含まれている）

#### Phase 3: GREEN (実装)

- [x] `visit_comment()`メソッドを実装
  - ファイル: `sphinxcontrib/typst/translator.py`
  - 変更: `raise nodes.SkipNode`でコメントをスキップ
- [x] `depart_comment()`メソッドを実装
  - ファイル: `sphinxcontrib/typst/translator.py`
  - 変更: パススルー実装

#### Phase 4: Confirm GREEN

- [x] テストを実行してパスを確認
  ```bash
  uv run pytest tests/test_translator.py::test_comment_skipped -xvs
  ```
  **Expected:** テストがパス

#### Phase 5: REFACTOR (Optional)

- [x] コードのrefactorが必要か確認
- [x] 必要であればrefactor実施
- [x] refactor後もテストがパスすることを確認

### 2. リグレッションテスト

- [x] 既存テストスイートを実行
  ```bash
  uv run pytest tests/test_translator.py -v
  ```
  **Expected:** 既存テストが全てパス（48テスト）

- [x] 全テストスイートを実行
  ```bash
  uv run pytest
  ```
  **Expected:** 全319テスト（318+1）がパス

### 3. 統合検証

- [x] 実際のRSTファイルでテスト
  - サンプルRSTファイルを作成（コメントを含む）
  - `sphinx-build -b typst`で変換
  - 生成された`.typ`ファイルにコメントが含まれないことを確認

- [x] 警告メッセージの確認
  - `WARNING: unknown node type: <comment>`が表示されないことを確認

### 4. 品質チェック

- [x] コードフォーマット
  ```bash
  uv run black sphinxcontrib/typst/translator.py tests/test_translator.py
  ```

- [x] リンター実行
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py tests/test_translator.py
  ```

- [x] 型チェック
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```

### 5. ドキュメント更新

- [x] CHANGELOG.mdに変更を記録
  - セクション: `### Fixed`
  - 内容: RSTコメントが正しくスキップされるようになった旨を記載
  - 関連issue #21へのリンク

## 完了基準

- ✅ 新規テスト`test_comment_skipped`が追加され、パスする
- ✅ 既存テスト全318テストがパスする
- ✅ コードフォーマット、リンター、型チェックが全てパスする
- ✅ 実際のRSTファイルでコメントがスキップされることを確認
- ✅ 警告メッセージが表示されない
- ✅ CHANGELOG.mdが更新されている
