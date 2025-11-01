Quick Start
===========

This guide will help you get started with typsphinx in just a few minutes.

Basic Setup
-----------

1. **Install typsphinx** (if you haven't already):

   .. code-block:: bash

      pip install typsphinx

2. **Add to your Sphinx project**

   Add ``typsphinx`` to the ``extensions`` list in your ``conf.py``:

   .. code-block:: python

      extensions = [
          "typsphinx",
      ]

   .. note::

      Thanks to entry points, adding to ``extensions`` is optional.
      The builders are automatically discovered.

3. **Build Typst output**:

   .. code-block:: bash

      # Generate Typst markup
      sphinx-build -b typst source/ build/typst

      # Or generate PDF directly
      sphinx-build -b typstpdf source/ build/pdf

Your First PDF
--------------

Here's a minimal example to generate your first PDF:

1. Create a simple ``index.rst``:

   .. code-block:: rst

      Welcome to My Documentation
      ===========================

      This is a sample document.

      Features
      --------

      - Easy to use
      - Beautiful PDFs
      - Fast compilation

2. Build the PDF:

   .. code-block:: bash

      sphinx-build -b typstpdf source/ build/pdf

3. Find your PDF in ``build/pdf/index.pdf``!

Configuration Options
---------------------

You can customize the output by adding options to ``conf.py``:

.. code-block:: python

   # Project information
   project = "My Project"
   author = "Your Name"
   release = "1.0.0"

   # Typst configuration
   typst_documents = [
       ("index", "myproject", project, author, "typst"),
   ]

   # Use mitex for LaTeX math
   typst_use_mitex = True

   # Custom template (optional)
   typst_template = "_templates/custom.typ"

What's Next?
------------

- Learn about :doc:`user_guide/configuration` options
- Explore :doc:`user_guide/builders` (typst vs typstpdf)
- Customize with :doc:`user_guide/templates`
- See :doc:`examples/index` for more examples
