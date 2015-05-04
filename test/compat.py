

def setNumColors(qimage, color_count):
    """Compatibility function btw. PyQt4 and PyQt5"""

    try:
        qimage.setNumColors(color_count)
    except AttributeError:
        qimage.setColorCount(color_count)


def numBytes(qimage):
    """Compatibility function btw. PyQt4 and PyQt5"""

    try:
        return qimage.numBytes()
    except AttributeError:
        return qimage.byteCount()


def numColors(qimage):
    """Compatibility function btw. PyQt4 and PyQt5"""

    try:
        return qimage.numColors()
    except AttributeError:
        return qimage.colorCount()
