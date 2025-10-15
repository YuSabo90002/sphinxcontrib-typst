# Implementation Gap Analysis

## 分析概要

### 機能スコープと複雑性
**機能**: toctree 翻訳処理の簡略化 - 複数 `#include()` の単一コンテンツブロック化

**複雑性**: Small (S)
**理由**: 既存の `visit_toctree()` メソッドの制御フローを変更するのみ。新規ファイルやモジュールの追加は不要。

### 主要な技術的課題
1. **最小限の変更**: ループ構造を変更せずにコンテンツブロックの生成位置を調整する
2. **後方互換性**: 既存のすべてのテスト (313 tests) を成功させる
3. **機能的等価性**: 生成される PDF 出力が既存実装と完全に同一であることを保証

### 総合的な実装アプローチ推奨
**推奨アプローチ**: 既存ファイル拡張 (Extension)

**理由**:
- 変更範囲が `sphinxcontrib/typst/translator.py` の `visit_toctree()` メソッド内の15行程度に限定される
- 新規ファイルやモジュールの作成は不要
- 既存のテストフレームワークとフィクスチャをそのまま利用可能

---

## 既存コードベースの洞察

### 関連する既存コンポーネントと責務

#### 1. `sphinxcontrib/typst/translator.py`
**クラス**: `TypstTranslator`
**メソッド**: `visit_toctree(self, node: nodes.Node)`
**現在の責務**:
- toctree ノードから entries を抽出
- 各 entry に対してループ処理
- 相対パスの計算 (`_compute_relative_include_path()` 呼び出し)
- **各 entry ごとに個別のコンテンツブロック `#[...]` を生成**
- 各ブロック内に `#set heading(offset: 1)` と `#include()` を配置

**現在の実装構造** (lines 998-1015):
```python
for _title, docname in entries:
    # Compute relative path for #include() (Issue #5 fix)
    relative_path = self._compute_relative_include_path(
        docname, current_docname
    )

    logger.debug(...)

    # Requirement 13.14: Use content block #[...] for heading offset
    self.add_text("#[\n")
    self.add_text("  #set heading(offset: 1)\n")
    self.add_text(f'  #include("{relative_path}.typ")\n')
    self.add_text("]\n\n")
```

**依存メソッド**:
- `_compute_relative_include_path(target_docname, current_docname)` - Issue #5 で実装された相対パス計算
- `add_text(text)` - 継承元の NodeVisitor クラスのメソッド

