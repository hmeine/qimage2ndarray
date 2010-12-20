from distutils.core import setup, Extension

import sys, os.path, numpy
import sipdistutils

import PyQt4.pyqtconfig
config = PyQt4.pyqtconfig.Configuration()

# --------------------------------------------------------------------

# Replace the following with
#  qt_inc_dir = "C:/path/to/Qt/include"
#  qt_lib_dir = "C:/path/to/Qt/lib"
# when automatically extracted paths don't fit your installation.
# (Note that you should use a compatible compiler and Qt version
#  as was used for building PyQt.)
qt_inc_dir = config.qt_inc_dir
qt_lib_dir = config.qt_lib_dir

# --------------------------------------------------------------------

# Is there a better way than to explicitly list the Qt4 include
# dirs and libraries here?  (before distutils, I used
# PyQt4.pyqtconfig.QtGuiModuleMakefile to build extensions)
qt_lib_dirs = [qt_lib_dir]
qt_libraries = ["QtCore", "QtGui"]

# TODO: is this the right criterion?
# seems to be correct for mingw32 and msvc at least:
if sys.platform.startswith("win"): # was: if "mingw32" in sys.argv:
	qt_lib_dirs.extend((qt_lib_dir.replace(r"\lib", r"\bin"),
						# fall back to default Qt DLL location:
						os.path.dirname(PyQt4.__file__)))
	qt_libraries = [lib + "4" for lib in qt_libraries]

qimageview = Extension('qimage2ndarray.qimageview',
					   sources = ['qimageview.sip'],
					   include_dirs = [numpy.get_include(),
									   qt_inc_dir,
									   os.path.join(qt_inc_dir, "QtCore"),
									   os.path.join(qt_inc_dir, "QtGui")])

if sys.platform == 'darwin':
	# Qt is distributed as 'framework' on OS X; obviously we need this
	# special handling?!
	for lib in qt_libraries:
		qimageview.extra_link_args.extend(['-framework', lib])
	for d in qt_lib_dirs:
		qimageview.extra_link_args.append('-F' + d)
else:
	qimageview.libraries.extend(qt_libraries)
	qimageview.library_dirs.extend(qt_lib_dirs)

class build_ext(sipdistutils.build_ext):
	def _sip_compile(self, sip_bin, source, sbf):
		import PyQt4.pyqtconfig
		config = PyQt4.pyqtconfig.Configuration()
		self.spawn([sip_bin,
					"-c", self.build_temp,
					"-b", sbf] +
				   config.pyqt_sip_flags.split() +
				   ["-I", config.pyqt_sip_dir,
					source])

for line in file("qimage2ndarray/__init__.py"):
	if line.startswith("__version__"):
		exec line

setup(name = 'qimage2ndarray',
	  version = __version__,
	  description = 'Conversion between QImages and numpy.ndarrays.',
	  author = "Hans Meine",
	  author_email = "meine@informatik.uni-hamburg.de",
	  url = "http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray",
	  download_url = "http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/dist",
	  keywords = ["QImage", "numpy", "ndarray", "image", "convert", "PyQt4"],
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
