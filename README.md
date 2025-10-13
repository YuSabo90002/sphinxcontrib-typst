# sphinxcontrib-typst

[![PyPI version](https://badge.fury.io/py/sphinxcontrib-typst.svg)](https://badge.fury.io/py/sphinxcontrib-typst)
[![Python Support](https://img.shields.io/pypi/pyversions/sphinxcontrib-typst.svg)](https://pypi.org/project/sphinxcontrib-typst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sphinx extension for Typst output format support.

## Overview

sphinxcontrib-typst is a Sphinx extension that enables generating Typst documents from reStructuredText sources. Typst is a modern typesetting system designed as an alternative to LaTeX, offering faster compilation and a more intuitive syntax.

## Features

- **Convert Sphinx documentation to Typst format**: Seamlessly transform your reStructuredText/Markdown documents
- **Standard docutils nodes**: Full support for paragraphs, sections, lists, tables, admonitions, and more
- **Mathematical expressions**:
  - LaTeX syntax via mitex (`@preview/mitex:0.2.4`)
  - Native Typst math syntax
- **Code blocks with syntax highlighting**: Using codly package (`@preview/codly:1.3.0`)
  - Automatic line numbering
  - Syntax highlighting for multiple languages
  - Highlight specific lines
- **Images and figures**: Embed images with captions and references
- **Cross-references and citations**: Maintain document structure with internal links
- **Customizable templates**: Use default or custom Typst templates
- **Direct PDF generation**: Self-contained PDF generation via typst-py (no external Typst CLI required)
- **Multi-document support**: Generate multiple Typst files with toctree integration using `#include()`

## Requirements

- Python 3.9 or higher
- Sphinx 5.0 or higher
- typst-py 0.11.1 or higher

## Installation

### From PyPI (Beta Release)

```bash
pip install sphinxcontrib-typst
```

### Using uv (recommended for development)

```bash
# Clone the repository
git clone https://github.com/YuSabo90002/sphinxcontrib-typst.git
cd sphinxcontrib-typst

# Install dependencies with uv
uv sync

# For development dependencies
uv sync --extra dev
```

## Quick Start

### Basic Configuration

Add `sphinxcontrib.typst` to your `conf.py`:

```python
# conf.py
extensions = [
    'sphinxcontrib.typst',
]

# Optional: Configure Typst builder
typst_use_mitex = True  # Use mitex for LaTeX math (default: True)
```

### Build Typst Output

```bash
# Generate Typst files
sphinx-build -b typst source build/typst

# Generate PDF directly
sphinx-build -b typstpdf source build/pdf
```

### Example Document

Create a simple reStructuredText document:

```rst
==============
My Document
==============

This is a paragraph with **bold** and *italic* text.

Math Example
============

Inline math: :math:`E = mc^2`

Block math:

.. math::

   \\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}

Code Example
============

.. code-block:: python

   def hello_world():
       print("Hello, Typst!")
```

This will generate a Typst file with:
- Proper heading hierarchy
- Formatted text with emphasis
- LaTeX math via mitex (or native Typst math)
- Syntax-highlighted code blocks with codly

## Advanced Usage

### Custom Templates

Create a custom Typst template:

```python
# conf.py
typst_template = '_templates/custom.typ'

typst_elements = {
    'papersize': 'a4',
    'fontsize': '11pt',
    'lang': 'ja',
}
```

### Template Parameter Mapping

Map Sphinx metadata to template parameters:

```python
# conf.py
typst_template_mapping = {
    'title': 'project',
    'authors': ['author'],
    'date': 'release',
}
```

### Multi-Document Projects

Use toctree to combine multiple documents:

```rst
.. toctree::
   :maxdepth: 2
   :numbered:

   intro
   chapter1
   chapter2
```

This generates `#include()` directives in Typst with proper heading level adjustments.

## Configuration Options

See [docs/configuration.rst](docs/configuration.rst) for all available configuration options:

- `typst_use_mitex`: Enable/disable mitex for LaTeX math
- `typst_template`: Custom template path
- `typst_elements`: Template parameters (paper size, fonts, etc.)
- `typst_template_mapping`: Sphinx metadata to template parameter mapping
- `typst_toctree_defaults`: Default toctree options

## Development

This project uses uv for fast package management and follows TDD (Test-Driven Development) practices.

### Setup Development Environment

```bash
# Install with development dependencies
uv sync --extra dev

# Run tests (286 tests, 93% coverage)
uv run pytest

# Run tests with coverage report
uv run pytest --cov=sphinxcontrib.typst --cov-report=html

# Run tests across multiple Python versions
uv run tox

# Run linters
uv run black .
uv run ruff check .
uv run mypy sphinxcontrib/
```

### Testing Strategy

- **Unit tests**: 286 tests covering all major components
- **Integration tests**: Full build process validation
- **Example projects**: `examples/basic/` and `examples/advanced/`
- **Code coverage**: 93% overall

### Project Structure

```
sphinxcontrib-typst/
├── sphinxcontrib/typst/    # Main package
│   ├── builder.py          # Typst builder
│   ├── writer.py           # Doctree writer
│   ├── translator.py       # Node translator
│   ├── template_engine.py  # Template processor
│   ├── pdf.py              # PDF generation
│   └── templates/          # Default templates
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/               # Example projects
└── pyproject.toml          # Project configuration
```

## Known Limitations (v0.1.0b1)

- **Requirement 11** (Extensibility and Plugin Support): Custom node handler registry not yet implemented (planned for v0.2.0)
- **Bibliography**: BibTeX integration not yet supported
- **Glossary**: Glossary generation not yet supported

See full requirements verification in project documentation.

## Documentation

- [Installation Guide](docs/installation.rst)
- [Usage Guide](docs/usage.rst)
- [Configuration Reference](docs/configuration.rst)
- [Examples](examples/)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass: `uv run pytest`
5. Submit a pull request

### Development Guidelines

- Follow TDD (Test-Driven Development)
- Maintain 80%+ code coverage
- Use black for code formatting
- Follow Sphinx extension conventions
- Add tests for all new features

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [Sphinx](https://www.sphinx-doc.org/)
- Uses [Typst](https://typst.app/) for typesetting
- Integrates [mitex](https://github.com/mitex-rs/mitex) for LaTeX math
- Uses [codly](https://typst.app/universe/package/codly) for code highlighting
- Uses [gentle-clues](https://typst.app/universe/package/gentle-clues) for admonitions

## Version History

### v0.1.0b1 (Beta Release)

Initial beta release with:
- 12 out of 13 requirements fully implemented
- 286 tests passing (93% coverage)
- Support for Typst output generation
- Self-contained PDF generation
- Multi-document support with toctree
- LaTeX math via mitex
- Code highlighting via codly
- Admonition support via gentle-clues

---

**Status**: Beta (v0.1.0b1) - Suitable for testing and early adoption
**Python**: 3.9+ | **Sphinx**: 5.0+ | **Typst**: 0.11.1+