#### 2. テストファイル
**関連テストファイル**:
- `tests/test_toctree_requirement13.py` - toctree の基本機能テスト
- `tests/test_nested_toctree_paths.py` - 相対パス計算のユニットテスト (Issue #5)
- `tests/test_integration_nested_toctree.py` - ネストされた toctree の統合テスト (Issue #5)
- `tests/test_config_toctree_defaults.py` - toctree 設定オプションのテスト

**既存テストパターン**:
```python
def test_toctree_with_heading_offset(simple_document, mock_builder):
    translator = TypstTranslator(simple_document, mock_builder)

    toctree = addnodes.toctree()
    toctree["entries"] = [("Chapter 1", "chapter1")]

    try:
        translator.visit_toctree(toctree)
    except nodes.SkipNode:
        pass

    output = translator.astext()

    # Assertions on generated Typst code
    assert "#set heading(offset: 1)" in output
    assert '#include("chapter1.typ")' in output
```

### 確立されたパターンと規約

#### コーディング規約
- **Line Length**: 88 文字 (Black デフォルト)
- **Indentation**: スペース 4 個
- **Quotes**: ダブルクォート優先
- **Import Order**: PEP 8 準拠 (標準 → サードパーティ → ローカル)
- **Type Hints**: Python 3.9+ 記法 (`Optional[str]` 形式)

#### テスト規約
- **テストファイル名**: `test_*.py`
- **テストクラス名**: `Test*`
- **テスト関数名**: `test_*`
- **フィクスチャ**: `conftest.py` で共有、または各テストファイル内で定義
- **Assertion パターン**: 生成された Typst コードの文字列マッチング

#### ログ記録パターン
```python
from sphinx.util import logging
logger = logging.getLogger(__name__)

logger.debug(f"Processing toctree with {len(entries)} entries")
```

### 再利用可能なユーティリティとサービス

#### 既存の再利用可能コンポーネント
1. **`_compute_relative_include_path()`** - Issue #5 で実装
   - 相対パス計算ロジック
   - 今回の変更では**変更不要**、そのまま利用可能

2. **`add_text()` メソッド**
   - NodeVisitor から継承
   - 今回の変更でも継続使用

3. **テストフィクスチャ**
   - `simple_document` - 基本的なドキュメントノード
   - `mock_builder` - ビルダーのモック
   - 既存テストスイート内で定義済み

---

## 実装戦略オプション

### Option A: 既存メソッドの拡張（推奨）

**アプローチ**: `visit_toctree()` メソッドのループ構造を変更

**実装詳細**:
```python
def visit_toctree(self, node: nodes.Node) -> None:
    # ... 既存の前処理（entries 取得、空チェック）...

    # 【変更点1】単一の開始ブロックを生成
    self.add_text("#[\n")
    self.add_text("  #set heading(offset: 1)\n")

    # 【変更点2】ループ内ではincludeのみ生成
    for _title, docname in entries:
        relative_path = self._compute_relative_include_path(
            docname, current_docname
        )
        logger.debug(...)
        self.add_text(f'  #include("{relative_path}.typ")\n')

    # 【変更点3】単一の終了ブロックを生成
    self.add_text("]\n\n")

    raise nodes.SkipNode
```

**変更範囲**:
- **ファイル**: `sphinxcontrib/typst/translator.py`
- **メソッド**: `visit_toctree()` (lines 962-1018)
- **変更行数**: 約 10-15 行

**根拠**:
- 最小限の変更で要件を満たす
- 既存の相対パス計算ロジックを再利用
- テストケースの大部分は変更不要（Typst コード生成の検証のみ更新）

**トレードオフ**:
- ✅ **Pro**: 最小限の変更、低リスク
- ✅ **Pro**: 既存のテストインフラストラクチャをそのまま利用
- ✅ **Pro**: レビューが容易
- ⚠️ **Con**: なし（このケースでは明確なデメリットなし）

**複雑性**: **Small (S)** - 1-2日
- 実装: 30分-1時間
- テスト更新: 1-2時間
- 統合テスト・E2Eテスト: 2-3時間
- コード品質チェック (lint/format/type): 30分
- tox による多バージョンテスト: 1-2時間

---

### Option B: 新規メソッド作成（非推奨）

**アプローチ**: `_generate_toctree_includes()` のような補助メソッドを作成

**実装詳細**:
```python
def _generate_toctree_includes(self, entries, current_docname):
    """Generate single content block with multiple includes."""
    self.add_text("#[\n")
    self.add_text("  #set heading(offset: 1)\n")
    for _title, docname in entries:
        relative_path = self._compute_relative_include_path(
            docname, current_docname
        )
        self.add_text(f'  #include("{relative_path}.typ")\n')
    self.add_text("]\n\n")

def visit_toctree(self, node: nodes.Node) -> None:
    # ... 前処理 ...
    self._generate_toctree_includes(entries, current_docname)
    raise nodes.SkipNode
```

**根拠**:
- コードの責務分離
- ユニットテストの独立性

**トレードオフ**:
- ⚠️ **Con**: 過度な抽象化（単純なループに対して）
- ⚠️ **Con**: テストケースの追加が必要
- ⚠️ **Con**: コード行数の増加

**複雑性**: **Small-Medium (S-M)** - 2-3日

**推奨しない理由**: このケースでは過度な設計。Option A で十分。

---

### Option C: ハイブリッドアプローチ（不要）

このケースでは該当なし。変更範囲が限定的であり、ハイブリッドアプローチは不要。

---

## 技術的リサーチ要件

### 外部依存関係の分析
**結論**: 新規外部依存なし

**既存依存関係のみ使用**:
- `docutils` - ノード処理
- `sphinx` - ビルダーとロガー
- `pytest` - テスト

### 知識ギャップの評価
**結論**: チームに既知の技術のみ

**必要な知識**:
1. ✅ Typst のコンテンツブロック `#[...]` の動作 - 既に実装で使用中
2. ✅ Sphinx の NodeVisitor パターン - 既存実装で確立
3. ✅ toctree の相対パス計算 - Issue #5 で実装済み

**リサーチ不要**: すべての技術要素が既知

### パフォーマンス・セキュリティ考慮事項

#### パフォーマンス
**影響**: なし（むしろ微小な改善）

**理由**:
- `add_text()` 呼び出し回数が削減される（N×4回 → 2+N回）
- 例: 3つの entry の場合
  - 既存: 12 回の `add_text()` 呼び出し
  - 新規: 5 回の `add_text()` 呼び出し

#### セキュリティ
**影響**: なし

**理由**:
- 入力検証ロジックは変更なし
- パス計算ロジックは変更なし（Issue #5 の実装を再利用）
- 出力形式の変更のみ

---

## 設計フェーズへの推奨事項

### 推奨実装アプローチ
**Option A: 既存メソッドの拡張**を強く推奨

**理由**:
1. 最小限の変更で要件を完全に満たす
2. リスクが低く、レビューが容易
3. 既存のテストインフラを最大限活用
4. 1-2日で完了可能

### 主要なアーキテクチャ決定事項

#### 決定1: コンテンツブロックの生成位置
**決定**: ループの外側（開始前と終了後）

**理由**:
- 要件通り、単一ブロックで全 include を囲む
- 既存のループ構造を最大限維持

#### 決定2: ログ記録の配置
**決定**: 各 include 生成時にログを記録（既存と同じ）

**理由**:
- デバッグ時の可読性維持
- 既存のログパターンとの一貫性

#### 決定3: テスト戦略
**決定**: 既存テストを更新 + 新規テストケース追加

**更新が必要なテスト**:
- `test_toctree_with_heading_offset()` - 複数 include の場合を追加
- `test_toctree_generates_include_directives()` - Assertion を更新

**新規テストケース**:
- 単一コンテンツブロック内に複数 include が存在することを検証
- `#set heading(offset: 1)` が1回のみ出現することを検証
- 生成行数が削減されることを検証

### 設計フェーズで更なる調査が必要な領域

#### 調査事項1: 空の toctree の処理
**現状**: `if not entries: raise nodes.SkipNode`

**確認事項**: 新実装でも同じ動作を維持（変更なし）

**優先度**: Low（既存動作の確認のみ）

#### 調査事項2: toctree オプション (maxdepth, numbered, caption) の影響
**現状**: `visit_toctree()` 内では処理なし（テンプレートエンジンで処理）

**確認事項**: 新実装が既存オプション処理に影響しないことを確認

**優先度**: Medium（後方互換性の保証）

**検証方法**: `tests/test_config_toctree_defaults.py` のテストが全て成功することを確認

### 設計フェーズで対処すべき潜在的リスク

#### リスク1: 既存テストの失敗
**リスクレベル**: Low

**対策**:
- テストケースを段階的に更新
- 各更新後に全テストスイートを実行
- カバレッジツールで変更箇所のテストを確認

#### リスク2: Typst コンパイルエラー
**リスクレベル**: Very Low

**対策**:
- E2E テストで PDF 生成を検証
- Issue #7 の Example に記載された Typst コードで手動検証済み

#### リスク3: パフォーマンス劣化
**リスクレベル**: None

**理由**: `add_text()` 呼び出し回数が削減されるため、むしろ改善

---

## 実装複雑性の最終評価

### 工数見積もり
**総合評価**: **Small (S)** - 1-2日

**詳細内訳**:
| タスク | 所要時間 |
|--------|----------|
| `visit_toctree()` メソッドの変更 | 30分-1時間 |
| 既存テストケースの更新 | 1-2時間 |
| 新規テストケースの追加 | 1-2時間 |
| lint/format/type チェックの実行と修正 | 30分 |
| 統合テスト・E2Eテストの実行 | 2-3時間 |
| tox による多バージョンテスト | 1-2時間 |
| コードレビューと修正 | 1-2時間 |
| **合計** | **1-2日** |

### リスクファクター
**総合リスク**: **Low（低）**

**リスク要因**:
- ✅ 既知の技術のみ使用
- ✅ 変更範囲が限定的（1メソッド、約15行）
- ✅ 既存の相対パス計算ロジックを再利用
- ✅ 包括的なテストスイート (313 tests) が存在
- ✅ CI/CD による自動品質チェック

**緩和策**:
- 段階的な実装とテスト
- 各変更後の全テストスイート実行
- E2E テストによる PDF 出力検証

---

## まとめ

### 推奨実装アプローチ
**Option A: 既存メソッドの拡張** - `sphinxcontrib/typst/translator.py` の `visit_toctree()` メソッドを直接変更

### 主要な成功要因
1. ✅ 変更範囲が明確で限定的
2. ✅ 既存の高品質なテストスイート
3. ✅ Issue #5 で実装済みの相対パス計算を再利用
4. ✅ すべての技術要素が既知

### 設計フェーズでの注意点
1. 既存テストケースの Assertion を単一コンテンツブロック用に更新
2. 後方互換性の検証（すべての既存テスト成功を確認）
3. コード品質チェック（ruff, black, mypy）の完全合格
4. tox による複数 Python バージョンでのテスト成功

**次のステップ**: `/kiro:spec-design simplify-toctree-content-block` で詳細設計を生成
