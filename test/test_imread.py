import qimage2ndarray, os, numpy
from PyQt4 import QtGui

from nose.tools import raises, assert_equal

def test_imread_box():
    filename = os.path.join(os.path.dirname(__file__), 'test_box.png')
    assert os.path.exists(filename)

    gray = qimage2ndarray.imread(filename)

    assert_equal(gray.min(), 0)
    assert_equal(gray.max(), 255)

    assert_equal(numpy.ndim(gray), 2)

    assert_equal(gray.shape, (50, 111))

    
def test_imread_colored():
    filename = os.path.join(os.path.dirname(__file__), 'test_colored.jpg')
    assert os.path.exists(filename)

    rgb = qimage2ndarray.imread(filename)

    assert_equal(rgb.min(), 0)
    assert_equal(rgb.max(), 255)

    assert_equal(numpy.ndim(rgb), 3)

    assert_equal(rgb.shape, (11, 16, 3))

    
def test_imread_colored():
    filename = os.path.join(os.path.dirname(__file__), 'test_gray.jpg')
    assert os.path.exists(filename)

    gray = qimage2ndarray.imread(filename)

    assert 200 < gray.max() <= 255

    assert_equal(numpy.ndim(gray), 2)

    assert_equal(gray.shape, (11, 16))
