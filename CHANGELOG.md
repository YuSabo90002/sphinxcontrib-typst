# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Migrate CI to Tox**
  - GitHub Actions workflows now use tox commands for consistency
  - Added `docs-html`, `docs-pdf`, and `docs` tox environments
  - Simplified CI configuration with single source of truth in `tox.ini`
  - Improved local/CI consistency - same commands work in both environments
  - Updated test, lint, type-check, and coverage jobs to use tox
  - Documentation builds now reproducible locally with `tox -e docs-html` or `tox -e docs-pdf`
  - Fixed paths in existing tox environments (sphinxcontrib/ → typsphinx/)

### Added

- **Documentation Site with GitHub Pages** ([#36](https://github.com/YuSabo90002/typsphinx/issues/36))
  - Comprehensive documentation site hosted on GitHub Pages at https://yusabo90002.github.io/typsphinx/
  - Complete user guide covering installation, quickstart, configuration, builders, and templates
  - Extensive examples section with basic and advanced use cases
  - API reference with autodoc integration
  - Contributing guide with development workflow
  - Automated documentation deployment via GitHub Actions
  - HTML documentation built with Sphinx and Furo theme
  - PDF documentation generated using typsphinx itself (dogfooding)
  - PDF artifacts uploaded to GitHub Releases for tagged versions
  - Documentation badge added to README
  - 13 comprehensive documentation pages created

- **Typst Universe Template Support** ([#13](https://github.com/YuSabo90002/typsphinx/issues/13))
  - Full support for Typst Universe templates (charged-ieee, modern-cv, etc.)
  - `typst_template_function` now accepts dictionary format: `{"name": "ieee", "params": {...}}`
  - New `typst_authors` configuration for detailed author information (department, organization, email)
  - Template-specific parameters can be configured directly in `conf.py`
  - Python variable references work naturally in configuration (no special syntax needed)
  - Backward compatibility maintained for all existing configurations
  - Added comprehensive charged-ieee examples demonstrating two approaches:
    - Approach 1: Configuration-based (recommended, simple)
    - Approach 2: Custom template with Typst code (flexible)
  - Added 8 new test cases (4 for dict format, 4 for author details)
  - All 365 tests passing with full backward compatibility

- **Image File Copying Support** ([#38](https://github.com/YuSabo90002/typsphinx/issues/38))
  - Image files referenced in documents are now automatically copied to the output directory
  - Preserves directory structure when copying images
  - Enables successful PDF builds for documents containing images
  - Implemented `post_process_images()` and `copy_image_files()` methods in TypstBuilder
  - Images are copied before PDF compilation in TypstPDFBuilder
  - Added 9 comprehensive test cases covering various scenarios
  - No configuration required - images are copied automatically

- **Table Header Wrapping Support** ([#40](https://github.com/YuSabo90002/typsphinx/issues/40))
  - Table headers now wrapped in `table.header()` for proper Typst rendering
  - Enables automatic header repetition on multi-page tables
  - Provides accessibility metadata for screen readers and assistive technologies
  - Supports multi-row headers (`:header-rows: N` with N > 1)
  - Maintains backward compatibility for tables without headers
  - Added `in_thead` state flag to track header section in translator
  - Modified cell storage to include `is_header` flag
  - Updated `depart_table()` to generate `table.header()` wrapper for header cells
  - Complies with Typst documentation recommendations for table accessibility
  - Added 4 comprehensive test cases covering various header scenarios

- **Table Cell Spanning Support** ([#39](https://github.com/YuSabo90002/typsphinx/issues/39))
  - Added support for horizontal cell spanning (colspan) via `morecols` attribute
  - Added support for vertical cell spanning (rowspan) via `morerows` attribute
  - Cells with spanning now generate `table.cell(colspan: N, rowspan: M)` syntax
  - Supports combined horizontal and vertical spanning in same cell
  - Works correctly with header cells inside `table.header()`
  - Maintains backward compatibility for tables without cell spanning
  - Created `_format_table_cell()` helper method for consistent cell formatting
  - Reads `morecols`/`morerows` attributes in `visit_entry()`
  - Extended cell storage to include `colspan` and `rowspan` fields
  - Added 5 comprehensive test cases covering various spanning scenarios

## [0.3.0] - 2025-10-23

### Changed (Breaking)
- **Package Rename**: `sphinxcontrib-typst` → `typsphinx`
  - Changed to a simpler and more unique name
  - Reflects the nature of this package as a builder
  - PyPI package name: `typsphinx`
  - Python import: `import typsphinx`
  - Sphinx extension name: `extensions = ['typsphinx']`
  - Package structure: `sphinxcontrib/typst/` → `typsphinx/`
  - **Migration steps**:
    1. `pip uninstall sphinxcontrib-typst`
    2. `pip install typsphinx`
    3. Update `conf.py`: `extensions = ['sphinxcontrib.typst']` → `extensions = ['typsphinx']`

### Rationale
- `sphinxcontrib-*` namespace is traditionally for extensions that add directives or roles
- This package is primarily a builder (Sphinx→Typst conversion) and needs a more appropriate name
- Current low user base makes this the optimal timing for the change
- Unique and memorable name that represents the integration of Typst and Sphinx

## [0.2.2] - 2025-10-23

### Added
- **Additional Code Block Options Support** ([#31](https://github.com/YuSabo90002/typsphinx/issues/31))
  - Added support for `:lineno-start:` option to specify starting line number for code blocks
  - Added support for `:dedent:` option (handled automatically by Sphinx during parsing)
  - `:lineno-start:` works with codly's `start` parameter to display custom line numbers
  - Both options work correctly in combination with existing options (`:linenos:`, `:emphasize-lines:`, etc.)
  - Sphinx now supports 6 out of 8 standard code-block directive options (75%)
  - Added 7 comprehensive test cases covering various scenarios

- **Raw Directive Support** ([#25](https://github.com/YuSabo90002/typsphinx/issues/25))
  - Added support for docutils `raw` directive (`.. raw:: typst`)
  - Typst-specific content (`format='typst'`) is passed through to output
  - Other formats (html, latex, etc.) are skipped and logged
  - Format name matching is case-insensitive
  - Implemented `visit_raw()` and `depart_raw()` methods in TypstTranslator
  - Added 6 comprehensive test cases covering various scenarios

### Fixed
- **Code Block Directive Options Support** ([#20](https://github.com/YuSabo90002/typsphinx/issues/20))
  - Fixed `:linenos:` option being ignored - now properly controls line number display in code blocks
  - Fixed `:caption:` and `:name:` options causing "unknown node type: container" warnings
  - Code blocks with `:caption:` now wrapped in `#figure()` with proper caption
  - Code blocks with `:name:` now generate Typst labels for cross-referencing
  - Added `visit_container()` and `depart_container()` methods to handle Sphinx literal-block-wrapper containers
  - Extended `visit_literal_block()` and `depart_literal_block()` to support caption and label generation
  - Modified `visit_caption()` to skip caption text output for captioned code blocks (prevents duplication)
  - Line numbers now disabled by default when `:linenos:` is not specified (via `#codly(number-format: none)`)
  - All four options (`:linenos:`, `:caption:`, `:name:`, `:emphasize-lines:`) now work correctly together
  - Added comprehensive test coverage for all code block option combinations

- **PDF Builder codly Import Missing** ([#28](https://github.com/YuSabo90002/typsphinx/issues/28))
  - Fixed `typstpdf` builder failing with "unknown variable: codly" error
  - Added codly package imports to document-level essential imports in `template_engine.py`
  - Document files now include `#import "@preview/codly:1.3.0": *` and `#import "@preview/codly-languages:0.1.1": *`
  - Enables PDF generation for documents with code blocks (prerequisite for Issue #20)
  - No breaking changes - only adds imports alongside existing mitex/gentle-clues imports

### Documentation
- **README Math Example Fix** ([#33](https://github.com/YuSabo90002/typsphinx/pull/33))
  - Fixed incorrect double-escaped backslashes in math directive example
  - Changed `\\int` to `\int` for correct reStructuredText syntax
  - Helps users write proper reStructuredText files

## [0.2.1] - 2025-10-18

### Fixed
- **Table Content Duplication** ([#19](https://github.com/YuSabo90002/typsphinx/issues/19))
  - Fixed duplicate table content in Typst output where cell content appeared both as plain text and inside `#table()` structure
  - Affects all reStructuredText table formats: list-table, grid table, simple table, csv-table
  - Modified `add_text()` method to route text to `table_cell_content` when inside table cells
  - Modified `depart_table()` to use `self.body.append()` directly for table structure output
  - Added comprehensive test coverage for all table formats

- **RST Comments Rendered as Plain Text** ([#21](https://github.com/YuSabo90002/typsphinx/issues/21))
  - Fixed reStructuredText comments appearing as plain text in Typst output
  - Comments (lines starting with `..`) are now properly skipped during conversion
  - Resolved "unknown node type: comment" warning messages
  - Added `visit_comment()` and `depart_comment()` methods to TypstTranslator
  - Comments are completely omitted from output as intended for source-level documentation

## [0.1.0b1] - 2025-10-13

### Added

#### Core Features
- **Sphinx Builder Integration** (Requirement 1)
  - TypstBuilder registered as standard Sphinx builder
  - Entry point automatic discovery: `sphinx.builders` → `typst = "sphinxcontrib.typst"`
  - Command: `sphinx-build -b typst` and `sphinx-build -b typstpdf`

- **Doctree to Typst Conversion** (Requirement 2)
  - TypstWriter and TypstTranslator for node conversion
  - Support for 70+ standard docutils nodes + 14+ Sphinx addnodes
  - Document structure: sections, paragraphs, lists, tables
  - Inline elements: emphasis, strong, literal, subscript, superscript
  - Admonitions via gentle-clues (`@preview/gentle-clues:1.2.0`):
    - `note` → `#info[]`
    - `warning`/`caution` → `#warning[]`
    - `tip` → `#tip[]`
    - `important` → `#warning(title: "Important")[]`
    - `seealso` → `#info(title: "See Also")[]`

- **Cross-References and Links** (Requirement 3)
  - `nodes.reference` → `#link(url)[text]`
  - `nodes.target` → `<label>`
  - `addnodes.pending_xref` → `#link(<label>)[text]` or `#ref(<label>)`
  - Document and figure cross-references with `numref`
  - Inline references (`nodes.inline` with `xref` class)

- **Mathematical Expressions** (Requirements 4 & 5)
  - **LaTeX math via mitex** (`@preview/mitex:0.2.4`):
    - Block math: `#mitex(\`...\`)`
    - Inline math: `#mi(\`...\`)`
    - Supports LaTeX commands, environments, user-defined macros
  - **Native Typst math**:
    - Block: `$ ... $` with labeled equations
    - Inline: `$...$`
    - Typst-specific functions: `cal()`, `bb()`, `subset.eq`, etc.
  - **Fallback mode**: Basic LaTeX→Typst conversion when `typst_use_mitex = False`

- **Images and Figures** (Requirement 6)
  - `nodes.image` → `#image("path")`
  - `nodes.figure` → `#figure()` with captions
  - `nodes.table` → `#table()` with headers and rows
  - Figure/table labels and cross-references

- **Code Highlighting** (Requirement 7)
  - **Codly integration** (`@preview/codly:1.3.0` + `@preview/codly-languages:0.1.1`):
    - Automatic line numbering for all code blocks
    - Syntax highlighting for 50+ languages
    - Highlight specific lines via `#codly-range(highlight: (...))`
    - Language-specific icons and colors

- **Template System** (Requirement 8)
  - TemplateEngine for Typst template management
  - Default template with project metadata integration
  - Custom template support via `typst_template` config
  - Template parameter mapping: `typst_template_mapping`
  - Sphinx metadata → template parameters (title, authors, date, etc.)
  - Support for Typst Universe packages

- **Self-Contained PDF Generation** (Requirement 9)
  - TypstPDFBuilder using typst-py (PyPI: `typst>=0.11.1`)
  - No external Typst CLI required
  - Command: `sphinx-build -b typstpdf`
  - Automatic .typ → .pdf conversion
  - Platform support: Linux, macOS, Windows

- **Error Handling and Logging** (Requirement 10)
  - Sphinx logger integration with warning/error levels
  - Unknown node fallback with warnings
  - Template/resource error handling
  - PDF compilation error reporting (`TypstCompilationError`)

- **Multi-Document Integration** (Requirement 13)
  - Each .rst → independent .typ file
  - `toctree` → `#include()` directives
  - Heading level adjustment: `#set heading(offset: 1)`
  - `#outline()` managed in templates (not in document body)
  - Toctree options → template parameters:
    - `:maxdepth:` → `toctree_maxdepth`
    - `:numbered:` → `toctree_numbered`
    - `:caption:` → `toctree_caption`

#### Configuration Options
- `typst_use_mitex`: Enable/disable mitex for LaTeX math (default: `True`)
- `typst_template`: Custom template path
- `typst_elements`: Template parameters (paper size, fonts, etc.)
- `typst_template_mapping`: Sphinx metadata to template parameter mapping
- `typst_toctree_defaults`: Default toctree options
- `typst_package`: External Typst Universe package
- `typst_package_imports`: Package imports
- `typst_template_function`: Template function name
- `typst_output_dir`: Output directory structure
- `typst_debug`: Debug mode

#### Documentation and Examples
- Installation guide: `docs/installation.rst`
- Usage guide: `docs/usage.rst` (600+ lines)
- Configuration reference: `docs/configuration.rst` (400+ lines, 11 config values)
- Basic example: `examples/basic/`
- Advanced example: `examples/advanced/` (toctree, LaTeX math, code, tables)

#### Testing and Quality Assurance
- **286 tests** with **93% code coverage**:
  - Unit tests: builder, translator, template engine, PDF generation
  - Integration tests: basic, multi-document, advanced features
  - Documentation tests: installation, configuration, usage
  - Example tests: basic and advanced examples
- **Multi-version testing** via tox:
  - Python 3.9, 3.10, 3.11, 3.12
  - tox environments: py39, py310, py311, py312, lint, type, cov
- **CI/CD pipeline** (GitHub Actions):
  - Test matrix: 3 OSes × 4 Python versions
  - Lint (black, ruff), type check (mypy)
  - Code coverage reporting (Codecov)
  - Package build validation (twine check)
- **Code quality tools**:
  - black (code formatting)
  - ruff (linting)
  - mypy (type checking)

### Known Limitations

- **Requirement 11** (Extensibility and Plugin Support): Custom node handler registry not yet implemented
  - Planned for v0.2.0
  - Workaround: Extend TypstTranslator directly
- **Bibliography**: BibTeX integration not yet supported
- **Glossary**: Glossary generation not yet supported
- **Index**: Index generation not yet supported

### Technical Details

#### Requirements Fulfilled
- ✅ Requirement 1: Sphinx Builder Integration (100%)
- ✅ Requirement 2: Doctree to Typst Conversion (100%)
- ✅ Requirement 3: Cross-References and Links (100%)
- ✅ Requirement 4: Math Support (mitex) (100%)
- ✅ Requirement 5: Typst Native Math (100%)
- ✅ Requirement 6: Figures and Tables (100%)
- ✅ Requirement 7: Code Highlighting (100%)
- ✅ Requirement 8: Templates and Customization (100%)
- ✅ Requirement 9: Self-Contained PDF Generation (100%)
- ✅ Requirement 10: Error Handling and Logging (100%)
- ⏳ Requirement 11: Extensibility (Planned for v0.2.0)
- ✅ Requirement 12: Testing and Documentation (100%)
- ✅ Requirement 13: Multi-Document Integration (100%)

**Total: 12 out of 13 requirements fully implemented**

#### Dependencies
- Python: ≥3.9
- Sphinx: ≥5.0
- docutils: ≥0.18
- typst (typst-py): ≥0.11.1

#### Typst Packages Used
- `@preview/mitex:0.2.4`: LaTeX math rendering
- `@preview/codly:1.3.0`: Code syntax highlighting
- `@preview/codly-languages:0.1.1`: Language definitions
- `@preview/gentle-clues:1.2.0`: Admonition styling

### Development Tools
- **uv**: Fast package management and dependency resolution
- **pytest**: Testing framework (286 tests)
- **tox**: Multi-version testing automation
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking
- **sphinx-testing**: Sphinx extension testing helpers

---

## [0.2.0] - 2025-10-16

### Fixed

- **Issue #5**: Fixed nested toctree relative path issues in `#include()` directives (PR #14)
  - Corrected relative path calculation for nested toctree structures
  - Added comprehensive debug logging for path resolution
  - Added E2E Typst compilation tests and integration tests
  - Improved code coverage to 94%

- **Issue #10**: Fixed typstpdf builder auto-discovery (PR #12)
  - Registered `typstpdf` builder in `entry_points` for automatic Sphinx discovery
  - Updated documentation to reflect optional extension registration
  - Added test coverage for typstpdf entry point

### Improved

- **Issue #7**: Simplified toctree output format (PR #15)
  - Changed from multiple `#block(breakable: true)[]` to single content block
  - Improved readability and maintainability of generated Typst code
  - Resolved lint and format errors in test files

### Documentation

- **Issue #6**: Documented custom node support using Sphinx standard API (PR #16)
  - Added "Working with Third-Party Extensions" section to README.md
  - Documented usage of Sphinx's standard `app.add_node()` API
  - Provided practical example with sphinxcontrib-mermaid integration
  - Clarified that NodeHandlerRegistry is unnecessary - Sphinx already provides this functionality
  - **Requirement 11 is now complete**: Custom node support via Sphinx's standard extension mechanism

- **Issue #8**: Added acknowledgment for AI-assisted development (PR #9)
  - Added Claude Code and Kiro-style Spec-Driven Development to acknowledgments

- **PR #11**: Improved CLAUDE.md with repository information and guidelines
  - Added repository owner and URL information
  - Added language guidelines for GitHub interactions
  - Added issue template references

### Dependencies

- **Dependabot updates**:
  - Bump astral-sh/setup-uv from 4 to 7 (PR #1)
  - Bump actions/checkout from 4 to 5 (PR #2)
  - Bump codecov/codecov-action from 4 to 5 (PR #3)

### Requirements Status

**All 13 requirements now fully implemented**:
- ✅ Requirement 1: Sphinx Builder Integration (100%)
- ✅ Requirement 2: Doctree to Typst Conversion (100%)
- ✅ Requirement 3: Cross-References and Links (100%)
- ✅ Requirement 4: Math Support (mitex) (100%)
- ✅ Requirement 5: Typst Native Math (100%)
- ✅ Requirement 6: Figures and Tables (100%)
- ✅ Requirement 7: Code Highlighting (100%)
- ✅ Requirement 8: Templates and Customization (100%)
- ✅ Requirement 9: Self-Contained PDF Generation (100%)
- ✅ Requirement 10: Error Handling and Logging (100%)
- ✅ Requirement 11: Extensibility and Plugin Support (100%) - **Now complete**
- ✅ Requirement 12: Testing and Documentation (100%)
- ✅ Requirement 13: Multi-Document Integration (100%)

### Testing

- **317 tests** with **94% code coverage**
- All tests passing across Python 3.9, 3.10, 3.11, 3.12
- CI/CD pipeline validated on Linux, macOS, Windows

---

## [Unreleased]

### Planned for Future Releases
- BibTeX/bibliography support
- Glossary generation
- Index generation
- Pre-commit hooks
- Additional Typst Universe template integration

---

[0.2.0]: https://github.com/YuSabo90002/typsphinx/releases/tag/v0.2.0
[0.1.0b1]: https://github.com/YuSabo90002/typsphinx/releases/tag/v0.1.0b1
[Unreleased]: https://github.com/YuSabo90002/typsphinx/compare/v0.2.0...HEAD
