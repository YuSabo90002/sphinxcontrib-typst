Templates
=========

Customize the appearance and structure of your Typst output using templates.

Template System Overview
------------------------

typsphinx uses Typst templates to control document layout and styling.
There are three ways to customize templates:

1. **Default template**: Built-in template (no configuration needed)
2. **Configuration-based**: Use ``typst_template_function`` dict format
3. **Custom template file**: Provide your own ``.typ`` template

Default Template
----------------

The default template provides a clean, professional layout:

.. code-block:: python

   # No configuration needed - uses built-in template
   typst_documents = [
       ("index", "output", "Title", "Author", "typst"),
   ]

Features:

- Title page with project name and author
- Table of contents
- Section numbering
- Professional styling

Configuration-Based Templates
------------------------------

Use Typst Universe packages with configuration:

.. code-block:: python

   typst_package = "@preview/charged-ieee:0.1.4"

   typst_template_function = {
       "name": "ieee",
       "params": {
           "abstract": "This paper presents...",
           "index-terms": ["AI", "ML"],
           "paper-size": "us-letter",
       }
   }

Advantages:

- No custom files needed
- Declarative configuration
- Easy to maintain

See :doc:`/examples/advanced` for complete examples.

Custom Template Files
---------------------

For full control, create a custom template file.

Template Assets
~~~~~~~~~~~~~~~

When using custom templates, you often need additional assets like fonts, logos, or images. typsphinx automatically copies these assets to the output directory.

**Automatic Asset Copying (Default)**

By default, all files in your template directory are automatically copied (except ``.typ`` files):

.. code-block:: python

   # conf.py
   typst_template = "_templates/custom.typ"
   # All files in _templates/ are automatically copied

Directory structure:

.. code-block:: text

   _templates/
     ├── custom.typ          # Template file
     ├── logo.png            # Automatically copied
     ├── fonts/
     │   └── custom.otf      # Automatically copied
     └── icons/
         └── icon.svg        # Automatically copied

Reference assets in your template using relative paths:

.. code-block:: typst

   // _templates/custom.typ
   #image("logo.png")
   #set text(font: "fonts/custom.otf")
   #image("icons/icon.svg")

**Explicit Asset Specification**

For more control, explicitly specify which assets to copy:

.. code-block:: python

   # conf.py
   typst_template = "_templates/custom.typ"
   typst_template_assets = [
       "_templates/logo.png",
       "_templates/fonts/",
       "_templates/icons/*.svg"
   ]

Features:

- Individual files: ``"_templates/logo.png"``
- Directories: ``"_templates/fonts/"``
- Glob patterns: ``"_templates/icons/*.svg"``

**Disabling Automatic Copying**

To disable automatic asset copying (for performance):

.. code-block:: python

   # conf.py
   typst_template = "_templates/custom.typ"
   typst_template_assets = []  # Empty list = no automatic copying

.. note::

   Typst Universe packages (``typst_package``) handle assets automatically.
   Asset copying only applies to custom local templates (``typst_template``).

Basic Structure
~~~~~~~~~~~~~~~

Create a file ``_templates/custom.typ``:

.. code-block:: typst

   #let project(
     title: "",
     authors: (),
     date: none,
     body
   ) = {
     // Title page
     align(center)[
       #text(size: 24pt, weight: "bold")[#title]
       #v(1em)
       #text(size: 14pt)[#authors.join(", ")]
       #if date != none {
         v(1em)
         text(size: 12pt)[#date]
       }
     ]

     pagebreak()

     // Table of contents
     outline(title: "Contents", indent: auto)

     pagebreak()

     // Document body
     body
   }

Configuration
~~~~~~~~~~~~~

Reference your custom template in ``conf.py``:

.. code-block:: python

   typst_template = "_templates/custom.typ"

Template Parameters
-------------------

Standard Parameters
~~~~~~~~~~~~~~~~~~~

Your template function receives these parameters:

- ``title``: Document title (from ``typst_documents``)
- ``authors``: Author(s) tuple or list
- ``date``: Document date (auto-generated or custom)
- ``body``: The main document content

Custom Parameters
~~~~~~~~~~~~~~~~~

Add custom parameters using ``typst_template_function``:

.. code-block:: python

   typst_template_function = {
       "name": "project",  # Your template function name
       "params": {
           "subtitle": "A Technical Report",
           "version": "1.0",
           "confidential": True,
       }
   }

Access in template:

.. code-block:: typst

   #let project(
     title: "",
     subtitle: none,
     version: none,
     confidential: false,
     body
   ) = {
     // Use custom parameters
     if confidential {
       text(fill: red)[CONFIDENTIAL]
     }
     // ...
   }

Wrapping External Packages
---------------------------

You can wrap Typst Universe packages in custom templates:

.. code-block:: typst

   #import "@preview/charged-ieee:0.1.4": ieee

   #let project(
     title: "",
     authors: (),
     body
   ) = {
     // Transform parameters
     let ieee_authors = authors.map(name => (
       name: name,
       department: "Engineering",
       organization: "My Org",
     ))

     // Apply IEEE template
     show: ieee.with(
       title: title,
       authors: ieee_authors,
     )

     body
   }

This approach gives you:

- Parameter transformation
- Custom preprocessing
- Multiple package integration

Examples
--------

Minimal Template
~~~~~~~~~~~~~~~~

.. code-block:: typst

   #let project(title: "", body) = {
     set page(paper: "a4", margin: 2.5cm)
     set text(font: "New Computer Modern", size: 11pt)

     align(center)[#text(20pt, weight: "bold")[#title]]
     v(2em)

     body
   }

Academic Paper Template
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: typst

   #let project(
     title: "",
     authors: (),
     abstract: none,
     keywords: (),
     body
   ) = {
     // Two-column layout
     set page(
       paper: "us-letter",
       columns: 2,
       margin: (x: 2cm, y: 2.5cm),
     )

     // Title and authors in single column
     place(top + center, float: true)[
       #text(18pt, weight: "bold")[#title]
       #v(0.5em)
       #text(12pt)[#authors.join(", ")]
     ]

     // Abstract box
     if abstract != none {
       place(top + center, float: true, clearance: 3em)[
         #box(width: 100%, inset: 1em)[
           *Abstract:* #abstract
         ]
       ]
     }

     // Keywords
     if keywords.len() > 0 {
       place(top + center, float: true, clearance: 6em)[
         *Keywords:* #keywords.join(", ")
       ]
     }

     v(8em)

     // Two-column body
     body
   }

Best Practices
--------------

1. **Start simple**: Use the default template or configuration-based approach first
2. **Reuse packages**: Leverage Typst Universe packages when possible
3. **Test incrementally**: Build frequently to catch errors early
4. **Document parameters**: Comment your template parameters clearly
5. **Keep it maintainable**: Don't over-complicate templates

Debugging Templates
-------------------

If you encounter errors:

1. **Check syntax**: Typst errors are reported in build output
2. **Test standalone**: Compile your template with test data
3. **Use typst builder**: Generate ``.typ`` files to inspect output
4. **Simplify**: Remove customizations until it works

.. code-block:: bash

   # Generate .typ files for inspection
   sphinx-build -b typst source/ build/typst

   # Check the generated template usage
   cat build/typst/index.typ

See Also
--------

- :doc:`configuration` - Template configuration options
- :doc:`/examples/advanced` - Advanced template examples
- `Typst Documentation <https://typst.app/docs>`_ - Official Typst docs
- `Typst Universe <https://typst.app/universe>`_ - Template packages
