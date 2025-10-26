# タスク: ストリームベースリストレンダリングの実装

## 実装タスク

### Phase 1: Bullet ListとEnumerated Listのストリーム化

#### 1. 状態フラグの追加

- [x] `typsphinx/translator.py`の`__init__`メソッドに新しいフラグを追加
  ```python
  self.is_first_list_item = True
  self.list_item_needs_separator = False
  ```

**検証:**
```bash
rg "self.is_first_list_item|self.list_item_needs_separator" typsphinx/translator.py
```

#### 2. visit_bullet_listの修正

- [x] `visit_bullet_list()`メソッドを修正
  - `self.list_items_stack.append(("bullet", []))`を削除
  - 代わりに`self.add_text("list(")`を追加
  - `self.is_first_list_item = True`を設定
  - ネスト対応のため状態保存/復元ロジックも追加

**修正前:**
```python
def visit_bullet_list(self, node: nodes.bullet_list) -> None:
    self.list_stack.append("bullet")
    self.list_items_stack.append(("bullet", []))
```

**修正後:**
```python
def visit_bullet_list(self, node: nodes.bullet_list) -> None:
    self.list_stack.append("bullet")
    self.add_text("list(")
    self.is_first_list_item = True
```

#### 3. depart_bullet_listの修正

- [x] `depart_bullet_list()`メソッドを修正
  - `list_items_stack.pop()`とitem収集ロジックを削除
  - 代わりに`self.add_text(")")`を追加
  - トップレベルリストのみ改行追加
  - ネスト対応のため状態復元ロジックも追加

**修正前:**
```python
def depart_bullet_list(self, node: nodes.bullet_list) -> None:
    self.list_stack.pop()
    list_type, items = self.list_items_stack.pop()
    if items:
        items_str = ", ".join(items)
        self.add_text(f"list({items_str})\n\n")
    else:
        self.add_text("list()\n\n")
```

**修正後:**
```python
def depart_bullet_list(self, node: nodes.bullet_list) -> None:
    self.list_stack.pop()
    self.add_text(")\n\n")
```

#### 4. visit_list_itemの修正

- [x] `visit_list_item()`メソッドを修正
  - ボディ置き換えロジックを削除
  - カンマ追加ロジックを追加
  - `list_item_needs_separator`フラグをリセット

**修正前:**
```python
def visit_list_item(self, node: nodes.list_item) -> None:
    self.in_list_item = True
    self.saved_body = self.body
    self.current_list_item_buffer = []
    self.body = self.current_list_item_buffer
```

**修正後:**
```python
def visit_list_item(self, node: nodes.list_item) -> None:
    self.in_list_item = True
    if not self.is_first_list_item:
        self.add_text(", ")
    self.is_first_list_item = False
    self.list_item_needs_separator = False
```

#### 5. depart_list_itemの修正

- [x] `depart_list_item()`メソッドを修正
  - ボディ復元ロジックを削除
  - item収集ロジックを削除
  - `self.in_list_item = False`のみ残す

**修正前:**
```python
def depart_list_item(self, node: nodes.list_item) -> None:
    self.in_list_item = False
    item_content = "".join(self.current_list_item_buffer or []).strip()
    if self.saved_body is not None:
        self.body = self.saved_body
    self.saved_body = None
    self.current_list_item_buffer = None
    if self.list_items_stack:
        list_type, items = self.list_items_stack[-1]
        items.append(item_content)
        self.list_items_stack[-1] = (list_type, items)
```

**修正後:**
```python
def depart_list_item(self, node: nodes.list_item) -> None:
    self.in_list_item = False
```

#### 6. visit_enumerated_listとdepart_enumerated_listの修正

- [x] `visit_enumerated_list()`を修正（bullet listと同様）
- [x] `depart_enumerated_list()`を修正（bullet listと同様）
  - `list(`を`enum(`に変更

#### 7. 要素メソッドに+セパレータロジックを追加

