import qimage2ndarray, numpy
from qimage2ndarray.dynqt import QtGui

from nose.tools import assert_equal

def test_gray2qimage():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_Indexed8)
    assert_equal(a.nbytes, qImg.numBytes() * a.itemsize)
    assert_equal(qImg.numColors(), 256)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(42,42,42)))
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(0,0,0)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))

def test_gray2qimage_normalize():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_Indexed8)
    assert_equal(a.nbytes, qImg.numBytes() * a.itemsize)
    assert_equal(qImg.numColors(), 256)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(255,255,255)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    x = int(255 * 10.0 / 52.42)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))

def test_empty2qimage():
    a = numpy.ones((240, 320), dtype = float)
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))

def test_gray2qimage_normalize_onlymax():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = 80)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_Indexed8)
    assert_equal(a.nbytes, qImg.numBytes() * a.itemsize)
    assert_equal(qImg.numColors(), 256)
    x = int(255 * 42.42 / 80.0)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(x,x,x)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(0,0,0)))

def test_gray2qimage_normalize_domain():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = (-100, 100))
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_Indexed8)
    assert_equal(a.nbytes, qImg.numBytes() * a.itemsize)
    assert_equal(qImg.numColors(), 256)
    x = int(255 * 142.42 / 200.0)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(x,x,x)))
    x = int(255 *  90.0 / 200.0)
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(x,x,x)))
    x = int(255 * 100.0 / 200.0)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))

def test_gray2qimage_normalize_dont_touch_0_255():
    a = numpy.zeros((100, 256), dtype = float)
    a[:] = numpy.arange(256)
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    b = qimage2ndarray.raw_view(qImg)
    assert numpy.all(a == b)

def test_gray2qimage_masked():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    a[:,160:] = 100
    a = numpy.ma.masked_greater(a, 99)
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_Indexed8)
    assert_equal(a.nbytes, qImg.numBytes() * a.itemsize)
    assert_equal(qImg.numColors(), 256)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(255,255,255)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    x = int(255 * 10.0 / 52.42)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))
    assert_equal(QtGui.qAlpha(qImg.pixel(0,10)), 255)
    assert_equal(QtGui.qAlpha(qImg.pixel(200,10)), 0)

# --------------------------------------------------------------------

def test_scalar2qimage():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(42,42,42))) # max pixel
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(0,0,0)))    # zero pixel
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))    # min pixel

def test_scalar2qimage_with_alpha():
    a = numpy.zeros((240, 320, 2), dtype = float)
    a[...,1] = 255
    a[12,10] = (42.42, 128)
    a[13,10] = (-10, 0)
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_ARGB32)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgba(42,42,42,128))) # max pixel
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgba(0,0,0,255)))    # zero pixel
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgba(0,0,0,0)))      # min pixel

def test_scalar2qimage_normalize():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(255,255,255))) # max pixel
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))       # min pixel
    x = int(255 * 10.0 / 52.42)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))       # zero pixel

def test_scalar2qimage_normalize_onlymax():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = 80)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    x = int(255 * 42.42 / 80.0)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(x,x,x))) # max pixel
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0))) # min pixel
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(0,0,0))) # zero pixel

def test_scalar2qimage_normalize_domain():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = (-100, 100))
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    x = int(255 * 142.42 / 200.0)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(x,x,x)))
    x = int(255 *  90.0 / 200.0)
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(x,x,x)))
    x = int(255 * 100.0 / 200.0)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))

def test_scalar2qimage_normalize_dont_touch_0_255():
    a = numpy.zeros((100, 256), dtype = float)
    a[:] = numpy.arange(256)
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    b = qimage2ndarray.byte_view(qImg)
    assert numpy.all(a == b[...,0])

def test_scalar2qimage_masked():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    a[:,160:] = 100
    a = numpy.ma.masked_greater(a, 99)
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_ARGB32)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(255,255,255)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    x = int(255 * 10.0 / 52.42)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))
    assert_equal(QtGui.qAlpha(qImg.pixel(0,10)), 255)
    assert_equal(QtGui.qAlpha(qImg.pixel(200,10)), 0)

# --------------------------------------------------------------------

def test_rgb2qimage():
    a = numpy.zeros((240, 320, 3), dtype = float)
    a[12,10] = (42.42, 20, 14)
    a[13,10] = (-10, 0, -14)
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    assert_equal(hex(qImg.pixel(10,12)), hex(QtGui.qRgb(42,20,14)))
    assert_equal(hex(qImg.pixel(10,13)), hex(QtGui.qRgb(0,0,0)))
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(0,0,0)))

def test_rgb2qimage_normalize():
    a = numpy.zeros((240, 320, 3), dtype = float)
    a[12,10] = (42.42, 20, 14)
    a[13,10] = (-10, 20, 0)
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert_equal(qImg.width(), 320)
    assert_equal(qImg.height(), 240)
    assert_equal(qImg.format(), QtGui.QImage.Format_RGB32)
    assert_equal(hex(qImg.pixel(10,12)),
                 hex(QtGui.qRgb(255,(255*30.0/52.42),(255*24/52.42))))
    assert_equal(hex(qImg.pixel(10,13)),
                 hex(QtGui.qRgb(0,(255*30.0/52.42),(255*10/52.42))))
    x = int(255 * 10.0 / 52.42)
    assert_equal(hex(qImg.pixel(10,14)), hex(QtGui.qRgb(x,x,x)))       # zero pixel
