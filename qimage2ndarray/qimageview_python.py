'''Pure-python version of previously necessary C extension providing
read/write access to the memory of a QImage.

Over time, it became possible to get rid of the compiled extension on
all supported backends, so this is now used for all Qt python bindings.
'''

import sys
import numpy as np
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


# what properties (e.g., how many bits) do the different formats have?
class QImageFormat:
    def __init__(self, bits, rgb_layout = None):
        self.code = None
        self.bits = bits
        self.rgb_layout = rgb_layout

    @staticmethod
    def from_code(code):
        for _name, qimage_format in FORMATS.items():
            if qimage_format.code == code:
                return qimage_format

FORMATS = dict(
    Format_Mono = QImageFormat(1),
    Format_MonoLSB = QImageFormat(1),
    Format_Indexed8 = QImageFormat(8),
    Format_RGB32 = QImageFormat(32, rgb_layout = 'argb32'),
    Format_ARGB32 = QImageFormat(32, rgb_layout = 'argb32'),
    Format_ARGB32_Premultiplied = QImageFormat(32, rgb_layout = 'argb32'),
    Format_RGB16 = QImageFormat(16),
    Format_ARGB8565_Premultiplied = QImageFormat(24),
    Format_RGB666 = QImageFormat(24),
    Format_ARGB6666_Premultiplied = QImageFormat(24),
    Format_RGB555 = QImageFormat(16),
    Format_ARGB8555_Premultiplied = QImageFormat(24),
    Format_RGB888 = QImageFormat(24, rgb_layout = 'rgb888'),
    Format_RGB444 = QImageFormat(16),
    Format_ARGB4444_Premultiplied = QImageFormat(16),
    Format_RGBX8888 = QImageFormat(32, rgb_layout = 'rgba8888'),
    Format_RGBA8888 = QImageFormat(32, rgb_layout = 'rgba8888'),
    Format_RGBA8888_Premultiplied = QImageFormat(32, rgb_layout = 'rgba8888'),
    Format_BGR30 = QImageFormat(32),
    Format_A2BGR30_Premultiplied = QImageFormat(32),
    Format_RGB30 = QImageFormat(32),
    Format_A2RGB30_Premultiplied = QImageFormat(32),
    Format_Alpha8 = QImageFormat(8),
    Format_Grayscale8 = QImageFormat(8),
    Format_Grayscale16 = QImageFormat(16),
    Format_RGBX64 = QImageFormat(64),
    Format_RGBA64 = QImageFormat(64),
    Format_RGBA64_Premultiplied = QImageFormat(64),
)

for name, qimage_format in FORMATS.items():
    if name in dir(QtGui.QImage):
        qimage_format.code = getattr(QtGui.QImage, name)

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
    if pixel_format == QtGui.QImage.Format_Invalid:
        raise ValueError("qimageview got invalid QImage")
    
    qimage_format = QImageFormat.from_code(pixel_format)
    if qimage_format.bits not in (8, 16, 32, 64):
        raise ValueError("qimageview can only handle 8-, 16-, 32- or 64-bit QImages (format was %r)" % pixel_format)

    # introduce intermediate object referencing image
    # and providing array interface:
    temp = ArrayInterfaceAroundQImage(image, qimage_format.bits // 8)

    result = np.asarray(temp)
    return result
