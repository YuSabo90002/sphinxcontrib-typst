"""
Test configuration for typsphinx extension.
"""

extensions = ["typsphinx"]

project = "Test Project"
author = "Test Author"
copyright = "2025, Test Author"

# Typst builder configuration
typst_documents = [
    ("index", "output.typ", "Test Document", "Test Author"),
]
