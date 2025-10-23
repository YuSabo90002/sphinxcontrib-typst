# Sphinx configuration for Issue #5 reproduction test
# Tests nested toctree with relative path generation

project = "Nested Toctree Test"
author = "Test Author"
release = "1.0.0"

extensions = [
    "typsphinx",
]

# Typst configuration
typst_documents = [
    ("index", "index.typ", "Nested Toctree Test", "Test Author"),
]
