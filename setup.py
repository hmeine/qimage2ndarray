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

qt_lib_dirs = [qt_lib_dir]
qt_libraries = ["QtCore", "QtGui"]

if "mingw32" in sys.argv:
	# FIXME: better criterion - this should only apply to mingw32
	qt_lib_dirs.append(qt_lib_dir.replace(r"\lib", r"\bin"),
					   # fall back to default Qt DLL location:
					   os.path.dirname(PyQt4.__file__))
	qt_libraries = [lib + "4" for lib in qt_libraries]

# FIXME: is there a better way than to explicitly list the Qt4 include
# dirs and libraries here?  (before distutils, I used
# PyQt4.pyqtconfig.QtGuiModuleMakefile to build extensions)
qimageview = Extension('qimage2ndarray.qimageview',
					   sources = ['qimageview.sip'],
					   include_dirs = [numpy.get_include(),
									   qt_inc_dir,
									   os.path.join(qt_inc_dir, "QtCore"),
									   os.path.join(qt_inc_dir, "QtGui")],
					   library_dirs = qt_lib_dirs,
					   libraries = qt_libraries)

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

setup(name = 'qimage2ndarray',
	  version = '0.1',
	  description = 'Conversion between QImages and numpy.ndarrays.',
	  author = "Hans Meine",
	  author_email = "meine@informatik.uni-hamburg.de",
	  url = "http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray",
#	  download_url = "....tgz",
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
