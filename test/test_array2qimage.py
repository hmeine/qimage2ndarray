import qimage2ndarray, numpy
from qimage2ndarray.dynqt import QtGui

from compat import numBytes, numColors


def test_gray2qimage():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_Indexed8
    assert a.nbytes == numBytes(qImg) * a.itemsize
    assert numColors(qImg) == 256
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(42,42,42))
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(0,0,0))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))

def test_bool2qimage_normalize():
    a = numpy.zeros((240, 320), dtype = bool)
    a[12,10] = True
    # normalization should scale to 0/255
    # (not raise a numpy exception, see issue #17)
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,255,255))
    assert hex(qImg.pixel(0,0)) == hex(QtGui.qRgb(0,0,0))
    a[:] = True
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    # for boolean arrays, I would assume True should always map to 255
    assert hex(qImg.pixel(0,0)) == hex(QtGui.qRgb(255,255,255))

def test_gray2qimage_normalize():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_Indexed8
    assert a.nbytes == numBytes(qImg) * a.itemsize
    assert numColors(qImg) == 256
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,255,255))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    x = int(255 * 10.0 / 52.42)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))

def test_arrayqimage_readonly_float_normalizing():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    a.flags['WRITEABLE'] = False
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)

def test_arrayqimage_readonly_float():
    a = numpy.zeros((240, 320), dtype = float)
    a.flags['WRITEABLE'] = False
    qImg = qimage2ndarray.gray2qimage(a, normalize = False)

def test_arrayqimage_readonly_uint8():
    a = numpy.zeros((240, 320), dtype = numpy.uint8)
    a.flags['WRITEABLE'] = False
    qImg = qimage2ndarray.gray2qimage(a, normalize = False)

def test_empty2qimage():
    a = numpy.ones((240, 320), dtype = float)
    qImg = qimage2ndarray.gray2qimage(a, normalize = True)
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))

def test_gray2qimage_normalize_onlymax():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = 80)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_Indexed8
    assert a.nbytes == numBytes(qImg) * a.itemsize
    assert numColors(qImg) == 256
    x = int(255 * 42.42 / 80.0)
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(x,x,x))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(0,0,0))

def test_gray2qimage_normalize_domain():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.gray2qimage(a, normalize = (-100, 100))
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_Indexed8
    assert a.nbytes == numBytes(qImg) * a.itemsize
    assert numColors(qImg) == 256
    x = int(255 * 142.42 / 200.0)
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(x,x,x))
    x = int(255 *  90.0 / 200.0)
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(x,x,x))
    x = int(255 * 100.0 / 200.0)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))

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
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_Indexed8
    assert a.nbytes == numBytes(qImg) * a.itemsize
    assert numColors(qImg) == 256
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,255,255))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    x = int(255 * 10.0 / 52.42)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))
    assert QtGui.qAlpha(qImg.pixel(0,10)) == 255
    assert QtGui.qAlpha(qImg.pixel(200,10)) == 0

# --------------------------------------------------------------------

def test_scalar2qimage():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(42,42,42)) # max pixel
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(0,0,0))    # zero pixel
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))    # min pixel

def test_scalar2qimage_with_alpha():
    a = numpy.zeros((240, 320, 2), dtype = float)
    a[...,1] = 255
    a[12,10] = (42.42, 128)
    a[13,10] = (-10, 0)
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_ARGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgba(42,42,42,128)) # max pixel
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgba(0,0,0,255))    # zero pixel
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgba(0,0,0,0))      # min pixel

def test_scalar2qimage_normalize():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,255,255)) # max pixel
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))       # min pixel
    x = int(255 * 10.0 / 52.42)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))       # zero pixel

def test_scalar2qimage_normalize_onlymax():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = 80)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    x = int(255 * 42.42 / 80.0)
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(x,x,x)) # max pixel
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0)) # min pixel
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(0,0,0)) # zero pixel

def test_scalar2qimage_normalize_domain():
    a = numpy.zeros((240, 320), dtype = float)
    a[12,10] = 42.42
    a[13,10] = -10
    qImg = qimage2ndarray.array2qimage(a, normalize = (-100, 100))
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    x = int(255 * 142.42 / 200.0)
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(x,x,x))
    x = int(255 *  90.0 / 200.0)
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(x,x,x))
    x = int(255 * 100.0 / 200.0)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))

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
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_ARGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,255,255))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    x = int(255 * 10.0 / 52.42)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))
    assert QtGui.qAlpha(qImg.pixel(0,10)) == 255
    assert QtGui.qAlpha(qImg.pixel(200,10)) == 0

# --------------------------------------------------------------------

def test_rgb2qimage():
    a = numpy.zeros((240, 320, 3), dtype = float)
    a[12,10] = (42.42, 20, 14)
    a[13,10] = (-10, 0, -14)
    qImg = qimage2ndarray.array2qimage(a)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(42,20,14))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,0,0))
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(0,0,0))

def test_rgb2qimage_normalize():
    a = numpy.zeros((240, 320, 3), dtype = float)
    a[12,10] = (42.42, 20, 14)
    a[13,10] = (-10, 20, 0)
    qImg = qimage2ndarray.array2qimage(a, normalize = True)
    assert not qImg.isNull()
    assert qImg.width() == 320
    assert qImg.height() == 240
    assert qImg.format() == QtGui.QImage.Format_RGB32
    assert hex(qImg.pixel(10,12)) == hex(QtGui.qRgb(255,(255*30.0//52.42),(255*24//52.42)))
    assert hex(qImg.pixel(10,13)) == hex(QtGui.qRgb(0,(255*30.0//52.42),(255*10//52.42)))
    x = int(255 * 10.0 / 52.42)
    assert hex(qImg.pixel(10,14)) == hex(QtGui.qRgb(x,x,x))       # zero pixel
