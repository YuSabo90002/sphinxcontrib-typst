# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Table Content Duplication** ([#19](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/19))
  - Fixed duplicate table content in Typst output where cell content appeared both as plain text and inside `#table()` structure
  - Affects all reStructuredText table formats: list-table, grid table, simple table, csv-table
  - Modified `add_text()` method to route text to `table_cell_content` when inside table cells
  - Modified `depart_table()` to use `self.body.append()` directly for table structure output
  - Added comprehensive test coverage for all table formats

- **RST Comments Rendered as Plain Text** ([#21](https://github.com/YuSabo90002/sphinxcontrib-typst/issues/21))
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

[0.2.0]: https://github.com/YuSabo90002/sphinxcontrib-typst/releases/tag/v0.2.0
[0.1.0b1]: https://github.com/YuSabo90002/sphinxcontrib-typst/releases/tag/v0.1.0b1
[Unreleased]: https://github.com/YuSabo90002/sphinxcontrib-typst/compare/v0.2.0...HEAD
