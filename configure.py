#!/usr/bin/env python
import os, sys, subprocess, numpy, glob, shutil

# --------------------------------------------------------------------

from optparse import OptionParser

moduleName = "qimageview"

print "checking SIP/PyQt4 configuration..."
import PyQt4.pyqtconfig as pyqt4
config = pyqt4.Configuration()

moddir = config.pyqt_mod_dir
if moddir.endswith("PyQt4"):
	moddir = moddir[:-6]

op = OptionParser(usage = "python %prog [options]")
op.add_option("-m", "--moddir", action = "store",
			  dest = "moddir", default = moddir,
			  help = "install directory for the python module (default %r)"
			  % moddir)
op.add_option("-d", "--debug", action = "store_true",
			  dest = "debug", default = False,
			  help = "debug build (w/ debugging symbols)")
options, args = op.parse_args()

subdir = "sip"
buildfile = os.path.join(subdir, "%s.sbf" % moduleName)
command = [config.sip_bin, "-c", subdir, "-b", buildfile] + \
		  config.pyqt_sip_flags.split() + \
		  ["-I", config.pyqt_sip_dir, "%s.sip" % moduleName]

if not os.path.isdir(subdir):
	os.mkdir(subdir)

print "running SIP (%s)..." % " ".join(command)
ec = subprocess.call(command)
if ec:
	sys.exit(ec)

# --------------------------------------------------------------------

print "\nthe target directory for module installation will be:\n  %s\n" % options.moddir

print "generating Makefile..."
makefile = pyqt4.QtGuiModuleMakefile(
	config, buildfile, makefile = os.path.join(subdir, "Makefile"),
	debug = options.debug,
	install_dir = options.moddir)

makefile.extra_include_dirs.append(numpy.get_include())
makefile.generate()

print "done (you can run 'make -C sip' now)."
