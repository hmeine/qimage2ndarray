import qimage2ndarray
from PyQt4 import QtGui

from nose.tools import raises, assert_equal

def test_raw_indexed8():
	qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
	qimg.setNumColors(256)
	qimg.fill(0)
	v = qimage2ndarray.raw_view(qimg)
	qimg.fill(23)
	qimg.setPixel(12, 10, 42)
	assert_equal(v.shape, (240, 320))
	assert_equal(v[10,10], 23)
	assert_equal(v[10,12], 42)
	assert_equal(v.nbytes, qimg.numBytes())

def test_raw_rgb32():
	qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
	qimg.fill(0)
	v = qimage2ndarray.raw_view(qimg)
	qimg.fill(23)
	qimg.setPixel(12, 10, 42)
	assert_equal(v.shape, (240, 320))
	assert_equal(v[10,10], 23 | 0xff000000)
	assert_equal(v[10,12], 42 | 0xff000000)
	assert_equal(v.nbytes, qimg.numBytes())

def test_byte_view_rgb32():
	qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
	v = qimage2ndarray.byte_view(qimg)
	qimg.fill(23)
	qimg.setPixel(12, 10, 42)
	assert_equal(v.shape, (240, 320, 4))
	assert_equal(list(v[10,10]), [23, 0, 0, 0xff])
	assert_equal(list(v[10,12]), [42, 0, 0, 0xff])
	assert_equal(v.nbytes, qimg.numBytes())

def test_rgb_view():
	qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_RGB32)
	qimg.fill(23)
	v = qimage2ndarray.rgb_view(qimg)
	qimg.setPixel(12, 10, QtGui.qRgb(12,34,56))
	assert_equal(list(v[10,12]), [12,34,56])

def test_recarray_view():
	qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_ARGB32)
	qimg.fill(23)
	v = qimage2ndarray.recarray_view(qimg)
	qimg.setPixel(12, 10, QtGui.qRgb(12,34,56))
	assert_equal(v["g"][10,12], 34)
	assert_equal(v["g"].sum(), 34)
	assert_equal(v["green"].sum(), 34)
	assert_equal(v[10,12]["g"], 34)
	assert_equal(v.g[10,12], 34)
