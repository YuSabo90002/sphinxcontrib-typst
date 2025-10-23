# Tasks: Rename Package to typsphinx

`sphinxcontrib-typst` から `typsphinx` へのパッケージ名変更の実装タスク。

## Phase 1: パッケージ構造の移行

### Task 1.1: Rename package directory
- [ ] Move `sphinxcontrib/typst/` to `typsphinx/`
- [ ] Remove empty `sphinxcontrib/` directory
- [ ] Verify all Python files are in new location

**Validation**: `ls typsphinx/` shows all module files

### Task 1.2: Update pyproject.toml
- [ ] Change `name = "sphinxcontrib-typst"` to `name = "typsphinx"`
- [ ] Update `packages = [{include = "sphinxcontrib"}]` to `packages = [{include = "typsphinx"}]`
- [ ] Remove `[tool.setuptools.package-data]` for `sphinxcontrib.typst` namespace
- [ ] Add package data for `typsphinx` namespace if needed

**Validation**: `uv build` succeeds and creates `typsphinx-*.whl`

### Task 1.3: Update __init__.py
- [ ] Update module docstring to reflect new package name
- [ ] Verify `setup()` function works with new namespace
- [ ] Ensure version and metadata are correct

**Validation**: `python -c "import typsphinx; print(typsphinx.__version__)"` works

## Phase 2: インポート文の更新

### Task 2.1: Update internal imports in source code
- [ ] Update `builder.py` imports
- [ ] Update `pdf.py` imports
- [ ] Update `writer.py` imports
- [ ] Update `translator.py` imports
- [ ] Update `template_engine.py` imports
- [ ] Update any other `.py` files in `sphinx_typst/`

**Validation**: `uv run ruff check` passes, no import errors

### Task 2.2: Update test imports
- [ ] Update `tests/test_*.py` files (37 files based on grep count)
- [ ] Update `tests/conftest.py`
- [ ] Verify no `from sphinxcontrib.typst import` remains

**Validation**: `rg "from sphinxcontrib" tests/` returns no results

### Task 2.3: Update fixture conf.py files
- [ ] Update `tests/roots/test-basic/conf.py`
- [ ] Update `tests/fixtures/*/conf.py` files (6 fixture directories)
- [ ] Change all `extensions = ['sphinxcontrib.typst']` to `extensions = ['typsphinx']`

**Validation**: `rg "sphinxcontrib\.typst" tests/` returns no results in conf.py

### Task 2.4: Update example projects
- [ ] Update `examples/basic/conf.py`
- [ ] Update `examples/advanced/conf.py`
- [ ] Test both examples build successfully

**Validation**:
```bash
cd examples/basic && sphinx-build -b typst . _build/typst
cd examples/advanced && sphinx-build -b typstpdf . _build/pdf
```

## Phase 3: テストと検証

### Task 3.1: Run full test suite
- [ ] Run `uv run pytest` and verify all 339 tests pass
- [ ] Run `uv run pytest --cov` and verify coverage is maintained (≥73%)
- [ ] Check for any deprecation warnings

**Validation**: All tests pass, no import-related failures

### Task 3.2: Run code quality checks
- [ ] Run `uv run black .` and fix any formatting issues
- [ ] Run `uv run ruff check .` and fix any linting issues
- [ ] Run `uv run mypy typsphinx/` and fix any type errors

**Validation**: All checks pass with zero errors

### Task 3.3: Manual integration testing
- [ ] Create a temporary Sphinx project
- [ ] Add `extensions = ['typsphinx']` to conf.py
- [ ] Build with both `typst` and `typstpdf` builders
- [ ] Verify output is correct

**Validation**: Both builders work correctly

## Phase 4: ドキュメントの更新

### Task 4.1: Update README.md
- [ ] Change installation from `sphinxcontrib-typst` to `typsphinx`
- [ ] Update configuration examples to use `extensions = ['typsphinx']`
- [ ] Update import examples if any
- [ ] Update version badge to v0.3.0

**Validation**: README correctly documents new package name

### Task 4.2: Update CHANGELOG.md
- [ ] Add v0.3.0 section with breaking changes
- [ ] Document package rename as breaking change
- [ ] Explain rationale for rename

**Validation**: CHANGELOG documents breaking change

### Task 4.3: Update GitHub Actions workflows
- [ ] Update `.github/workflows/release.yml`:
  - Line 70: `mypy sphinxcontrib/` → `mypy typsphinx/`
  - Line 113: PyPI URL to `https://pypi.org/p/typsphinx`
  - Line 173: Install command to `pip install typsphinx`
  - Line 203: TestPyPI URL to `https://test.pypi.org/p/typsphinx`
- [ ] Update `.github/workflows/ci.yml`:
  - Line 89: `mypy sphinxcontrib/` → `mypy typsphinx/`
  - Line 110: `--cov=sphinxcontrib.typst` → `--cov=typsphinx`

**Validation**: `rg "sphinxcontrib" .github/` returns no results

### Task 4.4: Update other documentation
- [ ] Check for any references to `sphinxcontrib-typst` in docs/
- [ ] Update GitHub repository description (via web UI after rename)
- [ ] Update openspec/project.md with new package structure

**Validation**: `rg "sphinxcontrib-typst" docs/` returns minimal or no results

## Phase 5: リポジトリとリリース

### Task 5.1: Update version to 0.3.0
- [ ] Update version in `pyproject.toml` to `0.3.0`
- [ ] Update version in `typsphinx/__init__.py` to `0.3.0`

**Validation**: `python -c "import typsphinx; print(typsphinx.__version__)"` prints `0.3.0`

### Task 5.2: Commit and create PR
- [ ] Commit all changes with clear message
- [ ] Push to branch `refactor/rename-to-typsphinx`
- [ ] Create PR with detailed description of breaking changes

**Validation**: PR created on GitHub

### Task 5.3: Rename GitHub repository
- [ ] After PR approval, rename repository from `sphinxcontrib-typst` to `typsphinx` (Settings → Repository name)
- [ ] Verify old URL redirects to new URL
- [ ] Update local git remote: `git remote set-url origin <new-url>`

**Validation**: Repository accessible at new name, old URL redirects

### Task 5.4: Merge and release
- [ ] Merge PR to main
- [ ] Create git tag v0.3.0
- [ ] Push tag to GitHub
- [ ] Create GitHub release with migration notes

**Validation**: GitHub release v0.3.0 published

## Phase 6: PyPIへの公開（オプション - OpenSpec実装後）

これらのタスクはOpenSpec実装の範囲外ですが、完全性のために文書化されています：

- [ ] Publish `typsphinx` v0.3.0 to PyPI
- [ ] Verify PyPI package installs correctly
- [ ] Test installation in clean environment

## 依存関係

- Phase 2はPhase 1に依存（構造変更前にインポートは更新できない）
- Phase 3はPhase 2に依存（インポート更新前にテストできない）
- Phase 4はPhase 3と並行実施可能
- Phase 5はPhase 1-4のすべてが完了していることに依存
- Phase 6はPhase 5に依存（リポジトリ名変更を先に実施する必要がある）

## ロールバック計画

重大な問題が発見された場合：

1. 前のv0.2.2タグからhotfixブランチを作成
2. 重大な修正を適用
3. v0.2.3としてリリース
4. 問題が解決するまでv0.3.0の改名を延期

PyPI公開前であれば、以下の方法で改名を元に戻すことができます：
1. PRをrevert
2. リポジトリ名を元に戻す
3. 古いパッケージ名を維持
