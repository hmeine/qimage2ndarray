import qimageview
from PyQt4 import QtGui

from nose.tools import raises

qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)
qimg.setNumColors(256)

def test_viewcreation():
	v = qimageview.qimageview(qimg)
	assert v.shape == (240, 320)

@raises(TypeError)
def test_qimageview_noargs():
	v = qimageview.qimageview()

@raises(TypeError)
def test_qimageview_manyargs():
	v = qimageview.qimageview(qimg, 1)

@raises(TypeError)
def test_qimageview_wrongarg():
	v = qimageview.qimageview(42)

def test_data_access():
	qimg.fill(42)
	v = qimageview.qimageview(qimg)
	assert v.shape == (240, 320)
	assert v[10,10] == 42

def test_being_view():
	qimg.fill(23)
	v = qimageview.qimageview(qimg)
	qimg.fill(42)
	assert v.shape == (240, 320)
	assert v[10,10] == 42

def test_coordinate_access():
	qimg.fill(0)
	qimg.setPixel(12, 10, 42)
	v = qimageview.qimageview(qimg)
	qimg.fill(42)
	assert v.shape == (240, 320)
	assert v[10,12] == 42
