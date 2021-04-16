'''PythonQt is missing bindings of some functions that we use,
so we provide backup implementations.
'''

from .dynqt import QtGui


def qRgb(r, g, b):
    return 0xff000000 + (int(r) << 16) + (int(g) << 8) + int(b)


def qRgba(r, g, b, a):
    return (int(a) << 24) + (int(r) << 16) + (int(g) << 8) + int(b)


def qAlpha(rgba):
    return (rgba & 0xff000000) >> 24


def _install_polyfill():
    if not hasattr(QtGui, 'qRgb'):
        QtGui.qRgb = qRgb
        QtGui.qRgba = qRgba
        QtGui.qAlpha = qAlpha
