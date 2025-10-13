Chapter 1: Mathematical Content
================================

This chapter demonstrates mathematical content rendering using mitex
and Typst's native math support.

.. _math-basics:

Basic Mathematics
-----------------

Inline Math
~~~~~~~~~~~

You can write inline math like :math:`a^2 + b^2 = c^2` directly in your text.

Greek letters: :math:`\alpha, \beta, \gamma, \delta, \epsilon`

Subscripts and superscripts: :math:`x_1, x_2, ..., x_n` and :math:`e^{i\theta}`

Block Equations
~~~~~~~~~~~~~~~

Quadratic formula:

.. math::

   x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

Summation:

.. math::

   \sum_{i=1}^{n} i = \frac{n(n+1)}{2}

Integration:

.. math::

   \int_0^\infty e^{-x} dx = 1

Advanced Mathematics
--------------------

Matrix Operations
~~~~~~~~~~~~~~~~~

A matrix example:

.. math::

   \begin{pmatrix}
   a & b \\
   c & d
   \end{pmatrix}
   \begin{pmatrix}
   x \\
   y
   \end{pmatrix}
   =
   \begin{pmatrix}
   ax + by \\
   cx + dy
   \end{pmatrix}

Labeled Equations
~~~~~~~~~~~~~~~~~

Important equations can be labeled and referenced:

.. math::
   :label: pythagoras

   a^2 + b^2 = c^2

The Pythagorean theorem (equation :eq:`pythagoras`) is fundamental in geometry.

.. math::
   :label: gaussian-integral

   \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}

The Gaussian integral (equation :eq:`gaussian-integral`) appears frequently
in probability theory.

Complex Expressions
~~~~~~~~~~~~~~~~~~~

Taylor series expansion:

.. math::

   e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + ...

Fourier transform:

.. math::

   F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt

Mathematical Theorems
---------------------

.. note::

   **Fermat's Last Theorem**

   For :math:`n > 2`, the equation :math:`a^n + b^n = c^n` has no integer
   solutions for :math:`a, b, c \neq 0`.

.. important::

   **Fundamental Theorem of Calculus**

   If :math:`f` is continuous on :math:`[a, b]`, then:

   .. math::

      \frac{d}{dx} \int_a^x f(t) dt = f(x)

Code with Math
--------------

Here's a Python implementation of the Euler method for differential equations:

.. code-block:: python

   def euler_method(f, y0, t0, tf, n):
       """
       Solve dy/dt = f(t, y) using Euler's method.

       The update rule is: y_{n+1} = y_n + h * f(t_n, y_n)
       """
       h = (tf - t0) / n
       t = t0
       y = y0

       for i in range(n):
           y = y + h * f(t, y)
           t = t + h

       return y

The corresponding mathematical formulation is:

.. math::

   y_{n+1} = y_n + h \cdot f(t_n, y_n)

Summary
-------

This chapter demonstrated:

- Inline and block mathematics
- Greek letters, fractions, and special functions
- Matrices and complex expressions
- Labeled equations and cross-references
- Integration of code and mathematics

See :ref:`math-basics` for a review of basic concepts.
