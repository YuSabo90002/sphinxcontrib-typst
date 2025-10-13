# Sphinx configuration for math and figures integration testing

project = "Math and Figures Test"
author = "Test Author"
release = "1.0.0"

extensions = [
    "sphinxcontrib.typst",
]

typst_documents = [
    ("index", "index.typ", "Math and Figures Test", "Test Author"),
]

# Enable both mitex and native math
typst_use_mitex = True
