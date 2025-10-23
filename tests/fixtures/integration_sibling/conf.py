# Sphinx configuration for sibling directory toctree test
# Tests cross-directory references between sibling directories

project = "Sibling Directory Toctree Test"
author = "Test Author"
release = "1.0.0"

extensions = [
    "typsphinx",
]

# Typst configuration
typst_documents = [
    ("index", "index.typ", "Sibling Directory Test", "Test Author"),
]
