# Sphinx configuration for multi-level nested toctree test
# Tests 3-level directory structure (root → part1 → chapter1)

project = "Multi-Level Toctree Test"
author = "Test Author"
release = "1.0.0"

extensions = [
    "sphinxcontrib.typst",
]

# Typst configuration
typst_documents = [
    ("index", "index.typ", "Multi-Level Toctree Test", "Test Author"),
]
