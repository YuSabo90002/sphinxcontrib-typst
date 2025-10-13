Math and Figures Integration Test
===================================

Inline LaTeX Math
-----------------

This is inline math: :math:`E = mc^2` in the text.

Block LaTeX Math
-----------------

.. math::

   \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}

Typst Native Math
-----------------

This is Typst native inline math.

Tables
------

.. list-table:: Sample Table
   :header-rows: 1

   * - Column 1
     - Column 2
   * - Data 1
     - Data 2
   * - Data 3
     - Data 4

Code with Math
--------------

Combined content:

.. code-block:: python

   def integrate(f, a, b):
       return sum(f(x) for x in range(a, b))

And a formula: :math:`f(x) = x^2`
