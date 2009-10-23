from distutils.core import setup, Extension

import os.path, numpy
import sipdistutils

import PyQt4.pyqtconfig
config = PyQt4.pyqtconfig.Configuration()

# FIXME: is there a better way than to explicitly list the Qt4 include
# dirs and libraries here?  (before distutils, I used
# PyQt4.pyqtconfig.QtGuiModuleMakefile to build extensions)
qimageview = Extension('qimage2ndarray.qimageview',
					   sources = ['qimageview.sip'],
					   include_dirs = [numpy.get_include(),
									   config.qt_inc_dir,
									   os.path.join(config.qt_inc_dir, "QtCore"),
									   os.path.join(config.qt_inc_dir, "QtGui")],
					   library_dirs = [config.qt_lib_dir],
					   libraries = ["QtCore", "QtGui"])

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
	  packages = ['qimage2ndarray'],
	  ext_modules = [qimageview],
	  cmdclass = {'build_ext': build_ext})
