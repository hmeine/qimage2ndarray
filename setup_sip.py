
import os, numpy
from os.path import join
from distutils.core import setup, Extension
import sipdistutils


qimageview = Extension('qimage2ndarray.qimageview',
                       sources = ['qimageview.sip'],
                       include_dirs = [numpy.get_include(),
                                       join(os.getcwd(), "include")],
                       define_macros = [('NPY_NO_DEPRECATED_API',
                                         'NPY_1_7_API_VERSION')])



class build_ext(sipdistutils.build_ext):

    user_options = sipdistutils.build_ext.user_options[:]
    user_options += [('sip-sipfiles-dir=', None,
         "directory to search for sip files"),]

    def initialize_options (self):
        sipdistutils.build_ext.initialize_options(self)
        self.sip_opts = None
        self.sip_sipfiles_dir = None

    def _sip_sipfiles_dir(self):
        if self.sip_sipfiles_dir is None:
            return sipdistutils._sip_sipfiles_dir()
        else:
            return self.sip_sipfiles_dir


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
      keywords = ["QImage", "numpy", "ndarray", "image", "convert", "PyQt4/5"],
      install_requires = ['numpy'],
      tests_require = 'nose',
      packages = ['qimage2ndarray'],
      ext_modules = [qimageview],
      cmdclass = {'build_ext': build_ext},
      long_description = """\
qimage2ndarray is a small python extension for quickly converting
between QImages and numpy.ndarrays (in both directions).  These are
very common tasks when programming e.g. scientific visualizations in
Python using PyQt4 as the GUI library.

* Supports conversion of scalar and RGB data, with arbitrary dtypes
  and memory layout, with and without alpha channels, into QImages
  (e.g. for display or saving using Qt).

* Using a tiny C++ extension, qimage2ndarray makes it possible to
  create ndarrays that are *views* into a given QImage's memory.

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
