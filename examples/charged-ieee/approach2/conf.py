# Configuration file for charged-ieee example (Approach 2)
# Approach 2: Use custom template with Typst code for transformation (Flexible)

import os
import sys

# -- Project information -----------------------------------------------------
project = "Machine Learning Applications in Computer Vision"
copyright = "2025, John Doe"
author = "John Doe"
release = "1.0"

# -- General configuration ---------------------------------------------------
extensions = ["typsphinx"]

# -- Typst output options ----------------------------------------------------
typst_documents = [
    ("index", "paper", project, author, "typst"),
]

# -- Typst Universe package configuration ------------------------------------
# Use charged-ieee template from Typst Universe
typst_package = "@preview/charged-ieee:0.1.4"

# -- Custom template configuration (Approach 2 - Flexible) ------------------
# Use custom template that wraps charged-ieee
typst_template = "_templates/_template.typ"
typst_template_function = "project"
