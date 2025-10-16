# Project Context

## Purpose

sphinxcontrib-typst は、Sphinx ドキュメントジェネレータと Typst タイプセッティングシステムを統合する拡張機能です。Sphinx の強力なドキュメント生成機能と Typst のモダンな組版機能を組み合わせ、高品質な技術文書の作成を可能にします。

### Core Features

- **Sphinx to Typst Conversion**: Sphinx ドキュメント(reStructuredText/Markdown)を Typst フォーマットに変換
- **Dual Builder Integration**:
  - `typst` ビルダー: Typst マークアップファイルを生成
  - `typstpdf` ビルダー: PDF を直接生成（外部 Typst CLI 不要）
- **Self-Contained PDF Generation**: typst-py による自己完結型 PDF 生成（外部ツール不要）
- **カスタマイズ可能な出力**: Typst テンプレートとスタイルのカスタマイズをサポート
- **相互参照とインデックス**: Sphinx の相互参照、インデックス、目次機能を Typst で再現
- **コードハイライト**: codly パッケージによるシンタックスハイライトと行番号表示
- **数式サポート**: mitex による LaTeX 数式またはネイティブ Typst 数式
- **図表管理**: 画像、表、図表の埋め込みと参照管理
- **マルチドキュメント対応**: toctree による `#include()` 統合

### Target Users

- Python ドキュメント作成者で、より美しい PDF 出力を求める開発者
- Sphinx を使用しているが LaTeX の設定に苦労しているチーム
- モダンな組版システム(Typst)を既存の Sphinx ワークフローに統合したいユーザー
- 技術文書と学術文書の両方を扱うドキュメンテーションチーム

## Tech Stack

### Language & Framework
- **Python 3.9+**: Sphinx が Python 3.9+ を要求
- **Sphinx 5.0+**: 最新の Sphinx API を活用
- **docutils**: Sphinx のドキュメントツリー処理
- **typst-py >= 0.11.1**: Typst の Python バインディング (自己完結型 PDF 生成)

### Typst Packages
- `@preview/mitex:0.2.4`: LaTeX math rendering
- `@preview/codly:1.3.0`: Code syntax highlighting
- `@preview/codly-languages:0.1.1`: Language definitions
- `@preview/gentle-clues:1.2.0`: Admonition styling

### Development Tools
- **uv**: 高速パッケージマネージャ（推奨）
- **pytest**: ユニットテスト、統合テスト、E2Eテスト（317 テスト、94% カバレッジ）
- **black**: コードフォーマッター
- **ruff**: 高速リンター
- **mypy**: 型チェック
- **tox**: 複数環境でのテスト

## Project Conventions

### Code Style

- **Line Length**: 88 文字 (Black デフォルト)
- **Indentation**: スペース 4 個
- **Quotes**: ダブルクォート優先 (Black 準拠)
- **Module Names**: `snake_case` (例: `builder.py`, `translator.py`)
- **Class Names**: `PascalCase` (例: `TypstBuilder`, `TypstWriter`)
- **Function Names**: `snake_case` (例: `convert_doctree`, `render_template`)
- **Constants**: `UPPER_SNAKE_CASE` (例: `DEFAULT_TEMPLATE`, `TYPST_VERSION`)

### Import Organization (PEP 8)

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

### Architecture Patterns

#### Separation of Concerns
- **Builder**: ビルドプロセス管理、ファイル I/O
- **Writer**: Doctree から Typst マークアップへの変換オーケストレーション
- **Translator**: 個別ノードタイプの Typst 変換ロジック (Visitor パターン)
- **Templates**: 出力ドキュメントの構造とスタイル

#### Sphinx Extension Pattern
```python
def setup(app: Sphinx) -> Dict[str, Any]:
    """Sphinx 拡張エントリーポイント

    Note: pyproject.toml の entry points で自動検出されるため、
    conf.py の extensions リストへの追加はオプショナル
    """
    app.add_builder(TypstBuilder)
    app.add_builder(TypstPDFBuilder)
    app.add_config_value('typst_use_mitex', True, 'html')
    # ...
    return {'version': '0.2.0', 'parallel_read_safe': True}
```

### Testing Strategy

- **ユニットテスト**: 個別モジュール・関数のテスト
- **統合テスト**: ビルドプロセス全体のテスト
- **E2Eテスト**: Typst PDF 生成の完全検証
- **フィクスチャベース**: 実際の Sphinx プロジェクトでテスト
- **出力検証**: 生成された Typst コードの妥当性確認
- **317 tests, 94% coverage**

Test file naming:
- **Test modules**: `test_*.py`
- **Test classes**: `Test*`
- **Test functions**: `test_*`

### Git Workflow

- **Main branch**: `main` (stable releases)
- **Feature branches**: `feature/[feature-name]` or `[type]/[description]`
  - `feature/`: New features
  - `fix/`: Bug fixes
  - `docs/`: Documentation updates
  - `improve/`: Improvements to existing features
