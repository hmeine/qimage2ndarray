import qimage2ndarray, numpy
from PyQt4 import QtGui

from nose.tools import raises, assert_equal

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

