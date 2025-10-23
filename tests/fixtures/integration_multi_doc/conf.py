# Sphinx configuration for multi-document integration testing

project = "Multi-Document Test"
author = "Test Author"
release = "1.0.0"

extensions = [
    "typsphinx",
]

typst_documents = [
    ("index", "index.typ", "Multi-Document Test", "Test Author"),
]
