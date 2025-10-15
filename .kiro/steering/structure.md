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
├── __init__.py                 # 拡張エントリーポイント (setup 関数)
├── builder.py                  # TypstBuilder - Typst マークアップ生成
├── pdf.py                      # TypstPDFBuilder - PDF 直接生成
├── writer.py                   # TypstWriter (doctree → typst)
├── translator.py               # TypstTranslator (Node visitor パターン)
├── template_engine.py          # テンプレート処理とパラメータマッピング
└── templates/                  # デフォルト Typst テンプレート
    ├── base.typ                # 基本テンプレート
    └── article.typ             # 記事スタイルテンプレート
```

#### `tests/` - Test Suite
テストコードの配置（313 テスト、94% カバレッジ）

```
tests/
├── conftest.py                      # pytest 設定とフィクスチャ
├── test_builder.py                  # TypstBuilder のテスト
├── test_translator.py               # TypstTranslator のテスト
├── test_template_engine.py          # テンプレートエンジンのテスト
├── test_pdf_generation.py           # PDF 生成のテスト
├── test_config*.py                  # 設定関連のテスト
├── test_math_*.py                   # 数式変換のテスト (mitex/native)
├── test_template_*.py               # テンプレート機能のテスト
├── test_integration_*.py            # 統合テスト
├── test_documentation_*.py          # ドキュメンテーションのテスト
├── test_entry_points.py             # Entry points 自動検出のテスト
├── test_extension.py                # 拡張機能のテスト
├── test_nested_toctree_paths.py     # ユニットテスト（相対パス計算、Issue #5）
├── test_integration_nested_toctree.py  # 統合・E2Eテスト（Issue #5）
├── fixtures/                        # テスト用フィクスチャ
│   ├── integration_basic/           # 基本統合テスト用
│   ├── integration_multi_doc/       # マルチドキュメント用
│   ├── integration_math_figures/    # 数式・図表用
│   ├── integration_nested_toctree/  # Issue #5再現テスト用（2階層ネスト）
│   ├── integration_multi_level/     # 3階層ネストテスト用（Issue #5）
│   └── integration_sibling/         # 兄弟ディレクトリ参照テスト用（Issue #5）
└── roots/                           # Sphinx テストルート
    └── test-basic/                  # 基本テストプロジェクト
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
└── requirements.txt            # ドキュメントビルド用依存関係
```

#### `examples/` - Example Projects
実際の使用例を示すサンプルプロジェクト

```
examples/
├── basic/                      # 基本的な使用例
│   ├── conf.py
│   ├── index.rst
│   └── README.md
└── advanced/                   # 高度な使用例
    ├── conf.py
    ├── index.rst
    ├── chapter1.rst
    ├── chapter2.rst
    └── README.md
```

## Code Organization Patterns

### Sphinx Extension Pattern

Sphinx 拡張の標準パターンに従います。Entry points による自動検出をサポート：

```python
# sphinxcontrib/typst/__init__.py
from typing import Any, Dict
from sphinx.application import Sphinx
from .builder import TypstBuilder
from .pdf import TypstPDFBuilder

def setup(app: Sphinx) -> Dict[str, Any]:
    """Sphinx 拡張エントリーポイント

    Note: pyproject.toml の entry points で自動検出されるため、
    conf.py の extensions リストへの追加はオプショナル
    """
    # 両方のビルダーを登録
    app.add_builder(TypstBuilder)
    app.add_builder(TypstPDFBuilder)

    # 設定値の追加
    app.add_config_value('typst_use_mitex', True, 'html')
    app.add_config_value('typst_template', None, 'html')
    app.add_config_value('typst_elements', {}, 'html')
    app.add_config_value('typst_template_mapping', {}, 'html')
    app.add_config_value('typst_toctree_defaults', {}, 'html')

    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

Entry points 定義（pyproject.toml）:
```toml
[project.entry-points."sphinx.builders"]
typst = "sphinxcontrib.typst:TypstBuilder"
typstpdf = "sphinxcontrib.typst:TypstPDFBuilder"
```

### Builder Pattern

```python
# sphinxcontrib/typst/builder.py
from sphinx.builders import Builder
from .writer import TypstWriter

class TypstBuilder(Builder):
    name = 'typst'
    format = 'typst'
    out_suffix = '.typ'

    def init(self) -> None:
        """ビルダー初期化"""
        self.writer = TypstWriter(self)

    def get_outdated_docs(self) -> Iterator[str]:
        """更新が必要なドキュメントを特定"""
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
            targetname = self.get_outfilename(docname)
            if not path.isfile(targetname):
                yield docname

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """ドキュメント書き込み"""
        self.current_docname = docname
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = self.get_outfilename(docname)
        ensuredir(path.dirname(outfilename))
        with open(outfilename, 'w', encoding='utf-8') as f:
            f.write(self.writer.output)
```

PDF Builder（pdf.py）:
```python
# sphinxcontrib/typst/pdf.py
from .builder import TypstBuilder
import typst

class TypstPDFBuilder(TypstBuilder):
    name = 'typstpdf'
    format = 'pdf'
    out_suffix = '.pdf'

    def finish(self) -> None:
        """すべてのドキュメント処理後に PDF を生成"""
        super().finish()
        # typst-py を使用して PDF 生成
        for docname in self.env.found_docs:
            typ_file = self.get_typst_file(docname)
            pdf_file = self.get_outfilename(docname)
            typst.compile(typ_file, output=pdf_file)
```

### Visitor Pattern for Node Translation

```python
# sphinxcontrib/typst/translator.py
from docutils import nodes
from sphinx.writers import Writer

class TypstTranslator(nodes.NodeVisitor):
    """Doctree ノードを Typst に変換

    各ノードタイプに対して visit_* および depart_* メソッドを実装
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document)
        self.builder = builder
        self.body: List[str] = []
        self.section_level = 0

    def visit_section(self, node: nodes.section) -> None:
        """セクション開始時の処理"""
        self.section_level += 1

    def depart_section(self, node: nodes.section) -> None:
        """セクション終了時の処理"""
        self.section_level -= 1

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        """段落の処理"""
        pass

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        """段落終了"""
        self.body.append('\n\n')

    # その他多数のノードタイプに対応
    # visit_literal_block, visit_image, visit_table, など
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
