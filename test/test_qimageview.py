from qimage2ndarray import _qimageview
from qimage2ndarray.dynqt import qt, QtGui
import sys, numpy

from compat import setColorCount, sizeInBytes
import pytest


def test_viewcreation():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGB32)
    v = _qimageview(qimg)
    assert v.shape == (240, 320)
    assert v.base is not None
    del qimg
    if hasattr(v.base, 'width'):
        w, h = v.base.width(), v.base.height() # should not segfault
        assert (w, h) == (320, 240)
    v[239] = numpy.arange(320) # should not segfault

def test_qimageview_noargs():
    with pytest.raises(TypeError):
        v = _qimageview()

def test_qimageview_manyargs():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_Indexed8)
    with pytest.raises(TypeError):
        v = _qimageview(qimg, 1)

def test_qimageview_wrongarg():
    with pytest.raises(TypeError):
        v = _qimageview(42)

def test_data_access():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_Indexed8)
    setColorCount(qimg, 256)
    qimg.fill(42)
    v = _qimageview(qimg)
    assert v.shape == (240, 320)
    assert v[10,10] == 42
    assert v.nbytes == sizeInBytes(qimg)

def test_being_view():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_Indexed8)
    setColorCount(qimg, 256)
    qimg.fill(23)
    v = _qimageview(qimg)
    qimg.fill(42)
    assert v.shape == (240, 320)
    assert v[10,10] == 42
    assert v.nbytes == sizeInBytes(qimg)

def test_coordinate_access():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_Indexed8)
    setColorCount(qimg, 256)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 320)
    assert v[10,10] == 23
    assert v[10,12] == 42
    assert v.nbytes == sizeInBytes(qimg)

def test_RGB32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,10] == 23 | 0xff000000
    assert v[10,12] == 0xff123456 if sys.byteorder == 'little' else 0x563412ff
    assert v.nbytes == sizeInBytes(qimg)

def test_ARGB32():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_ARGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,12] == 0xff123456 if sys.byteorder == 'little' else 0x563412ff
    assert v.nbytes == sizeInBytes(qimg)

def test_RGBX8888():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGBX8888)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.fill(23)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,10] == 23 | 0xff000000
    assert v[10,12] == 0x123456ff if sys.byteorder == 'big' else 0xff563412
    assert v.nbytes == sizeInBytes(qimg)

def test_RGBA8888():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGBA8888)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,12] == 0x123456ff if sys.byteorder == 'big' else 0xff563412
    assert v.nbytes == sizeInBytes(qimg)

def test_RGBX64():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGBX64)
    qimg.fill(QtGui.qRgb(0, 0, 0))
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,10] == 0xffff000000000000 if sys.byteorder == 'little' else 0xffff
    assert v[10,12] == 0xffff565634341212 if sys.byteorder == 'little' else 0x121234345656ffff
    assert v.nbytes == sizeInBytes(qimg)

def test_RGBA64():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGBX64)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, QtGui.qRgb(0x12,0x34,0x56))
    assert v.shape == (240, 320)
    assert v[10,10] == 0
    assert v[10,12] == 0xffff565634341212 if sys.byteorder == 'little' else 0x121234345656ffff
    assert v.nbytes == sizeInBytes(qimg)

def test_odd_size_8bit():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format.Format_Indexed8)
    setColorCount(qimg, 256)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 321)
    assert v[10,12] == 42
    assert v.strides[0] == qimg.bytesPerLine()

def test_odd_size_32bit():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format.Format_ARGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 321)
    assert v[10,12] == 42
    assert v.strides[0] == qimg.bytesPerLine()

def test_odd_size_32bit_rgb():
    qimg = QtGui.QImage(321, 240, QtGui.QImage.Format.Format_RGB32)
    qimg.fill(0)
    v = _qimageview(qimg)
    qimg.setPixel(12, 10, 42)
    assert v.shape == (240, 321)
    assert v[10,12] == 42 | 0xff000000
    assert v.strides[0] == qimg.bytesPerLine()
    assert v.strides[1] == 4

def test_mono():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_Mono)
    with pytest.raises(ValueError):
        v = _qimageview(qimg)

def test_rgb666():
    qimg = QtGui.QImage(320, 240, QtGui.QImage.Format.Format_RGB666)
    with pytest.raises(ValueError):
        v = _qimageview(qimg)