- [x] リスト項目内で使用される要素の各visitメソッドを修正
  - [x] `visit_Text()`
  - [x] `visit_emphasis()` - 子要素のため状態保存/復元も実装
  - [x] `visit_strong()` - 子要素のため状態保存/復元も実装
  - [x] `visit_literal()`
  - [ ] `visit_reference()` - 未実装（必要に応じて）
  - [ ] `visit_paragraph()` - 未実装（既存ロジックで動作）
  - [x] ネストされた`visit_bullet_list()`/`visit_enumerated_list()` - 状態保存/復元実装

各メソッドの先頭に以下を追加:
```python
if self.in_list_item and self.list_item_needs_separator:
    self.add_text(" + ")
# 既存のロジック...
if self.in_list_item:
    self.list_item_needs_separator = True
```

**検証:**
```bash
# 各メソッドを確認
rg -B 2 -A 10 "def visit_Text|def visit_emphasis|def visit_strong" typsphinx/translator.py
```

### Phase 2: Definition Listsのストリーム化

**注記**: Phase 2はスキップ。Definition listsは現在のバッファ方式で正常動作しており、Issue #61修正には不要。

#### 8. visit_definitionとdepart_definitionの修正

- [ ] **SKIPPED** - Definition listsは現在のまま維持

#### 9. visit_termとdepart_termの修正

- [ ] **SKIPPED** - Definition listsは現在のまま維持

### Phase 3: クリーンアップ

#### 10. 不要なコードの削除

- [x] `__init__`から以下を削除
  ```python
  self.list_items_stack = []
  self.current_list_item_buffer = None
  self.saved_body = None  # Definition listsで使用中のため一部残存
  ```

- [x] 他に`saved_body`、`current_list_item_buffer`、`list_items_stack`を使用している箇所を確認
  - **注記**: `saved_body`はdefinition listsで引き続き使用（term/definitionメソッド）
  - `list_items_stack`と`current_list_item_buffer`は完全削除

**検証:**
```bash
# 削除すべきコードが残っていないか確認
rg "saved_body|current_list_item_buffer|list_items_stack" typsphinx/translator.py
```

#### 11. 既存テストの更新

- [x] テストが新しい出力形式に対応しているか確認
  ```bash
  uv run pytest tests/test_translator.py -v -k list
  ```
  **結果**: 全9テストパス

- [x] 必要に応じてテストのアサーションを更新
  **結果**: 更新不要（既存テストが正しく動作）

#### 12. 新規テストケースの追加

- [ ] **OPTIONAL** - `tests/test_translator.py`にストリームベースレンダリングのテストを追加
  - **注記**: 既存テスト（test_bullet_list_conversion, test_nested_bullet_listなど）が十分カバー
  - 追加テストは必須ではない

**テストの骨格:**
```python
def test_stream_based_list_rendering(mock_builder):
    """Verify stream-based list rendering preserves document wrapper."""
    from typsphinx.translator import TypstTranslator
    from docutils.parsers.rst import Parser
    from docutils.utils import new_document
    from docutils.frontend import get_default_settings

    rst_content = """
Title
=====

- Item 1
- Item 2 with **bold**

  - Nested item 1
  - Nested item 2

- Item 3
"""

    parser = Parser()
    settings = get_default_settings(Parser)
    document = new_document('<test>', settings=settings)
    parser.parse(rst_content, document)

    translator = TypstTranslator(document, mock_builder)
    document.walkabout(translator)
    output = translator.astext()

    # Verify document wrapper
    assert output.startswith('#{'), "Document should start with #{"
    assert output.endswith('}\n'), "Document should end with }\\n"

    # Verify list structure
    assert 'list(' in output
    assert 'text("Item 1"), text("Item 2 with ")' in output
    assert '+ strong(text("bold"))' in output

    # Verify nested list
    assert '+ list(text("Nested item 1"), text("Nested item 2"))' in output
```

- [ ] テストを実行して成功を確認
  ```bash
  uv run pytest tests/test_translator.py::test_stream_based_list_rendering -v
  ```

### Phase 4: 実ドキュメントでの検証

#### 13. index.rstとcontributing.rstの動作確認

