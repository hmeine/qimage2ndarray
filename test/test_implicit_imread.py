import qimage2ndarray, os, numpy

from test_imread import all_test_images, _locate_test_image

def test_byte_view():
    for filename in all_test_images:
        assert isinstance(qimage2ndarray.byte_view(filename), numpy.ndarray)


def test_raw_view():
    for filename in all_test_images:
        assert isinstance(qimage2ndarray.raw_view(filename), numpy.ndarray)


def test_color_views():
    filename = _locate_test_image('test_colored.jpg')
    for view in (qimage2ndarray.alpha_view,
                 qimage2ndarray.rgb_view,
                 qimage2ndarray.recarray_view):
        assert isinstance(view(filename), numpy.ndarray)
