import qimageview
from PyQt4 import QtGui

from nose.tools import raises

qimg = QtGui.QImage(320, 240, QtGui.QImage.Format_Indexed8)

def test_qimageview():
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
