# Project Structure

## Root Directory Organization

```
sphinx-typst/
├── .kiro/                      # Kiro spec-driven development
│   ├── steering/               # プロジェクト全体のガイドライン
│   └── specs/                  # 機能ごとの仕様書
├── .claude/                    # Claude Code コマンド
│   └── commands/               # カスタムスラッシュコマンド
├── sphinxcontrib/              # メインパッケージ
│   └── typst/                  # Typst ビルダー実装
├── tests/                      # テストスイート
├── docs/                       # プロジェクトドキュメント
├── examples/                   # サンプルプロジェクト
├── pyproject.toml              # プロジェクト設定
├── README.md                   # プロジェクト概要
├── CLAUDE.md                   # Claude Code 設定
├── LICENSE                     # ライセンス
└── CHANGELOG.md                # 変更履歴
```

### Key Directories

#### `sphinxcontrib/typst/` - Core Package
Sphinx 拡張の主要実装ディレクトリ

```
sphinxcontrib/typst/
├── __init__.py                 # 拡張エントリーポイント
├── builder.py                  # Typst ビルダー実装
├── writer.py                   # Typst ライター (doctree → typst)
├── translator.py               # Node visitor / Typst変換ロジック
├── templates/                  # デフォルト Typst テンプレート
│   ├── base.typ                # 基本テンプレート
│   └── components/             # 再利用可能コンポーネント
├── transforms/                 # Doctree 変換処理
├── utils/                      # ユーティリティ関数
└── config.py                   # 設定ハンドラ
```

#### `tests/` - Test Suite
テストコードの配置

```
tests/
├── conftest.py                 # pytest 設定とフィクスチャ
├── test_builder.py             # ビルダーのテスト
├── test_writer.py              # ライターのテスト
├── test_translator.py          # トランスレータのテスト
├── test_integration.py         # 統合テスト
├── fixtures/                   # テスト用フィクスチャ
│   ├── sample_docs/            # サンプルドキュメント
│   └── expected_output/        # 期待される出力
└── utils/                      # テスト用ヘルパー
```

#### `docs/` - Documentation
プロジェクト自身のドキュメント (Sphinx + sphinx-typst で生成)

```
docs/
├── conf.py                     # Sphinx 設定
├── index.rst                   # ドキュメントルート
├── installation.rst            # インストールガイド
├── usage.rst                   # 使用方法
├── configuration.rst           # 設定オプション
├── api/                        # API リファレンス
├── examples/                   # 使用例
└── development.rst             # 開発者ガイド
```

#### `examples/` - Example Projects
実際の使用例を示すサンプルプロジェクト

```
examples/
├── basic/                      # 基本的な使用例
│   ├── conf.py
│   └── index.rst
├── advanced/                   # 高度な使用例
│   ├── conf.py
│   ├── index.rst
│   └── custom_template.typ
└── api_docs/                   # API ドキュメント例
    └── ...
```

## Code Organization Patterns

### Sphinx Extension Pattern

Sphinx 拡張の標準パターンに従います：

```python
# sphinxcontrib/typst/__init__.py
from typing import Any, Dict
from sphinx.application import Sphinx

def setup(app: Sphinx) -> Dict[str, Any]:
    """Sphinx 拡張エントリーポイント"""
    app.add_builder(TypstBuilder)
    app.add_config_value('typst_documents', default_value, 'html')

    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

### Builder Pattern

```python
# sphinxcontrib/typst/builder.py
from sphinx.builders import Builder

class TypstBuilder(Builder):
    name = 'typst'
    format = 'typst'
    out_suffix = '.typ'

    def init(self) -> None:
        """ビルダー初期化"""
        pass

    def get_outdated_docs(self) -> Iterator[str]:
        """更新が必要なドキュメントを特定"""
        pass

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """ドキュメント書き込み"""
        pass
```

### Visitor Pattern for Node Translation

```python
# sphinxcontrib/typst/translator.py
from docutils import nodes
from sphinx.writers import Writer

class TypstTranslator(nodes.NodeVisitor):
    """Doctree ノードを Typst に変換"""

    def visit_section(self, node: nodes.section) -> None:
        """セクション開始時の処理"""
        pass

    def depart_section(self, node: nodes.section) -> None:
        """セクション終了時の処理"""
        pass
