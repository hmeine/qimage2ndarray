qimage2ndarray
==============

qimage2ndarray is a small python extension for quickly converting
between QImages_ and numpy.ndarrays_ (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4_ as the GUI library.

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into QImages
  (e.g. for display or saving using Qt).

* Using a tiny C++ extension, qimage2ndarray makes it possible to
  create ndarrays_ that are *views* into a given QImage_'s memory.

  This allows for very efficient data handling and makes it possible
  to modify Qt image data in-place (e.g. for brightness/gamma or alpha
  mask modifications).

* qimage2ndarray is stable and unit-tested.

* `Masked arrays`_ are also supported and are converted into QImages
  with transparent pixels.

* Supports value scaling / normalization to 0..255 for convenient
  display of arbitrary NumPy arrays.

The extension is open source, BSD-licensed, and the mercurial
repository can be browsed online or cloned using Mercurial:

  hg clone http://www.informatik.uni-hamburg.de/~meine/hg/qimage2ndarray/

Documentation can be found in the doc/ subdirectory or on the homepage:

  http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray
