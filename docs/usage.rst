=====
Usage
=====

This guide covers common usage patterns and workflows for typsphinx.

Quick Start
===========

Basic Setup
-----------

1. **Install typsphinx**:

   .. code-block:: bash

      pip install typsphinx

2. **Configure Typst output** (``conf.py``):

   .. note::

      typsphinx builders are automatically discovered via entry points.
      Adding to ``extensions`` list is optional but recommended for clarity.

   .. code-block:: python

      # Optional: explicit extension loading
      # extensions = ['sphinxcontrib.typst']

      typst_documents = [
          ('index', 'output.typ', 'My Document', 'Author Name'),
      ]

3. **Build Typst output**:

   .. code-block:: bash

      sphinx-build -b typst source/ build/typst

That's it! You now have Typst files in ``build/typst/``.

Basic Workflow
==============

Step-by-Step Guide
------------------

1. Create or Update Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Write your documentation using standard reStructuredText:

.. code-block:: rst

   My Project
   ==========

   Welcome to my project documentation.

   Features
   --------

   * Feature 1
   * Feature 2

   Code Example
   ------------

   .. code-block:: python

      def hello():
          print("Hello, World!")

2. Configure Typst Output
~~~~~~~~~~~~~~~~~~~~~~~~~~

Edit ``conf.py`` to specify what documents to build:

.. code-block:: python

   # Basic configuration
   typst_documents = [
       ('index', 'manual.typ', 'User Manual', 'Development Team'),
   ]

   # Optional: Use custom template
   typst_template = '_templates/custom.typ'

   # Optional: Customize appearance
   typst_elements = {
       'papersize': 'a4',
       'fontsize': '11pt',
   }

3. Build Typst Files
~~~~~~~~~~~~~~~~~~~~

Use the Typst builder:

.. code-block:: bash

   sphinx-build -b typst source/ build/typst

This creates ``.typ`` files in ``build/typst/``.

4. Generate PDF (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have Typst CLI installed, compile to PDF:

.. code-block:: bash

   typst compile build/typst/manual.typ output.pdf

Or use the PDF builder directly:

.. code-block:: bash

   sphinx-build -b typstpdf source/ build/pdf

Common Use Cases
================

Single Document Project
-----------------------

For simple projects with one main document:

**conf.py:**

.. code-block:: python

   # Optional: explicit extension loading
   # extensions = ['sphinxcontrib.typst']

   typst_documents = [
       ('index', 'documentation.typ', project, author),
   ]

**Build:**

.. code-block:: bash

   sphinx-build -b typst . _build/typst

Multi-Document Project
----------------------

For projects with multiple chapters or sections:

**conf.py:**

.. code-block:: python

   typst_documents = [
       ('index', 'complete.typ', 'Complete Manual', 'Team'),
       ('quickstart', 'quickstart.typ', 'Quick Start Guide', 'Team'),
       ('api', 'api-reference.typ', 'API Reference', 'Team'),
   ]

**index.rst with toctree:**

.. code-block:: rst

   .. toctree::
      :maxdepth: 2
      :numbered:

      quickstart
      user-guide
      api-reference

The toctree is converted to Typst ``#include()`` directives.

API Documentation
-----------------

For Python projects with autodoc:

**conf.py:**

.. code-block:: python

   extensions = [
       # 'sphinxcontrib.typst',  # Optional: auto-discovered via entry points
       'sphinx.ext.autodoc',
       'sphinx.ext.napoleon',
   ]

   typst_documents = [
       ('index', 'api-docs.typ', f'{project} API', author),
   ]

**index.rst:**

.. code-block:: rst

   API Reference
   =============

   .. automodule:: mypackage
      :members:
      :undoc-members:
      :show-inheritance:

Mathematical Documentation
--------------------------

For documents with equations:

**conf.py:**

.. code-block:: python

   # Enable LaTeX math via mitex
   typst_use_mitex = True

**document.rst:**

.. code-block:: rst

   Mathematical Concepts
   =====================

   The quadratic formula:

   .. math::
      :label: quadratic

      x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

   See equation :eq:`quadratic` for details.

Custom Templates
----------------

To use a custom Typst template:

1. Create template file (``_templates/custom.typ``):

   .. code-block:: typst

      #let project(title: "", authors: (), body) = {
        set page(paper: "a4", margin: 2.5cm)
        set text(font: "Linux Libertine", size: 11pt)

        // Title page
        align(center)[
          #text(size: 24pt, weight: "bold")[#title]
          #v(1em)
          #text(size: 14pt)[#authors.join(", ")]
        ]

        pagebreak()

        // Content
        body
      }

2. Reference in ``conf.py``:

   .. code-block:: python

      typst_template = '_templates/custom.typ'

3. Build as usual:

   .. code-block:: bash

      sphinx-build -b typst source/ build/typst

Continuous Integration
----------------------

For CI/CD pipelines:

**GitHub Actions example** (``.github/workflows/docs.yml``):

.. code-block:: yaml

   name: Build Documentation

   on: [push, pull_request]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v3

         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             pip install sphinx typsphinx

         - name: Build Typst documentation
           run: |
             sphinx-build -b typst docs/ build/typst

         - name: Upload artifacts
           uses: actions/upload-artifact@v3
           with:
             name: typst-docs
             path: build/typst/

