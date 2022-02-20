import qimage2ndarray
from qimage2ndarray.dynqt import QtGui

from compat import setNumColors, numBytes


# Format_Indexed8 = 3
def test_raw_indexed8():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    qimg.fill(0)
    v = qimage2ndarray.raw_view(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 320)
    assert v[10, 10] == 23
    assert v[10, 12] == 42
    assert v.nbytes == numBytes(qimg)


# Format_RGB32 = 4
def test_raw_rgb32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
    qimg.fill(0)
    v = qimage2ndarray.raw_view(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, QtGui.qRgb(0, 0, 42))
    assert v.shape == (240, 320)
    assert v[10, 10] == 23 | 0xff000000
    assert v[10, 12] == 42 | 0xff000000
    assert v.nbytes == numBytes(qimg)


# Format_RGB16 = 4
def test_raw_rgb16():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB16)
    qimg.fill(0)
    v = qimage2ndarray.raw_view(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, QtGui.qRgb(0, 0, 91))
    assert v.shape == (240, 320)
    assert v[10, 10] == 23
    assert v[10, 12] == 91 >> 3
    assert v.nbytes == numBytes(qimg)


# Format_Grayscale8 = 24 (Qt 5.5+)
def test_raw_grayscale8():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Grayscale8)
    qimg.fill(0)
    v = qimage2ndarray.raw_view(qimg)
    qimg.fill(1)
    qimg.setPixel(12, 10, QtGui.qRgb(42, 42, 42))
    assert v.shape == (240, 320)
    assert v[10, 10] == 1
    assert v[10, 12] == 42
    assert v.nbytes == numBytes(qimg)


# Format_RGBA64 = 26 (Qt 5.12+)
def test_raw_rgba64():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGBA64)
    qimg.fill(0)
    v = qimage2ndarray.raw_view(qimg)
    qimg.fill(1)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12, 0x34, 0x56))
    assert v.shape == (240, 320)
    assert v[10, 10] == 0x010100000000
    assert v[10, 12] == 0xffff565634341212
    assert v.nbytes == numBytes(qimg)


# ---------------------------------------------------------------------


def test_byte_view_rgb32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
    v = qimage2ndarray.byte_view(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 320, 4)
    assert list(v[10, 10]) == [23, 0, 0, 0xff]
    assert list(v[10, 12]) == [42, 0, 0, 0xff]
    assert v.nbytes == numBytes(qimg)


def test_byte_view_indexed():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    v = qimage2ndarray.byte_view(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 320, 1)
    assert list(v[10, 10]) == [23]
    assert list(v[10, 12]) == [42]
    assert v.nbytes == numBytes(qimg)


def test_rgb_view():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
    qimg.fill(QtGui.qRgb(23, 0, 0))
    v = qimage2ndarray.rgb_view(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(12, 34, 56))
    assert list(v[10, 10]) == [23, 0, 0]
    assert list(v[10, 12]) == [12, 34, 56]


def test_alpha_view():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_ARGB32)
    qimg.fill(0)
    v = qimage2ndarray.alpha_view(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(12, 34, 56))
    assert v[10, 12] == 255
    assert v[10, 11] == 0


def test_recarray_view():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_ARGB32)
    qimg.fill(23)
    v = qimage2ndarray.recarray_view(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(12, 34, 56))
    assert v["g"][10, 12] == 34
    assert v["g"].sum() == 34
    assert v["green"].sum() == 34
    assert v.g[10, 12] == 34
    # this worked in the past, but with NumPy 1.2.1, I get:
    # TypeError: function takes at most 2 arguments (3 given)
    assert v[10, 12]["g"] == 34
