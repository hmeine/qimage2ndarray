import qimage2ndarray, os, numpy

import pytest


def _locate_test_image(basename):
    result = os.path.join(os.path.dirname(__file__), basename)
    assert os.path.exists(result)
    return result


def test_imread_file_not_found():
    filename = 'non_existing_image_file.png'

    with pytest.raises(IOError):
        qimage2ndarray.imread(filename)


def test_imread_box():
    filename = _locate_test_image('test_box.png')

    gray = qimage2ndarray.imread(filename)

    assert gray.min() == 0
    assert gray.max() == 255

    assert numpy.ndim(gray) == 2

    assert gray.shape == (50, 111)

    
def test_imread_rgba():
    filename = _locate_test_image('test_colored_shadow.png')

    rgb = qimage2ndarray.imread(filename)

    assert rgb.min() == 0
    assert rgb.max() == 255

    assert numpy.ndim(rgb) == 3

    assert rgb.shape == (50, 111, 4)

    
def test_imread_gray():
    filename = _locate_test_image('test_gray.jpg')

    gray = qimage2ndarray.imread(filename)

    assert 200 < gray.max() <= 255

    assert numpy.ndim(gray) == 2

    assert gray.shape == (11, 16)


def test_imread_gray_alpha():
    filename = _locate_test_image('test_box_shadow.png')

    gray = qimage2ndarray.imread(filename)

    assert 200 < gray.max() <= 255

    assert numpy.ndim(gray) == 3

    assert gray.shape == (50, 111, 2)


def test_imread_masked():
    filename = _locate_test_image('test_box_shadow.png')

    gray = qimage2ndarray.imread(filename, masked = True)

    assert 200 < gray.max() <= 255

    assert numpy.ndim(gray) == 2

    assert gray.shape == (50, 111)

    assert numpy.ma.is_masked(gray)

    masked_count = gray.mask.sum()
    assert 0 < masked_count < numpy.product(gray.shape)
    assert masked_count == 1464


def test_imread_masked_no_alpha():
    filename = _locate_test_image('test_gray.jpg')

    gray = qimage2ndarray.imread(filename, masked = True)

    assert 200 < gray.max() <= 255

    assert numpy.ndim(gray) == 2

    assert gray.shape == (11, 16)

    assert not numpy.ma.is_masked(gray)


all_test_images = map(_locate_test_image, ['test_box.png', 'test_colored.jpg', 'test_gray.jpg',
                                           'test_colored_shadow.png'])

def test_imread_against_scipy_ndimage():
    try:
        import scipy.ndimage
    except ImportError:
        pytest.skip('scipy.ndimage not installed')

    for filename in all_test_images:
        a = scipy.ndimage.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert a.shape == b.shape
        assert numpy.all(a == b)

def test_imread_against_scipy_misc():
    try:
        import scipy.misc
    except ImportError:
        pytest.skip('scipy.misc not installed')

    for filename in all_test_images:
        a = scipy.misc.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert a.shape == b.shape
        assert numpy.all(a == b)

def test_imread_against_matplotlib():
    try:
        import matplotlib.pyplot
    except ImportError:
        pytest.skip('matplotlib not installed')

    for filename in all_test_images:
        a = matplotlib.pyplot.imread(filename)
        b = qimage2ndarray.imread(filename)
        assert a.shape == b.shape
        if a.max() == 1.0: # strange MPL API: only the PNG has 0..1.0 range
            a *= 255
        assert numpy.all(numpy.abs(a - b) < 1e-8)
