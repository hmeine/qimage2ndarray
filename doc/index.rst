==============
qimage2ndarray
==============

.. toctree::
   :maxdepth: 2

qimage2ndarray is a small python extension for quickly converting
between QImages_ and numpy.ndarrays_ (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4_ as the GUI library.

Similar code was found in Qwt and floating around on mailing lists,
but qimage2ndarray has the following unique feature set:

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into QImages
  (e.g. for display or saving using Qt).

* Using a tiny C++ extension, qimage2ndarray makes it possible to
  create ndarrays_ that are *views* into a given QImage_'s memory.

  This allows for very efficient data handling and makes it possible
  to modify Qt image data in-place (e.g. for brightness/gamma or alpha
  mask modifications).

* qimage2ndarray is stable and unit-tested:

  * proper reference counting even with views (ndarray.base_ points to
    the underlying QImage_)

  * handles non-standard widths and respects QImage's 32-bit row
    alignment

* `Masked arrays`_ are also supported and are converted into QImages
  with transparent pixels.

* Supports value scaling / normalization to 0..255 for convenient
  display of arbitrary NumPy arrays.

.. _masked arrays: http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html

The extension is open source, BSD-licensed, and the mercurial
repository can be `browsed online`_ or cloned using Mercurial_::

  hg clone http://www.informatik.uni-hamburg.de/~meine/hg/qimage2ndarray/

Usage
=====

.. module:: qimage2ndarray

There are two opposite directions of conversion, discussed in the next
subsections:

1. `Converting QImages into numpy.ndarrays`_.
2. `Converting ndarrays into QImages`_.

The first task is supported by a family of functions that create
*views* into the corresponding QImage_ memory, while the second task
will always copy the image data (usually converting it into the
appropriate type or value range).

.. note::

  The reason for this is that ndarrays_ are much more flexible than
  QImages_, and while it is possible - even using pure python - to
  create QImages that are views into an ndarray's memory, this will
  only work if the latter fulfills certain strict requirements
  w.r.t. dtype, strides / memory layout etc.  Thus, you'd need
  functions that set up a properly convertible ndarray, which makes
  this less convenient.  Moreover, it is then a logical next step to
  let QImage set up and manage the memory and instead create ndarray
  views.

Converting QImages into numpy.ndarrays
--------------------------------------

QImages can be viewn as `recarrays <numpy.recarray>`_ using
:func:`recarray_view`, as uint8-valued array using :func:`rgb_view`,
:func:`alpha_view`, or just :func:`byte_view`, or as raw 2D array
using :func:`raw_view`.

.. autofunction:: recarray_view(qimage)
.. autodata:: bgra_dtype
.. autofunction:: rgb_view(qimage)
.. autofunction:: alpha_view(qimage)
.. autofunction:: byte_view(qimage)
.. autofunction:: raw_view(qimage)

.. _numpy.recarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html

Converting ndarrays into QImages
--------------------------------

.. autofunction:: array2qimage(qimage)
.. autofunction:: gray2qimage(qimage)

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. _browsed online: http://www.informatik.uni-hamburg.de/~meine/hg/qimage2ndarray/
.. _Mercurial: http://mercurial.selenic.com/wiki/
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/
.. _QImage: http://doc.trolltech.com/qimage.html
.. _QImages: http://doc.trolltech.com/qimage.html
.. _numpy.ndarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _numpy.ndarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarray.base: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.base.html
