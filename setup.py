
from distutils.core import setup

for line in open("qimage2ndarray/__init__.py"):
    if line.startswith("__version__"):
        exec(line)

setup(name = 'qimage2ndarray',
      version = __version__,
      description = 'Conversion between QImages and numpy.ndarrays.',
      author = "Hans Meine",
      author_email = "hans_meine@gmx.net",
      url = "https://github.com/hmeine/qimage2ndarray",
      download_url = "https://github.com/hmeine/qimage2ndarray/releases",
      keywords = ["QImage", "numpy", "ndarray", "image", "convert", "PyQt4", "PyQt5"],
      install_requires = ['numpy'],
      packages = ['qimage2ndarray'],
      long_description = """\
qimage2ndarray is a small python extension for quickly converting
between QImages and numpy.ndarrays (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4 as the GUI library.

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into QImages
  (e.g. for display or saving using Qt).

* qimage2ndarray makes it possible to create ndarrays_ that are
  *views* into a given QImage_'s memory.

  This allows for very efficient data handling and makes it possible
  to modify Qt image data in-place (e.g. for brightness/gamma or alpha
  mask modifications).

* `Masked arrays`_ are also supported and are converted into QImages
  with transparent pixels.

* Supports value scaling / normalization to 0..255 for convenient
  display of arbitrary NumPy arrays.
""",
      classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: User Interfaces",
    ]
)
