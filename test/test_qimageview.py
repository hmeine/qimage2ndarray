from qimage2ndarray import _qimageview
from qimage2ndarray.dynqt import qt, QtGui
import sys, numpy

from nose.tools import raises, assert_equal
from compat import setNumColors, numBytes


def test_viewcreation():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
    v = _qimageview(qimg)
    assert_equal(v.shape, (240, 320))
    assert v.base is not None
    del qimg
    if hasattr(v.base, 'width'):
        w, h = v.base.width(), v.base.height() # should not segfault
        assert_equal((w, h), (320, 240))
    v[239] = numpy.arange(320) # should not segfault

@raises(TypeError)
def test_qimageview_noargs():
    v = _qimageview()

@raises(TypeError)
def test_qimageview_manyargs():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    v = _qimageview(qimg, 1)

@raises(TypeError)
def test_qimageview_wrongarg():
    v = _qimageview(42)

def test_data_access():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    qimg.fill(42)
    v = _qimageview(qimg)
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 42)
    assert_equal(v.nbytes, numBytes(qimg))

def test_being_view():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    qimg.fill(23)
    v = _qimageview(qimg)
    qimg.fill(42)
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 42)
    assert_equal(v.nbytes, numBytes(qimg))

def test_coordinate_access():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, 42)
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 23)
    assert_equal(v[10,12], 42)
    assert_equal(v.nbytes, numBytes(qimg))

def test_RGB32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 23 | 0xff000000)
    assert_equal(v[10,12], 0xff123456 if sys.byteorder == 'little' else 0x563412ff)
    assert_equal(v.nbytes, numBytes(qimg))

def test_ARGB32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_ARGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,12], 0xff123456 if sys.byteorder == 'little' else 0x563412ff)
    assert_equal(v.nbytes, numBytes(qimg))

def test_RGBX64():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGBX64)
    qimg.fill(QtGui.qRgb(0, 0, 0))
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 0xffff000000000000 if sys.byteorder == 'little' else 0xffff)
    assert_equal(v[10,12], 0xffff565634341212 if sys.byteorder == 'little' else 0x121234345656ffff)
    assert_equal(v.nbytes, numBytes(qimg))

def test_RGBA64():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGBX64)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert_equal(v.shape, (240, 320))
    assert_equal(v[10,10], 0)
    assert_equal(v[10,12], 0xffff565634341212 if sys.byteorder == 'little' else 0x121234345656ffff)
    assert_equal(v.nbytes, numBytes(qimg))

def test_odd_size_8bit():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format_Indexed8)
    setNumColors(qimg, 256)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert_equal(v.shape, (240, 321))
    assert_equal(v[10,12], 42)
    assert_equal(v.strides[0], qimg.bytesPerLine())

def test_odd_size_32bit():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format_ARGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert_equal(v.shape, (240, 321))
    assert_equal(v[10,12], 42)
    assert_equal(v.strides[0], qimg.bytesPerLine())

def test_odd_size_32bit_rgb():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format_RGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert_equal(v.shape, (240, 321))
    assert_equal(v[10,12], 42 | 0xff000000)
    assert_equal(v.strides[0], qimg.bytesPerLine())
    assert_equal(v.strides[1], 4)

@raises(ValueError)
def test_mono():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Mono)
    v = _qimageview(qimg)

@raises(ValueError)
def test_rgb666():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB666)
    v = _qimageview(qimg)
