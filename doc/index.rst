==============
qimage2ndarray
==============

.. toctree::
   :maxdepth: 2

qimage2ndarray is a small python package for quickly converting
between QImages_ and numpy.ndarrays_ (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4_ as the GUI library.

Similar code was found in Qwt and floating around on mailing lists,
but qimage2ndarray has the following unique feature set:

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into QImages
  (e.g. for display or saving using Qt).

* qimage2ndarray makes it possible to create ndarrays_ that are
  *views* into a given QImage_'s memory.

  This allows for very efficient data handling and makes it possible
  to modify Qt image data in-place (e.g. for brightness/gamma or alpha
  mask modifications).

* qimage2ndarray is stable and unit-tested:

  * proper reference counting even with views (ndarray.base_ points to
    the underlying QImage_)

  * handles non-standard widths and respects QImage's 32-bit row
    alignment

  * tested with Python 2 and Python 3, and various Qt wrappers

* `Masked arrays`_ are also supported and are converted into QImages
  with transparent pixels.

* Supports recarrays_ (and comes with an appropriate dtype) for
  convenient access to RGB(A) channels (see :func:`recarray_view`).

* Supports value scaling / normalization to 0..255 for convenient
  display of arbitrary NumPy arrays.

* Recent additions are convenient image loading / saving methods.

.. _masked arrays: http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html

qimage2ndarray works with both Python 2.x and Python 3.x on all major
platforms, and with different Python wrappers of Qt (PyQt4 and PyQt5,
PySide, PySide2 and PythonQt).  The package is open source,
BSD-licensed__, and the repository can be `browsed online`_ or cloned
using Git_::

  git clone https://github.com/hmeine/qimage2ndarray.git

__ http://www.opensource.org/licenses/bsd-license.php

Changelog
=========

Version 1.9.0:
  - first support for 64bit pixel types
  - switched tests from nose to pytest
  - support PySide6
  - code cleanups

Version 1.8.3:
  - fix normalization potentially modifying input array

Version 1.8.2:
  - normalize boolean arrays to 0/255 by default

Version 1.8.1:
  - support normalization of boolean arrays

Version 1.8:
  - improve exception when calling `imread` on non-existing file
  - improved pure-python implementation working with PythonQt as well

Version 1.7:
  - add support for PySide2
  - changed default driver from PyQt4 to PyQt5

Version 1.6:
  - finally, also support PySide on Python 3 (closing last known issue)

Version 1.5.1:
  - small installation and documentation fixes

Version 1.5:
  - PyQt5 support

Version 1.4:
  - *pure python* version of qimage2ndarray
  - PySide support (Python 2 only yet)
  - added :func:`imsave()`

Version 1.3.1:
  - restored compatibility with NumPy 1.6 (lost in 1.2)

Version 1.3:
  - added :func:`imread()`
  - added implicit loading in view functions

Version 1.2:
  - support Python 3.x (in addition to Python 2.x, same codebase)
  - adapted to NumPy 1.7 API
  - move documentation away from uni-hamburg.de, too

Version 1.1:
  - gracefully handle empty normalization range
  - improved compilation support (on Windows and OS X)
  - small optimizations
  - support alternative Qt bindings (PythonQt, used by MeVisLab)
  - update URLs/email to move away from uni-hamburg.de

Version 1.0:
  - Let array2qimage support 2 channels (gray + alpha)
  - Fixed installation on OS X (where Qt libs come as "Frameworks")

Version 0.2:
  - Fixed endianness issues (tested on PowerPC arch)
  - Simplified installation on Windows (e.g. with Qt DLLs bundled with PyQt)

Version 0.1:
  - Initial Relase

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
  QImages_, and while it is possible -- even using pure python -- to
  create QImages that are views into an ndarray's memory, this will
  only work if the latter fulfills certain strict requirements
  w.r.t. dtype, strides / memory layout etc.  Thus, you'd need
  functions that set up a properly convertible ndarray, which makes
  this less convenient.  Moreover, it is then a logical next step to
  let QImage set up and manage the memory and instead create ndarray
  views.

Converting QImages into numpy.ndarrays
--------------------------------------

QImages can be viewed as recarrays_ using
:func:`recarray_view`, as uint8-valued array using :func:`rgb_view`,
:func:`alpha_view`, or just :func:`byte_view`, or as raw 2D array
using :func:`raw_view`.

.. autofunction:: recarray_view(qimage)
.. autodata:: bgra_dtype
.. autofunction:: rgb_view(qimage)
.. autofunction:: alpha_view(qimage)
.. autofunction:: byte_view(qimage)
.. autofunction:: raw_view(qimage)

Converting ndarrays into QImages
--------------------------------

.. autofunction:: array2qimage(array[, normalize])
.. autofunction:: gray2qimage(gray[, normalize])

Loading and Saving Images
-------------------------

There are two ways to read images from disk directly into `ndarrays`:

1. The :func:`imread` function mimicks existing API in other
   libraries, returning an ndarray whose dimensionality and shape
   depends on whether the image is a color or grayscale image.

2. Also, the view functions (all five of them) can be passed a
   filename instead of a qimage.  This can be more useful than
   :func:`imread`, e.g. in case you want to get a recarray_
   (:func:`recarray_view`), just the alpha channel
   (:func:`alpha_view`), or the original ARGB image data
   (:func:`byte_view`).

.. autofunction:: imread(filename)

Finally, there is also a tiny wrapper around :func:`array2qimage` and
`QImage.save()` for saving images to disk:

.. autofunction:: imsave(filename, array[, normalize])


Indices and Tables
==================

* :ref:`genindex`
* :ref:`search`

.. _browsed online: https://github.com/hmeine/qimage2ndarray
.. _Git: http://git-scm.com
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/
.. _QImage: http://qt-project.org/doc/qt-4.8/qimage.html
.. _QImages: http://qt-project.org/doc/qt-4.8/qimage.html

.. _numpy.ndarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _numpy.ndarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html
.. _ndarray.base: http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.base.html

.. _recarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
.. _recarrays: http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
.. _numpy.recarray: http://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
