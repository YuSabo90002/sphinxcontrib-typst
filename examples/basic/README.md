# Basic Sphinx-Typst Example

This is a basic example project demonstrating how to use `sphinxcontrib-typst` to generate Typst output from Sphinx documentation.

## Prerequisites

- Python 3.9 or higher
- Sphinx 5.0 or higher
- sphinxcontrib-typst installed

## Installation

If you haven't installed sphinxcontrib-typst yet:

```bash
pip install sphinxcontrib-typst
```

Or install from source:

```bash
cd /path/to/sphinxcontrib-typst
pip install -e .
```

## Building the Documentation

### Generate Typst Output

To build the documentation and generate `.typ` files:

```bash
sphinx-build -b typst . _build/typst
```

This will create `_build/typst/basic-example.typ` with the Typst markup.

### Generate PDF Output

To directly generate PDF output using typst-py:

```bash
sphinx-build -b typstpdf . _build/pdf
```

This will create both `.typ` and `.pdf` files in `_build/pdf/`.

### Alternative: Manual PDF Generation

If you have the Typst CLI installed, you can also compile the `.typ` file manually:

```bash
# First generate Typst output
sphinx-build -b typst . _build/typst

# Then compile with Typst CLI
typst compile _build/typst/basic-example.typ output.pdf
```

## Project Structure

```
basic/
├── conf.py          # Sphinx configuration
├── index.rst        # Main document
├── README.md        # This file
└── _build/          # Build output (generated)
    ├── typst/       # Typst markup files
    └── pdf/         # PDF files (if using typstpdf builder)
```

## Configuration

The `conf.py` file contains the Sphinx configuration, including:

- `extensions = ['sphinxcontrib.typst']` - Enables the Typst builder
- `typst_documents` - Defines which documents to build as Typst files
- `typst_use_mitex` - Enables mitex for LaTeX math support (default: True)

## Features Demonstrated

This example demonstrates:

- Basic text formatting (bold, italic, inline code)
- Lists (ordered and unordered)
- Code blocks with syntax highlighting
- Mathematics (inline and block equations)
- Tables
- Cross-references and links

## Next Steps

For more advanced features, check out:

- `examples/advanced/` - Advanced features like toctree, custom templates, etc.
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Typst Documentation](https://typst.app/docs/)
- [sphinxcontrib-typst Documentation](https://sphinxcontrib-typst.readthedocs.io/)

## Troubleshooting

### Build Fails with "No module named 'sphinxcontrib.typst'"

Make sure sphinxcontrib-typst is installed in your current Python environment:

```bash
pip install sphinxcontrib-typst
```

### Typst Compilation Errors

If you encounter Typst compilation errors, check:

1. The generated `.typ` file for syntax errors
2. Your Typst version is up to date
3. Required Typst packages (codly, mitex) are available

## Support

For issues and questions:

- GitHub Issues: https://github.com/your-repo/sphinxcontrib-typst/issues
- Documentation: https://sphinxcontrib-typst.readthedocs.io/
