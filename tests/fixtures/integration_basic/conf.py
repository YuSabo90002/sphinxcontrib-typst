# Minimal Sphinx configuration for integration testing

project = "Integration Test Project"
author = "Test Author"
release = "1.0.0"

extensions = [
    "sphinxcontrib.typst",
]

# Minimal Typst configuration
typst_documents = [
    ("index", "index.typ", "Integration Test", "Test Author"),
]