- [x] ドキュメントをビルドして修正を確認
  ```bash
  uv run sphinx-build -b typst docs/source docs/_build/typst
  ```
  **結果**: ビルド成功

- [x] `_build/typst/index.typ`を確認
  - ✅ ファイルに`#{`が含まれることを確認（16行目）
  - ✅ ファイルが`}`で終わることを確認
  - ✅ リストが正しく出力されていることを確認（ストリームベース）
  - ✅ ネストされたリストも正しく動作（`list(...) + list(...)`形式）

- [x] Issue #61が修正されていることを確認
  - ✅ ドキュメントラッパー`#{...}`が失われていない

#### 14. 型チェックとリンティング

- [x] 型チェックを実行
  ```bash
  uv run mypy typsphinx/translator.py
  ```
  **結果**: 成功（`saved_body`の型アノテーション追加が必要だったため修正）

- [x] リンティングを実行
  ```bash
  uv run ruff check typsphinx/
  uv run black --check typsphinx/
  ```
  **結果**: ruff成功、blackフォーマット実行（自動修正完了）

#### 15. 最終検証

- [x] 全テストスイートを実行
  ```bash
  uv run pytest
  ```
  **結果**: 373テスト全てパス

- [ ] **TODO** - PDFビルダーでも動作確認（オプション）
  ```bash
  uv run sphinx-build -b typstpdf docs/source docs/_build/pdf
  ls -lh docs/_build/pdf/*.pdf
  ```

### Phase 5: ワークアラウンドの削除（オプション）

#### 16. writer.pyのワークアラウンド削除

- [ ] **OPTIONAL** - `typsphinx/writer.py`のワークアラウンドを削除検討
  - 現在の行75-80のワークアラウンドコード
  - **推奨**: 当面は保持（追加の安全策として）
  - 複数バージョンで安定動作確認後に削除を検討

**注意:** この変更は慎重に行う。まず修正が完全に動作することを確認してから実施する。

```python
# 削除するコード（行75-80）
# WORKAROUND: For some Sphinx documents, visit_document may not be called
# Ensure body is wrapped in code mode block
if not body.startswith("#{"):
    body = "#{\n" + body
if not body.endswith("}\n"):
    body = body + "}\n"
```

- [ ] ワークアラウンド削除後、全テストを再実行
  ```bash
  uv run pytest
  ```

- [ ] ドキュメントビルドを再実行して問題ないか確認

#### 17. ドキュメント更新

- [ ] **TODO** - Issue #61にコメントを追加
  - 修正完了の報告
  - ストリームベースアプローチの簡単な説明
  - テスト結果

- [ ] **TODO** - コミットメッセージを作成
  - タイトル例: `fix: use stream-based rendering for lists (#61)`
  - 本文に以下を含める:
    - 問題の説明（body swapping pattern）
    - 解決策（stream-based approach with state flags）
    - 変更内容の要約
    - `Fixes #61`

## 依存関係

- タスク1は独立して実行可能
- タスク2-7はタスク1の完了後に実行（順序依存）
- タスク8-9はタスク2-7と並行実行可能（definition listsは独立）
- タスク10はタスク2-9の完了後
- タスク11-12はタスク10の完了後
- タスク13-15はタスク11-12の完了後
- タスク16はタスク15の成功後のみ実施
- タスク17は最後に実行

## 並列実行可能なタスク

- タスク8-9 (definition lists) とタスク2-7 (bullet/enum lists) は並行実行可能
- タスク11 (既存テスト更新) とタスク12 (新規テスト追加) は並行実行可能
- タスク14 (型チェック・リント) はタスク10の完了後、いつでも実行可能

## ロールバック計画

修正に問題があった場合:
1. すべての変更を元に戻す
2. body swapping方式に戻す
3. writer.pyのワークアラウンドを維持
4. Issue #61を再オープンして別のアプローチを検討

## 注意事項

- **Phase 1（bullet/enum lists）を完全に動作させてからPhase 2（definition lists）に進む**
- 各phaseで必ずテストを実行して動作確認する
- writer.pyのワークアラウンド削除は最後に、慎重に実施する
