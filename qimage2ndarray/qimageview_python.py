'''Pure-python version of previously necessary C extension providing
read/write access to the memory of a QImage.

Over time, it became possible to get rid of the compiled extension on
all supported backends, so this is now used for all Qt python bindings.
'''

import numpy as np, sys
from qimage2ndarray.dynqt import qt, QtGui

def PyQt_data(image):
    # PyQt4/PyQt5's QImage.bits() returns a sip.voidptr that supports
    # conversion to string via asstring(size) or getting its base
    # address via int(...):
    return (int(image.bits()), False)

def _re_buffer_address_match(buf_repr):
    import re
    _re_buffer_address = re.compile('<read-write buffer ptr 0x([0-9a-fA-F]*),')
    global _re_buffer_address_match
    _re_buffer_address_match = _re_buffer_address.match
    return _re_buffer_address_match(buf_repr)

def PySide_data(image):
    # PySide's QImage.bits() returns a buffer object like this:
    # <read-write buffer ptr 0x7fc3f4821600, size 76800 at 0x111269570>
    ma = _re_buffer_address_match(repr(image.bits()))
    assert ma, 'could not parse address from %r' % (image.bits(), )
    return (int(ma.group(1), 16), False)

def direct_buffer_data(image):
    return image.bits()

# I would have preferred a more pythonic (duck-typing-like) approach
# based on introspection, but finding out which one of the above functions
# works at runtime is quite hard
getdata = {
    ('PyQt4', 2) : PyQt_data,
    ('PyQt5', 2) : PyQt_data,
    ('PySide', 2) : PySide_data,
    ('PySide2', 2) : PySide_data,
    ('PyQt4', 3) : PyQt_data,
    ('PyQt5', 3) : PyQt_data,
    ('PySide', 3) : direct_buffer_data,
    ('PySide2', 3) : direct_buffer_data,
    ('PythonQt', 3) : direct_buffer_data,
}[qt.name(), sys.version_info.major]


# how many bits do the different formats have?
FORMATS_BITS = dict(
    Format_Mono = 1,
    Format_MonoLSB = 1,
    Format_Indexed8 = 8,
    Format_RGB32 = 32,
    Format_ARGB32 = 32,
    Format_ARGB32_Premultiplied = 32,
    Format_RGB16 = 16,
    Format_ARGB8565_Premultiplied = 24,
    Format_RGB666 = 24,
    Format_ARGB6666_Premultiplied = 24,
    Format_RGB555 = 16,
    Format_ARGB8555_Premultiplied = 24,
    Format_RGB888 = 24,
    Format_RGB444 = 16,
    Format_ARGB4444_Premultiplied = 16,
    Format_RGBX8888 = 32,
    Format_RGBA8888 = 32,
    Format_RGBA8888_Premultiplied = 32,
    Format_BGR30 = 32,
    Format_A2BGR30_Premultiplied = 32,
    Format_RGB30 = 32,
    Format_A2RGB30_Premultiplied = 32,
    Format_Alpha8 = 8,
    Format_Grayscale8 = 8,
    Format_Grayscale16 = 16,
    Format_RGBX64 = 64,
    Format_RGBA64 = 64,
    Format_RGBA64_Premultiplied = 64,
)

    
VALIDFORMATS_8BIT = tuple(
    getattr(QtGui.QImage, name)
    for name, bits in FORMATS_BITS.items()
    if name in dir(QtGui.QImage) and bits == 8)
VALIDFORMATS_16BIT = tuple(
    getattr(QtGui.QImage, name)
    for name, bits in FORMATS_BITS.items()
    if name in dir(QtGui.QImage) and bits == 16)
VALIDFORMATS_24BIT = tuple(
    getattr(QtGui.QImage, name)
    for name, bits in FORMATS_BITS.items()
    if name in dir(QtGui.QImage) and bits == 24)
VALIDFORMATS_32BIT = tuple(
    getattr(QtGui.QImage, name)
    for name, bits in FORMATS_BITS.items()
    if name in dir(QtGui.QImage) and bits == 32)
VALIDFORMATS_64BIT = tuple(
    getattr(QtGui.QImage, name)
    for name, bits in FORMATS_BITS.items()
    if name in dir(QtGui.QImage) and bits == 64)

class ArrayInterfaceAroundQImage(object):
    __slots__ = ('__qimage', '__array_interface__')

    def __init__(self, image, bytes_per_pixel):
        self.__qimage = image

        bytes_per_line = image.bytesPerLine()

        self.__array_interface__ = dict(
            shape = (image.height(), image.width()),
            typestr = "|u%d" % bytes_per_pixel,
            data = getdata(image),
            strides = (bytes_per_line, bytes_per_pixel),
            version = 3,
        )
    
def qimageview(image):
    if not isinstance(image, QtGui.QImage):
        raise TypeError("image argument must be a QImage instance")

    pixel_format = image.format()
    if pixel_format in VALIDFORMATS_8BIT:
        bytes_per_pixel = 1
    elif pixel_format in VALIDFORMATS_16BIT:
        bytes_per_pixel = 2
#    elif pixel_format in VALIDFORMATS_24BIT:
#        bytes_per_pixel = 3
    elif pixel_format in VALIDFORMATS_32BIT:
        bytes_per_pixel = 4
    elif pixel_format in VALIDFORMATS_64BIT:
        bytes_per_pixel = 8
    elif pixel_format == QtGui.QImage.Format_Invalid:
        raise ValueError("qimageview got invalid QImage")
    else:
        raise ValueError("qimageview can only handle 8-, 16-, 32- or 64-bit QImages (format was %r)" % pixel_format)

    # introduce intermediate object referencing image
    # and providing array interface:
    temp = ArrayInterfaceAroundQImage(image, bytes_per_pixel)

    result = np.asarray(temp)
    return result
