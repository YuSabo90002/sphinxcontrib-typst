API Reference
=============

This section provides detailed API documentation for typsphinx.

Builders
--------

.. automodule:: typsphinx.builder
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: typsphinx.pdf
   :members:
   :undoc-members:
   :show-inheritance:

Writer and Translator
---------------------

.. automodule:: typsphinx.writer
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: typsphinx.translator
   :members:
   :undoc-members:
   :show-inheritance:

Template Engine
---------------

.. automodule:: typsphinx.template_engine
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

Configuration values are registered in the main ``__init__.py`` module.

Available Configuration Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Name
     - Description
     - Default
   * - ``typst_documents``
     - List of documents to build
     - ``[]``
   * - ``typst_template``
     - Path to custom template file
     - ``None``
   * - ``typst_template_function``
     - Template function name or dict
     - ``None``
   * - ``typst_package``
     - Typst Universe package
     - ``None``
   * - ``typst_authors``
     - Detailed author information
     - ``None``
   * - ``typst_use_mitex``
     - Use mitex for LaTeX math
     - ``True``
   * - ``typst_use_codly``
     - Use codly for code highlighting
     - ``True``
   * - ``typst_code_line_numbers``
     - Show line numbers in code blocks
     - ``True``
   * - ``typst_papersize``
     - Paper size (e.g., "a4", "us-letter")
     - ``"a4"``
   * - ``typst_fontsize``
     - Base font size
     - ``"11pt"``

See :doc:`/user_guide/configuration` for detailed usage of each option.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
