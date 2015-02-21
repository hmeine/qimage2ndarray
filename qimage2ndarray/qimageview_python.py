import numpy as np
from qimage2ndarray.dynqt import qt, QtGui

def PyQtX_data(image):
    # PyQtX's QImage.bits() returns a sip.voidptr that supports
    # conversion to string via asstring(size) or getting its base
    # address via int(...):
    return (int(image.bits()), False)

def _re_buffer_address_match(buf_repr):
    import re
    _re_buffer_address = re.compile('<read-write buffer ptr 0x([0-9a-f]*),')
    global _re_buffer_address_match
    _re_buffer_address_match = _re_buffer_address.match
    return _re_buffer_address_match(buf_repr)

def PySide_data(image):
    # PySide's QImage.bits() returns a buffer object like this:
    # <read-write buffer ptr 0x7fc3f4821600, size 76800 at 0x111269570>
    ma = _re_buffer_address_match(repr(image.bits()))
    assert ma, 'could not parse address from %r' % (image.bits(), )
    return (int(ma.group(1), 16), False)

getdata = dict(PyQt4 = PyQtX_data,
               PyQt5 = PyQtX_data,
               PySide = PySide_data,)[qt.name()]


def qimageview(image):
    if not isinstance(image, QtGui.QImage):
        raise TypeError("image argument must be a QImage instance")

    shape = image.height(), image.width()
    strides0 = image.bytesPerLine()

    format = image.format()
    if format == QtGui.QImage.Format_Indexed8:
        dtype = "|u1"
        strides1 = 1
    elif format in (QtGui.QImage.Format_RGB32,
    QtGui.QImage.Format_ARGB32,
    QtGui.QImage.Format_ARGB32_Premultiplied):
        dtype = "|u4"
        strides1 = 4
    elif format == QtGui.QImage.Format_Invalid:
        raise ValueError("qimageview got invalid QImage")
    else:
        raise ValueError("qimageview can only handle 8- or 32-bit QImages")

    image.__array_interface__ = {
        'shape': shape,
        'typestr': dtype,
        'data': getdata(image),
        'strides': (strides0, strides1),
        'version': 3,
    }

    result = np.asarray(image)
    del image.__array_interface__
    return result
