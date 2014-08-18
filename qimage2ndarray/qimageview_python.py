import numpy as np
from PyQt4 import QtGui
from PyQt4.QtGui import QImage


def qimageview(image):
    if not isinstance(image, QImage):
        raise TypeError("image argument must be a QImage instance")

    shape = image.height(), image.width()
    strides0 = image.bytesPerLine()

    format = image.format()
    if format == QImage.Format_Indexed8:
        dtype = "|u1"
        strides1 = 1
    elif format in (QImage.Format_RGB32, QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied):
        dtype = "|u4"
        strides1 = 4
    elif format == QImage.Format_Invalid:
        raise ValueError("qimageview got invalid QImage")
    else:
        raise ValueError("qimageview can only handle 8- or 32-bit QImages")

    image.__array_interface__ = {
        '__ref': image,
        'shape': shape,
        'data': (int(image.bits()), False),
        'strides': (strides0, strides1),
        'typestr': dtype,
    }

    arr = np.array(image, copy=False)
    del image.__array_interface__
    return arr
