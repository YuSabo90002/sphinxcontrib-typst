# タスク: テーブル重複修正の実装

## 実装タスク

### 1. コア修正: add_text()メソッドの変更

- [ ] `sphinxcontrib/typst/translator.py:59`の`add_text()`メソッドを修正
  - テーブルセル内かどうかをチェックする条件分岐を追加
  - `in_table`フラグと`table_cell_content`属性の存在を確認
  - テーブルセル内の場合は`table_cell_content`に追加
  - テーブル外の場合は従来通り`self.body`に追加

**検証:**
```bash
# 変更後、該当メソッドを確認
cat -n sphinxcontrib/typst/translator.py | sed -n '59,66p'
```

### 2. 既存テストの実行とリグレッション確認

- [ ] 全テストを実行してリグレッションがないことを確認
  ```bash
  uv run pytest tests/test_translator.py -v
  uv run pytest tests/test_integration_advanced.py -v
  ```

**期待結果:** すべてのテストがパス

### 3. フィクスチャを使った動作確認

- [ ] `examples/advanced`のビルドを実行
  ```bash
  cd examples/advanced
  sphinx-build -b typst . _build/typst
  ```

- [ ] 生成された`_build/typst/chapter2.typ`を確認
  - 21-85行目付近のテーブル出力を確認
  - プレーンテキストの重複がないことを確認
  - `#table()`構造のみが存在することを確認

**検証コマンド:**
```bash
# テーブル部分を表示
sed -n '15,95p' examples/advanced/_build/typst/chapter2.typ
```

### 4. 新規テストケースの追加

- [ ] `tests/test_translator.py`に**すべてのテーブル形式**の非重複検証テストを追加
  - テストケース名: `test_table_no_duplication_all_types`
  - 以下のテーブル形式すべてをテスト:
    - list-table ディレクティブ
    - grid table (罫線形式)
    - simple table
    - csv-table ディレクティブ
  - 各形式で出力に`#table()`が1回だけ含まれることを確認
  - セル内容のプレーンテキストが`#table()`の前に出現しないことを確認

**テストの骨格:**
```python
def test_table_no_duplication_all_types(simple_document, mock_builder):
    """Verify table content is not duplicated for all table types."""
    from sphinxcontrib.typst.translator import TypstTranslator
    from docutils.parsers.rst import Parser
    from docutils.utils import new_document

    table_types = {
        'list-table': '.. list-table::\n   :header-rows: 1\n\n   * - H1\n     - H2\n   * - A\n     - B',
        'grid': '+---+---+\n| H1| H2|\n+===+===+\n| A | B |\n+---+---+',
        'simple': '==  ==\nH1  H2\n==  ==\nA   B\n==  ==',
        'csv': '.. csv-table::\n   :header: "H1", "H2"\n\n   "A", "B"'
    }

    for table_type, rst_content in table_types.items():
        # Parse RST and process
        # Assert no duplication for each type
```

- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_table_no_duplication_all_types -v
  ```

### 5. 型チェックとリンティング

- [ ] 型チェックを実行
  ```bash
  uv run mypy sphinxcontrib/typst/translator.py
  ```

- [ ] リンティングを実行
  ```bash
  uv run ruff check sphinxcontrib/typst/translator.py
  uv run black --check sphinxcontrib/typst/translator.py
  ```

**期待結果:** エラーなし

### 6. 最終検証

- [ ] 全テストスイートを実行
  ```bash
  uv run pytest
  ```

- [ ] カバレッジを確認
  ```bash
  uv run pytest --cov=sphinxcontrib.typst --cov-report=term-missing
  ```

**期待結果:**
- 全テストパス (317+ tests)
- カバレッジ 90%以上維持

### 7. ドキュメント更新

- [ ] CHANGELOG.mdに修正内容を追加
  - セクション: `## [Unreleased]` または次のバージョン
  - カテゴリ: `### Fixed`
  - 内容: 「テーブル内容の重複出力を修正 (#19)」

## 依存関係

- タスク1は独立して実行可能
- タスク2-3はタスク1の完了後
- タスク4はタスク2-3と並行可能
- タスク5はタスク1の完了後、いつでも実行可能
- タスク6はすべての実装タスク完了後
- タスク7は最後に実行

## 並列実行可能なタスク

- タスク4 (新規テスト追加) とタスク3 (フィクスチャ確認) は並行実行可能
- タスク5 (型チェック・リント) はタスク2-4と並行実行可能