Build Commands Reference
=========================

Basic Commands
--------------

Build Typst files
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -b typst source/ build/typst

Build PDF directly
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -b typstpdf source/ build/pdf

Rebuild all files
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -a -b typst source/ build/typst

Clean build
~~~~~~~~~~~

.. code-block:: bash

   rm -rf build/
   sphinx-build -b typst source/ build/typst

Verbose output
~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -v -b typst source/ build/typst

Advanced Options
----------------

Specify config file
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -c path/to/config -b typst source/ build/typst

Parallel build
~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -j auto -b typst source/ build/typst

Warnings as errors
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sphinx-build -W -b typst source/ build/typst

Best Practices
==============

Project Structure
-----------------

Organize your Sphinx project:

.. code-block:: text

   myproject/
   ├── docs/
   │   ├── conf.py
   │   ├── index.rst
   │   ├── chapter1.rst
   │   ├── chapter2.rst
   │   ├── _static/
   │   │   └── images/
   │   └── _templates/
   │       └── custom.typ
   ├── src/
   │   └── mypackage/
   └── README.md

Configuration Management
------------------------

**Keep configuration organized:**

.. code-block:: python

   # conf.py

   # Project info
   project = 'My Project'
   author = 'Development Team'
   release = '1.0.0'

   # Extensions
   extensions = [
       # 'sphinxcontrib.typst',  # Optional: auto-discovered via entry points
       'sphinx.ext.autodoc',
   ]

   # Typst configuration
   typst_documents = [
       ('index', 'documentation.typ', project, author),
   ]

   typst_use_mitex = True

   typst_elements = {
       'papersize': 'a4',
       'fontsize': '11pt',
   }

Version Control
---------------

**.gitignore:**

.. code-block:: text

   # Build output
   _build/
   build/

   # Sphinx cache
   .doctrees/

   # Python
   __pycache__/
   *.pyc

Document Organization
---------------------

1. **Use toctree** for multi-document projects
2. **Keep files focused** - one topic per file
3. **Use labels** for cross-references
4. **Include index** in each section

Troubleshooting
===============

Common Issues
-------------

Build Fails
~~~~~~~~~~~

**Problem:** ``sphinx-build`` command fails.

**Solutions:**

- Verify typsphinx is installed:

  .. code-block:: bash

     pip list | grep typsphinx

- Check conf.py syntax:

  .. code-block:: bash

     python -m py_compile docs/conf.py

- Run with verbose output:

  .. code-block:: bash

     sphinx-build -v -b typst docs/ build/typst

Empty Output
~~~~~~~~~~~~

**Problem:** Build succeeds but no .typ files generated.

**Solutions:**

- Check ``typst_documents`` is configured in conf.py
- Verify source files exist
- Ensure builder name is ``typst`` (not ``html``)

PDF Generation Fails
~~~~~~~~~~~~~~~~~~~~

**Problem:** ``sphinx-build -b typstpdf`` fails.

**Solutions:**

- Verify Typst CLI is installed:

  .. code-block:: bash

     typst --version

- Install typst Python package:

  .. code-block:: bash

     pip install typst

- Check generated .typ file for syntax errors

Math Not Rendering
~~~~~~~~~~~~~~~~~~

**Problem:** LaTeX math expressions don't appear correctly.

**Solutions:**

- Enable mitex in conf.py:

  .. code-block:: python

     typst_use_mitex = True

- Verify mitex package is available in Typst
- Check math syntax is valid LaTeX

Cross-References Broken
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Internal links don't work.

**Solutions:**

- Use proper reference syntax: ``:ref:`label```
- Ensure labels are defined: ``.. _label:``
- Check label names match exactly (case-sensitive)

Getting Help
------------

If you encounter issues:

1. **Check documentation**: Review :doc:`configuration` and examples
2. **Search GitHub issues**: https://github.com/your-repo/typsphinx/issues
3. **Enable debug mode**: Set ``typst_debug = True`` in conf.py
4. **Ask for help**: Create a GitHub issue with minimal reproduction

Examples and Templates
======================

The ``examples/`` directory contains working projects:

- **examples/basic/**: Simple single-document project
- **examples/advanced/**: Multi-document with custom template

To try an example:

.. code-block:: bash

   cd examples/basic
   sphinx-build -b typst . _build/typst
   ls _build/typst/

See Also
========

Related Documentation
---------------------

- :doc:`installation` - Installation guide
- :doc:`configuration` - Complete configuration reference
- `Sphinx Documentation <https://www.sphinx-doc.org/>`_ - Official Sphinx docs
- `Typst Documentation <https://typst.app/docs/>`_ - Official Typst docs

Example Projects
----------------

Check the ``examples/`` directory for:

- Basic usage patterns
- Advanced features
- Custom templates
- Multi-document projects

Next Steps
==========

Now that you're familiar with basic usage:

1. **Explore advanced features** in :doc:`configuration`
2. **Try the examples** in ``examples/`` directory
3. **Customize templates** for your project
4. **Integrate with CI/CD** for automated builds

Happy documenting with typsphinx!
