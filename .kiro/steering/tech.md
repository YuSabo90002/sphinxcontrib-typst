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
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       Typst Compiler (External)         │
│         (typst compile)                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│            Output (PDF)                 │
└─────────────────────────────────────────┘
```

### Key Components

1. **Typst Builder**: `sphinx.builders.Builder` を継承したカスタムビルダー
2. **Typst Writer**: Doctree ノードを Typst マークアップに変換するライター
3. **Template Engine**: Typst ドキュメントテンプレート管理
4. **Node Visitors**: 各種 docutils ノードの Typst 変換ロジック
5. **Config Integration**: Sphinx 設定と Typst オプションの統合

## Backend

### Language & Framework

- **Python 3.9+**: Sphinx が Python 3.9+ を要求
- **Sphinx 5.0+**: 最新の Sphinx API を活用
- **docutils**: Sphinx のドキュメントツリー処理

### Core Dependencies

```python
# 予定される主要依存関係
sphinx >= 5.0
docutils >= 0.18
typst-py  # Typst の Python バインディング (存在する場合)
```

### External Tools

- **Typst CLI**: PDF 生成のための外部コマンド (`typst compile`)
  - インストール方法: https://github.com/typst/typst
  - バージョン要件: 0.10.0+

## Development Environment

### Required Tools

1. **Python Development**
   - Python 3.9 以上
   - pip / pipenv / poetry (パッケージ管理)
   - virtualenv 推奨

2. **Typst**
   - Typst CLI ツール
   - PDF 生成のために必要

3. **Testing Tools**
   - pytest: ユニットテスト、統合テスト
   - sphinx-testing: Sphinx 拡張のテストヘルパー
   - coverage: コードカバレッジ測定

4. **Development Tools**
   - black: コードフォーマッター
   - flake8 / ruff: リンター
   - mypy: 型チェック
   - pre-commit: Git フック管理

### Setup Instructions

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 依存関係インストール
pip install -e ".[dev]"

# Typst インストール確認
typst --version

# テスト実行
pytest
```

## Common Commands

### Development Commands

```bash
# テスト実行
pytest                          # すべてのテスト
pytest tests/test_builder.py   # 特定のテストファイル
pytest -v                       # 詳細出力
pytest --cov                    # カバレッジ付き

# コード品質チェック
black .                         # フォーマット
flake8 sphinxcontrib/          # リント
mypy sphinxcontrib/            # 型チェック

# ドキュメントビルド (自己ドキュメント)
sphinx-build -b html docs/ docs/_build/html
sphinx-build -b typst docs/ docs/_build/typst

# パッケージビルド
python -m build                 # sdist と wheel を生成
twine check dist/*             # パッケージ検証
```

### Sphinx with Typst Builder

```bash
# Typst ビルダー使用例
sphinx-build -b typst source/ build/typst
sphinx-build -b typst -a source/ build/typst  # 全ファイル再ビルド

# Typst から PDF 生成
typst compile build/typst/index.typ output.pdf

# ワンステップビルド (予定機能)
sphinx-build -b typstpdf source/ build/pdf
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
extensions = [
    'sphinxcontrib.typst',
]

# Typst ビルダー設定
typst_documents = [
    ('index', 'output.typ', 'Project Documentation', 'Author Name'),
]

typst_template = 'custom_template.typ'
typst_elements = {
    'papersize': 'a4',
    'fontsize': '11pt',
}
```

### Custom Templates

- テンプレートディレクトリ: `_templates/typst/`
- カスタムテンプレート変数のサポート
- Typst マクロ・関数の埋め込み