```

## File Naming Conventions

### Python Modules

- **モジュール名**: `snake_case` (例: `builder.py`, `translator.py`)
- **クラス名**: `PascalCase` (例: `TypstBuilder`, `TypstWriter`)
- **関数名**: `snake_case` (例: `convert_doctree`, `render_template`)
- **定数**: `UPPER_SNAKE_CASE` (例: `DEFAULT_TEMPLATE`, `TYPST_VERSION`)

### Test Files

- **テストモジュール**: `test_*.py` (例: `test_builder.py`)
- **テストクラス**: `Test*` (例: `TestTypstBuilder`)
- **テスト関数**: `test_*` (例: `test_build_document`)

### Documentation

- **reStructuredText**: `.rst` 拡張子
- **Markdown**: `.md` 拡張子 (プロジェクトルートのみ)
- **Typst**: `.typ` 拡張子

## Import Organization

### Import Order (PEP 8 準拠)

```python
# 1. 標準ライブラリ
import os
import sys
from typing import Any, Dict, List

# 2. サードパーティライブラリ
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders import Builder

# 3. ローカルモジュール
from sphinxcontrib.typst import utils
from sphinxcontrib.typst.config import TypstConfig
```

### Absolute vs Relative Imports

- **外部からのインポート**: 常に絶対インポート
  ```python
  from sphinxcontrib.typst.builder import TypstBuilder
  ```

- **パッケージ内部**: 相対インポートも許可 (同一ディレクトリ内)
  ```python
  from .utils import escape_typst
  from .config import DEFAULT_CONFIG
  ```

## Key Architectural Principles

### 1. Separation of Concerns

- **Builder**: ビルドプロセス管理、ファイル I/O
- **Writer**: Doctree から Typst マークアップへの変換オーケストレーション
- **Translator**: 個別ノードタイプの Typst 変換ロジック
- **Templates**: 出力ドキュメントの構造とスタイル

### 2. Extensibility

- **カスタムノードサポート**: 拡張ノードタイプの変換フック
- **テンプレートオーバーライド**: ユーザーカスタムテンプレートの読み込み
- **設定可能性**: `conf.py` での詳細な動作制御

### 3. Sphinx Compatibility

- Sphinx の標準 API を使用
- Sphinx のイベントフックを活用
- 他の Sphinx 拡張との互換性を維持

### 4. Type Safety

- 型ヒントの活用 (Python 3.9+ 記法)
- mypy による静的型チェック
- docutils/Sphinx の型定義活用

```python
from typing import Any, Dict, List, Optional
from sphinx.application import Sphinx
from docutils.nodes import Node

def process_node(
    node: Node,
    config: Dict[str, Any],
    context: Optional[Dict[str, str]] = None
) -> str:
    """型安全な関数定義例"""
    pass
```

### 5. Testing Strategy

- **ユニットテスト**: 個別モジュール・関数のテスト
- **統合テスト**: ビルドプロセス全体のテスト
- **フィクスチャベース**: 実際の Sphinx プロジェクトでテスト
- **出力検証**: 生成された Typst コードの妥当性確認

### 6. Documentation-Driven Development

- すべての公開 API に docstring
- Sphinx autodoc でAPI ドキュメント自動生成
- 使用例を examples/ に配置
- "dogfooding": 自身のドキュメントを sphinx-typst でビルド

## Code Style Guidelines

### Formatting

- **Line Length**: 88 文字 (Black デフォルト)
- **Indentation**: スペース 4 個
- **Quotes**: ダブルクォート優先 (Black 準拠)

### Documentation

```python
def convert_section(node: nodes.section, level: int) -> str:
    """
    セクションノードを Typst ヘディングに変換

    Args:
        node: docutils section ノード
        level: セクションレベル (1-6)

    Returns:
        Typst マークアップ文字列

    Raises:
        ValueError: level が範囲外の場合

    Example:
        >>> node = nodes.section()
        >>> convert_section(node, 1)
        '= Section Title'
    """
    pass
```

### Error Handling

- 明示的なエラーメッセージ
- Sphinx の警告システムを活用
- ユーザーフレンドリーなエラー出力

```python
from sphinx.util import logging

logger = logging.getLogger(__name__)

def build_document(source: str) -> None:
    try:
        # ビルド処理
        pass
    except TypstError as e:
        logger.error(f"Typst conversion failed: {e}", location=source)
        raise
```
