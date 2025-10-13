# Configuration file for the Sphinx documentation builder.
#
# This is a basic example of using sphinxcontrib-typst to generate
# Typst output from Sphinx documentation.

# -- Project information -----------------------------------------------------

project = "Basic Sphinx-Typst Example"
copyright = "2024, Sphinx-Typst Contributors"
author = "Sphinx-Typst Contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinxcontrib.typst",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]

# -- Options for Typst output ------------------------------------------------

# Define documents to be built as Typst files
typst_documents = [
    (
        "index",
        "basic-example.typ",
        "Basic Sphinx-Typst Example",
        "Sphinx-Typst Contributors",
    ),
]

# Use mitex for LaTeX math (default: True)
typst_use_mitex = True

# Custom elements (optional)
typst_elements = {
    # You can customize Typst template parameters here
}
