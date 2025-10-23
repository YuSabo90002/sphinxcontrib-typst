# package-structure Specification

## Purpose
TBD - created by archiving change rename-package-to-typsphinx. Update Purpose after archive.
## Requirements
### Requirement: Package uses typsphinx namespace

パッケージは `sphinxcontrib.typst` の代わりに `typsphinx` をPythonパッケージ名前空間として使用しなければなりません（MUST）。

#### Scenario: Import package with new namespace

**GIVEN** a Python environment with typsphinx installed
**WHEN** user imports the package
**THEN** `import typsphinx` succeeds
**AND** `typsphinx.__version__` is accessible
**AND** `from sphinxcontrib.typst import ...` fails with ImportError

#### Scenario: Package directory structure uses new name

**GIVEN** the repository root
**WHEN** examining the directory structure
**THEN** `typsphinx/` directory exists
**AND** `sphinxcontrib/typst/` directory does not exist
**AND** `typsphinx/__init__.py` contains the version and setup function

### Requirement: Sphinx extension uses new module name

Sphinxユーザーは新しいパッケージ名を使用して拡張機能をロードできなければなりません（MUST）。

#### Scenario: Load extension in conf.py with new name

**GIVEN** a Sphinx project with typsphinx installed
**WHEN** `conf.py` contains `extensions = ['typsphinx']`
**THEN** `sphinx-build` successfully loads the extension
**AND** both `typst` and `typstpdf` builders are available
**AND** no warnings or errors are emitted about missing extensions

#### Scenario: Old extension name fails with clear error

**GIVEN** a Sphinx project with typsphinx v0.3.0+ installed
**WHEN** `conf.py` contains `extensions = ['sphinxcontrib.typst']`
**THEN** `sphinx-build` fails with ImportError or extension not found error
**AND** error message is clear about the module name change

### Requirement: PyPI package uses typsphinx name

パッケージは `typsphinx` という名前でPyPIに配布されなければなりません（MUST）。

#### Scenario: Install package from PyPI with new name

**GIVEN** PyPI has typsphinx v0.3.0 published
**WHEN** user runs `pip install typsphinx`
**THEN** package installs successfully
**AND** `typsphinx` module is importable
**AND** `pip list` shows `typsphinx` (not `sphinxcontrib-typst`)

### Requirement: All internal imports use new namespace

パッケージ内のすべてのPythonファイルは、インポートに新しい `typsphinx` 名前空間を使用しなければなりません（MUST）。

#### Scenario: Internal imports use new namespace

**GIVEN** the typsphinx package source code
**WHEN** examining all `.py` files in `typsphinx/`
**THEN** all relative imports within the package work correctly
**AND** no imports reference `sphinxcontrib.typst`
**AND** imports use `from typsphinx import ...` or `from typsphinx.module import ...`

### Requirement: Tests use new namespace

すべてのテストファイルは、新しい名前空間を使用してパッケージをインポートし、テストしなければなりません（MUST）。

#### Scenario: Test imports use new namespace

**GIVEN** the test suite
**WHEN** running `pytest`
**THEN** all tests pass
**AND** test files import using `import typsphinx` or `from typsphinx import ...`
**AND** no test references `sphinxcontrib.typst` module

#### Scenario: Test fixtures use new extension name

**GIVEN** test fixtures with Sphinx projects
**WHEN** examining fixture `conf.py` files
**THEN** all fixtures use `extensions = ['typsphinx']`
**AND** no fixture uses `extensions = ['sphinxcontrib.typst']`

### Requirement: Examples use new namespace

サンプルプロジェクトは新しいパッケージの使用方法を示さなければなりません（MUST）。

#### Scenario: Example conf.py files use new extension

**GIVEN** example projects in `examples/`
**WHEN** examining their `conf.py` files
**THEN** all examples use `extensions = ['typsphinx']`
**AND** examples build successfully with `sphinx-build`

### Requirement: Documentation reflects new package name

すべてのドキュメントは新しいパッケージ名を参照しなければなりません（MUST）。

#### Scenario: README shows new installation

**GIVEN** the README.md file
**WHEN** user reads installation instructions
**THEN** documentation shows `pip install typsphinx`
**AND** configuration example uses `extensions = ['typsphinx']`

#### Scenario: CHANGELOG documents breaking change

**GIVEN** CHANGELOG.md
**WHEN** examining v0.3.0 release notes
**THEN** breaking change is clearly documented
**AND** rationale for rename is explained

