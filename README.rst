qimage2ndarray
==============

qimage2ndarray is a small python extension for quickly converting
between ``QImages`` and ``numpy.ndarrays`` (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4 as the GUI library.

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into ``QImages``
  (e.g. for display or saving using Qt).

* qimage2ndarray makes it possible to create ``ndarrays`` that are
  *views* into a given QImage's memory.

  This allows for very efficient data handling and makes it possible
  to modify Qt image data in-place (e.g. for brightness/gamma or alpha
  mask modifications).

* qimage2ndarray is stable and unit-tested:

  * proper reference counting even with views (ndarray.base_ points to
    the underlying QImage)

  * handles non-standard widths and respects QImage's 32-bit row
    alignment

* `Masked arrays`_ are also supported and are converted into QImages
  with transparent pixels.

* Supports recarrays_ (and comes with an appropriate dtype) for
  convenient access to RGB(A) channels.

* Supports value scaling / normalization to 0..255 for convenient
  display of arbitrary NumPy arrays.

* Recent additions are convenient image loading / saving methods

.. _masked arrays: http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html
.. _recarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html

Code
----

The extension is open source, BSD-licensed, and the
repository can be `browsed online`_ or cloned using Git:

  git clone https://github.com/hmeine/qimage2ndarray.git

Documentation
-------------

Documentation can be found in the doc/ subdirectory or on GitHub:

  http://hmeine.github.io/qimage2ndarray

Contributors
------------

This package is written and maintained by Hans Meine <hans_meine@gmx.net>.

I am grateful for feedback from Ullrich Köthe, PowerPC/endianness
testing by Helge Kreutzmann and initial PyQt5 support by Rudolf Hoefler.

.. _browsed online: https://github.com/hmeine/qimage2ndarray
.. _ndarray.base: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.base.html
