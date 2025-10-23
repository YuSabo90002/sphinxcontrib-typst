============
Installation
============

This guide explains how to install typsphinx and its dependencies.

Requirements
============

System Requirements
-------------------

typsphinx requires the following software:

- **Python**: Version 3.9 or higher
- **Sphinx**: Version 5.0 or higher
- **Operating Systems**: Linux, macOS, Windows

Python Dependencies
-------------------

The following Python packages will be installed automatically:

- ``sphinx`` (>=5.0) - Documentation generator
- ``docutils`` (>=0.18) - Document processing system
- ``typst`` (>=0.11.1) - Typst compiler Python bindings for PDF generation

Optional Dependencies
---------------------

For development and testing:

- ``pytest`` (>=7.0) - Testing framework
- ``pytest-cov`` (>=4.0) - Code coverage reporting
- ``black`` (>=23.0) - Code formatter
- ``ruff`` (>=0.1.0) - Python linter
- ``mypy`` (>=1.0) - Static type checker

Installation Methods
====================

Using pip (Recommended for Users)
----------------------------------

The simplest way to install typsphinx is using pip:

.. code-block:: bash

   pip install typsphinx

This will install typsphinx and all required dependencies.

Using pip with Optional Dependencies
-------------------------------------

To install with development tools:

.. code-block:: bash

   pip install typsphinx[dev]

To install with documentation building tools:

.. code-block:: bash

   pip install typsphinx[docs]

Using uv (Recommended for Developers)
--------------------------------------

For faster package management and development, use `uv <https://github.com/astral-sh/uv>`_:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/typsphinx.git
      cd typsphinx

2. Install dependencies with uv:

   .. code-block:: bash

      uv sync

3. For development with all optional dependencies:

   .. code-block:: bash

      uv sync --extra dev

Installing from Source
----------------------

To install from source using pip:

.. code-block:: bash

   git clone https://github.com/yourusername/typsphinx.git
   cd typsphinx
   pip install -e .

The ``-e`` flag installs the package in "editable" mode, which is useful for development.

Verifying Installation
======================

After installation, verify that typsphinx is available:

.. code-block:: bash

   python -c "import sphinxcontrib.typst; print('typsphinx installed successfully')"

You can also check the Sphinx builders available:

.. code-block:: bash

   sphinx-build --help

You should see ``typst`` and ``typstpdf`` listed among the available builders.

Platform-Specific Notes
=======================

Linux
-----

On Linux systems, no additional steps are required. The typst Python package includes
all necessary binaries.

macOS
-----

On macOS, you may need to install Xcode Command Line Tools:

.. code-block:: bash

   xcode-select --install

Windows
-------

On Windows, ensure you have Python installed from `python.org <https://www.python.org/>`_.
The typst Python package supports Windows natively.

Troubleshooting
===============

Import Error
------------

If you encounter an import error:

.. code-block:: text

   ModuleNotFoundError: No module named 'sphinxcontrib.typst'

Make sure you have activated the correct Python environment and that the package
is installed in that environment:

.. code-block:: bash

   python -m pip list | grep typsphinx

Missing Dependencies
--------------------

If Sphinx cannot find the typst builder, ensure all dependencies are installed:

.. code-block:: bash

   pip install --upgrade typsphinx

PDF Generation Issues
---------------------

If PDF generation fails, verify that the typst package is installed:

.. code-block:: bash

   python -c "import typst; print(typst.__version__)"

If the typst package is not installed or outdated:

.. code-block:: bash

   pip install --upgrade typst

Virtual Environments
--------------------

It is recommended to use virtual environments to avoid dependency conflicts:

.. code-block:: bash

   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\\Scripts\\activate   # On Windows
   pip install typsphinx

   # Using virtualenv
   virtualenv venv
   source venv/bin/activate
   pip install typsphinx

Next Steps
==========

After installation, see the :doc:`usage` guide to learn how to use typsphinx
in your Sphinx projects.

For configuration options, see :doc:`configuration`.
