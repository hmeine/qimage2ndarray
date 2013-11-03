import qimage2ndarray, os, numpy

from nose.tools import assert_equal
from nose.plugins.skip import SkipTest


def _locate_test_image(basename):
    result = os.path.join(os.path.dirname(__file__), basename)
    assert os.path.exists(result)
    return result


def test_imread_box():
    filename = _locate_test_image('test_box.png')

    gray = qimage2ndarray.imread(filename)

    assert_equal(gray.min(), 0)
    assert_equal(gray.max(), 255)

    assert_equal(numpy.ndim(gray), 2)

    assert_equal(gray.shape, (50, 111))

    
def test_imread_rgba():
    filename = _locate_test_image('test_colored_shadow.png')

    rgb = qimage2ndarray.imread(filename)

    assert_equal(rgb.min(), 0)
    assert_equal(rgb.max(), 255)

    assert_equal(numpy.ndim(rgb), 3)

    assert_equal(rgb.shape, (50, 111, 4))

    
def test_imread_gray():
    filename = _locate_test_image('test_gray.jpg')

    gray = qimage2ndarray.imread(filename)

    assert 200 < gray.max() <= 255

    assert_equal(numpy.ndim(gray), 2)

    assert_equal(gray.shape, (11, 16))


all_test_images = map(_locate_test_image, ['test_box.png', 'test_colored.jpg', 'test_gray.jpg',
                                           'test_colored_shadow.png'])#, 'test_box_shadow.png'])

def test_imread_against_scipy_ndimage():
    try:
        import scipy.ndimage
    except ImportError:
        raise SkipTest

    for filename in all_test_images:
        a = scipy.ndimage.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert_equal(a.shape, b.shape)
        assert numpy.all(a == b)

def test_imread_against_scipy_misc():
    try:
        import scipy.misc
    except ImportError:
        raise SkipTest

    for filename in all_test_images:
        a = scipy.misc.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert_equal(a.shape, b.shape)
        assert numpy.all(a == b)

def test_imread_against_matplotlib():
    try:
        import matplotlib.pyplot
    except ImportError:
        raise SkipTest

    for filename in all_test_images:
        a = matplotlib.pyplot.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert_equal(a.shape, b.shape)
        if a.max() == 1.0: # strange MPL API: only the PNG has 0..1.0 range
            a *= 255
        assert numpy.all(numpy.abs(a - b) < 1e-8)