- **Release branches**: `release/v[version]`
- **Commit messages**: Conventional Commits format preferred
- **Pull Requests**: Required for all changes to main
- **CI/CD**: GitHub Actions (tests, lint, type check, coverage)

## Domain Context

### Sphinx Architecture
- **Doctree**: Internal document tree representation (docutils nodes)
- **Builder**: Converts doctree to output format
- **Writer/Translator**: Visitor pattern for node transformation
- **Extensions**: Registered via `setup()` function or entry points

### Typst Concepts
- **Markup Language**: Modern alternative to LaTeX
- **Templates**: Function-based document templates
- **Packages**: Reusable components from Typst Universe (`@preview/*`)
- **PDF Generation**: Built-in compiler (no external tools needed with typst-py)

### Key Integration Points
- **Entry Points**: `sphinx.builders` for auto-discovery
- **Node Translation**: docutils nodes → Typst markup
- **Template System**: Sphinx metadata → Typst template parameters
- **Multi-Document**: toctree → `#include()` directives with relative paths

## Important Constraints

### Technical Constraints
- **Python**: Minimum version 3.9
- **Sphinx**: Minimum version 5.0
- **Type Safety**: Full type hints required for public APIs
- **Backwards Compatibility**: Follow Semantic Versioning

### Package Management
- **Always use `uv` commands** for package management and task execution
  - Running commands: `uv run <command>`
  - Running tests: `uv run pytest`
  - Installing packages: `uv add <package>`
  - Syncing dependencies: `uv sync`
- Do NOT use `pip` or bare `python` commands directly
- Do NOT use `poetry` or other package managers

### Quality Gates
- **Test Coverage**: Maintain 90%+ coverage
- **Type Checking**: All code must pass `mypy --strict`
- **Linting**: Must pass `ruff check` and `black --check`
- **CI/CD**: All tests must pass before merge

### Development Language
- **思考**: English (for technical analysis and planning)
- **コメント・文字列**: 日本語または英語（プロジェクトの文脈に応じて）
- **GitHub interactions**: Always English (issues, PRs, commit messages)

## External Dependencies

### Required
- **Sphinx** (≥5.0): Documentation generator
- **docutils** (≥0.18): Document processing
- **typst-py** (≥0.11.1): Typst compiler (Python bindings)

### Optional
- **Typst CLI**: Only needed for manual compilation of `.typ` files
- **tox**: Multi-environment testing
- **sphinx-autobuild**: Development server for live preview

### Typst Universe Packages
All packages are downloaded automatically by Typst compiler:
- `@preview/mitex:0.2.4`
- `@preview/codly:1.3.0`
- `@preview/codly-languages:0.1.1`
- `@preview/gentle-clues:1.2.0`

## Project Structure

```
sphinxcontrib-typst/
├── openspec/                   # OpenSpec spec-driven development
│   ├── project.md              # This file
│   ├── AGENTS.md               # AI assistant instructions
│   ├── specs/                  # Current specifications
│   └── changes/                # Proposed changes
├── sphinxcontrib/              # Main package
│   └── typst/                  # Typst builder implementation
│       ├── __init__.py         # Extension entry point
│       ├── builder.py          # TypstBuilder
│       ├── pdf.py              # TypstPDFBuilder
│       ├── writer.py           # TypstWriter
│       ├── translator.py       # TypstTranslator
│       ├── template_engine.py  # Template processing
│       └── templates/          # Default Typst templates
├── tests/                      # Test suite (317 tests, 94% coverage)
├── docs/                       # Project documentation
├── examples/                   # Sample projects
├── pyproject.toml              # Project configuration
├── README.md                   # Project overview
├── CLAUDE.md                   # Claude Code configuration
├── AGENTS.md                   # OpenSpec AI instructions
├── LICENSE                     # MIT License
└── CHANGELOG.md                # Version history
```

## Common Commands

### Development
```bash
# Install dependencies
uv sync --extra dev

# Run tests
uv run pytest                          # All tests (317)
uv run pytest -v                       # Verbose output
uv run pytest --cov                    # With coverage (94%)

# Code quality
uv run black .                         # Format code
uv run ruff check .                    # Lint
uv run mypy sphinxcontrib/            # Type check

# Build documentation
sphinx-build -b html docs/ docs/_build/html
sphinx-build -b typstpdf docs/ docs/_build/pdf
```

### Sphinx with Typst
```bash
# Generate Typst markup
sphinx-build -b typst source/ build/typst

# Generate PDF directly
sphinx-build -b typstpdf source/ build/pdf
```

## Release Status

**Current Version**: v0.2.0 (Stable)
- **Status**: Production-ready
- **All 13 requirements**: Fully implemented (100%)
- **Test Coverage**: 94% (317 tests)
- **Distribution**: PyPI - `pip install sphinxcontrib-typst`
- **CI/CD**: Validated on Linux, macOS, Windows
- **Python Support**: 3.9, 3.10, 3.11, 3.12
