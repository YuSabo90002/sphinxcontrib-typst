Chapter 2: Figures and Tables
==============================

This chapter demonstrates figures, tables, and cross-referencing features.

.. _figures-section:

Tables
------

Simple Tables
~~~~~~~~~~~~~

A basic table example:

.. list-table:: Programming Languages Comparison
   :header-rows: 1
   :widths: 25 25 25 25

   * - Language
     - Paradigm
     - Typing
     - Use Case
   * - Python
     - Multi-paradigm
     - Dynamic
     - General purpose
   * - Rust
     - Systems
     - Static
     - Performance
   * - JavaScript
     - Multi-paradigm
     - Dynamic
     - Web development
   * - Haskell
     - Functional
     - Static
     - Academic

Complex Tables
~~~~~~~~~~~~~~

Tables with mathematical content:

.. list-table:: Common Mathematical Constants
   :header-rows: 1
   :widths: 20 30 50

   * - Symbol
     - Value
     - Description
   * - :math:`\pi`
     - 3.14159...
     - Ratio of circumference to diameter
   * - :math:`e`
     - 2.71828...
     - Euler's number (base of natural logarithm)
   * - :math:`\phi`
     - 1.61803...
     - Golden ratio
   * - :math:`\gamma`
     - 0.57721...
     - Euler-Mascheroni constant

Lists and Enumerations
-----------------------

Nested Lists
~~~~~~~~~~~~

- Programming Languages

  - Compiled Languages

    - C/C++
    - Rust
    - Go

  - Interpreted Languages

    - Python
    - Ruby
    - JavaScript

- Markup Languages

  - reStructuredText
  - Markdown
  - Typst

Enumerated Lists
~~~~~~~~~~~~~~~~

1. First, initialize the project:

   .. code-block:: bash

      sphinx-quickstart

2. Then, add sphinxcontrib-typst to extensions:

   .. code-block:: python

      extensions = ['sphinxcontrib.typst']

3. Finally, build the documentation:

   .. code-block:: bash

      sphinx-build -b typst . _build/typst

Cross-References
----------------

.. _algorithms-section:

Referencing Sections
~~~~~~~~~~~~~~~~~~~~

You can reference other sections in the documentation:

- See :ref:`figures-section` for information about figures
- Check :ref:`math-basics` in Chapter 1 for basic mathematics
- Review :ref:`intro-label` in the index for an overview

Referencing Documents
~~~~~~~~~~~~~~~~~~~~~

Link to other documents:

- Main documentation: :doc:`index`
- Mathematics chapter: :doc:`chapter1`

External Links
~~~~~~~~~~~~~~

Links to external resources:

- `Sphinx Documentation <https://www.sphinx-doc.org/>`_
- `Typst Documentation <https://typst.app/docs/>`_
- `mitex Package <https://typst.app/universe/package/mitex>`_
- `codly Package <https://typst.app/universe/package/codly>`_

Code Examples
-------------

Multi-Language Code Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python:

.. code-block:: python

   class DocumentBuilder:
       """Build documentation from source files."""

       def __init__(self, source_dir, output_dir):
           self.source_dir = source_dir
           self.output_dir = output_dir

       def build(self):
           """Execute the build process."""
           print(f"Building from {self.source_dir}")

Rust:

.. code-block:: rust

   struct DocumentBuilder {
       source_dir: String,
       output_dir: String,
   }

   impl DocumentBuilder {
       fn new(source_dir: String, output_dir: String) -> Self {
           Self { source_dir, output_dir }
       }

       fn build(&self) {
           println!("Building from {}", self.source_dir);
       }
   }

JavaScript:

.. code-block:: javascript

   class DocumentBuilder {
       constructor(sourceDir, outputDir) {
           this.sourceDir = sourceDir;
           this.outputDir = outputDir;
       }

       build() {
           console.log(`Building from ${this.sourceDir}`);
       }
   }

Admonitions
-----------

Note Box
~~~~~~~~

.. note::

   This is an informational note. Use it to provide additional context
   or helpful tips to readers.

Warning Box
~~~~~~~~~~~

.. warning::

   This is a warning. Use it to alert readers about potential issues
   or important considerations.

Important Box
~~~~~~~~~~~~~

.. important::

   This highlights critical information that readers should not miss.

Tip Box
~~~~~~~

.. tip::

   Pro tip: You can nest admonitions and include code blocks inside them!

   .. code-block:: python

      def useful_tip():
          return "Always write clear documentation!"

Summary
-------

This chapter demonstrated:

- Simple and complex tables
- Nested and enumerated lists
- Cross-references to sections, documents, and equations
- External links
- Multi-language code examples
- Various admonition types

For more examples, see :ref:`algorithms-section` or return to :doc:`index`.
