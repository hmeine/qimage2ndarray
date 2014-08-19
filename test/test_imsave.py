import qimage2ndarray, os, numpy, tempfile

from nose.tools import assert_equal
from test_imread import all_test_images, _locate_test_image

def test_imsave():
    fh, tempFilename = tempfile.mkstemp('.png')
    os.close(fh)
    try:
        for filename in all_test_images:
            filename = _locate_test_image(filename)
            a = qimage2ndarray.imread(filename)
            ok = qimage2ndarray.imsave(tempFilename, a)
            assert ok
            b = qimage2ndarray.imread(tempFilename)
            assert_equal(a.shape, b.shape)
            assert numpy.all(a == b)
    finally:
        #os.unlink(tempFilename)
        print tempFilename
