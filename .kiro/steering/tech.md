# Technology Stack

## Architecture

### High-Level Design

sphinx-typst は Sphinx 拡張アーキテクチャに基づいて構築されます：

```
┌─────────────────────────────────────────┐
│         Sphinx Document Source          │
│    (reStructuredText / Markdown)        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Sphinx Parser & Doctree         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      sphinx-typst Builder/Writer        │
│    - Doctree → Typst Conversion        │
│    - Template Processing                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Typst Markup Files              │
│         (typst builder)                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Typst Compiler (typst-py 0.11.1)    │
│    (typstpdf builder - built-in)       │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│            Output (PDF)                 │
└─────────────────────────────────────────┘
```

### Key Components

1. **Dual Builders**:
   - `TypstBuilder`: Typst マークアップファイルを生成
   - `TypstPDFBuilder`: typst-py を使用して直接 PDF を生成
2. **Typst Writer**: Doctree ノードを Typst マークアップに変換するライター
3. **Template Engine**: Typst ドキュメントテンプレート管理とパラメータマッピング
4. **Translator**: 各種 docutils ノードの Typst 変換ロジック（visitor パターン）
5. **PDF Generator**: typst-py ラッパーによる PDF 生成
6. **Config Integration**: Sphinx 設定と Typst オプションの統合

## Backend

### Language & Framework

- **Python 3.9+**: Sphinx が Python 3.9+ を要求
- **Sphinx 5.0+**: 最新の Sphinx API を活用
- **docutils**: Sphinx のドキュメントツリー処理

### Core Dependencies

```python
# 主要依存関係 (pyproject.toml より)
sphinx >= 5.0
docutils >= 0.18
typst-py >= 0.11.1  # Typst の Python バインディング (自己完結型 PDF 生成)
```

### External Tools (Optional)

- **Typst CLI**: オプショナル - typst ビルダー出力を手動でコンパイルする場合のみ必要
  - インストール方法: https://github.com/typst/typst
  - バージョン要件: 0.11.0+
  - **注**: typstpdf ビルダーは typst-py を使用するため Typst CLI は不要

## Development Environment

### Required Tools

1. **Python Development**
   - Python 3.9 以上
   - **uv**: 高速パッケージマネージャ（推奨）
   - pip: フォールバックオプション

2. **Typst (Optional)**
   - Typst CLI ツール（オプショナル）
   - typst ビルダー出力を手動コンパイルする場合のみ必要

3. **Testing Tools**
   - pytest: ユニットテスト、統合テスト、E2Eテスト（313 テスト）
   - pytest-cov: カバレッジ測定（94% 達成）
   - tox: 複数環境でのテスト
   - typst-py: E2E PDF生成テスト用

4. **Development Tools**
   - black: コードフォーマッター
   - ruff: 高速リンター
   - mypy: 型チェック

### Setup Instructions

```bash
# uv を使用した開発環境セットアップ（推奨）
uv sync --extra dev

# または pip を使用
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"

# テスト実行
uv run pytest
# または: pytest

# Typst CLI の確認（オプショナル）
typst --version  # typstpdf ビルダーには不要
```

## Common Commands

### Development Commands

```bash
# テスト実行（uv 使用 - 推奨）
uv run pytest                          # すべてのテスト（313 tests）
uv run pytest tests/test_builder.py   # 特定のテストファイル
uv run pytest -v                       # 詳細出力
uv run pytest --cov                    # カバレッジ付き（94%）
uv run pytest tests/test_nested_toctree_paths.py  # ユニットテスト（Issue #5）
uv run pytest tests/test_integration_nested_toctree.py  # 統合・E2Eテスト

# 複数環境でのテスト
uv run tox

# コード品質チェック
uv run black .                         # フォーマット
uv run ruff check .                    # リント
uv run mypy sphinxcontrib/            # 型チェック

# ドキュメントビルド (自己ドキュメント)
sphinx-build -b html docs/ docs/_build/html
sphinx-build -b typst docs/ docs/_build/typst
sphinx-build -b typstpdf docs/ docs/_build/pdf  # PDF 直接生成

# パッケージビルド
python -m build                 # sdist と wheel を生成
twine check dist/*             # パッケージ検証
```

### Sphinx with Typst Builder

```bash
# Typst マークアップ生成
sphinx-build -b typst source/ build/typst
sphinx-build -b typst -a source/ build/typst  # 全ファイル再ビルド

# 直接 PDF 生成（推奨 - typst-py 使用）
sphinx-build -b typstpdf source/ build/pdf

# または Typst CLI で手動コンパイル（オプショナル）
typst compile build/typst/index.typ output.pdf
```

## Environment Variables

### Development Configuration

```bash
# Typst 実行パス (非標準インストール時)
export TYPST_PATH=/path/to/typst

# デバッグモード
export SPHINX_TYPST_DEBUG=1

# Typst コンパイラオプション
export TYPST_FONT_PATHS=/path/to/custom/fonts
```

### Testing Configuration

```bash
# テスト時の一時ディレクトリ
export PYTEST_TMPDIR=/custom/tmp

# テストカバレッジ設定
export COVERAGE_FILE=.coverage
```

## Port Configuration

このプロジェクトは主にビルドツール・コマンドラインツールであり、通常ポートを使用しません。

ただし、開発時のドキュメントプレビューで以下を使用する可能性があります：

```bash
# Sphinx autobuild による開発サーバー
sphinx-autobuild docs/ docs/_build/html --port 8000
# → http://localhost:8000
```

## Build & Distribution

### Package Structure

- **Package Name**: `sphinxcontrib-typst`
- **Namespace**: `sphinxcontrib.typst`
- **Entry Point**: Sphinx builder として自動検出

### Configuration Files

- `pyproject.toml`: プロジェクトメタデータ、ビルド設定、依存関係
- `setup.py` / `setup.cfg`: レガシー互換性 (必要に応じて)
- `.pre-commit-config.yaml`: pre-commit フック設定
- `tox.ini`: 複数環境でのテスト自動化

## Extension Points

### Sphinx Configuration

```python
# conf.py での設定例

# 注: sphinxcontrib.typst は entry points で自動検出されます
# extensions リストへの追加はオプショナルですが、明示性のため推奨
# extensions = ['sphinxcontrib.typst']

# Typst ビルダー設定
typst_use_mitex = True  # LaTeX 数式に mitex を使用（デフォルト: True）

# テンプレートカスタマイズ
typst_template = '_templates/custom.typ'  # オプショナル
typst_elements = {
    'papersize': 'a4',
    'fontsize': '11pt',
    'lang': 'ja',
}

# メタデータマッピング
typst_template_mapping = {
    'title': 'project',      # Sphinx の project → template の title
    'authors': ['author'],   # Sphinx の author → template の authors
    'date': 'release',       # Sphinx の release → template の date
}

# toctree デフォルト設定
typst_toctree_defaults = {
    'maxdepth': 2,
    'numbered': True,
}
```

### Custom Templates

- テンプレートディレクトリ: `_templates/typst/`
- カスタムテンプレート変数のサポート
- Typst マクロ・関数の埋め込み
