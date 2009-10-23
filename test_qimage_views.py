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

