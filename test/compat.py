

def setColorCount(qimage, color_count):
    """Compatibility function btw. Qt4 and Qt5"""

    try:
        qimage.setColorCount(color_count) # Qt 4.6 and later
    except AttributeError:
        qimage.setNumColors(color_count)


def colorCount(qimage):
    """Compatibility function btw. Qt4 and Qt5"""

    try:
        return qimage.colorCount() # Qt 4.6 and later
    except AttributeError:
        return qimage.numColors()


def sizeInBytes(qimage):
    """Compatibility function btw. Qt4, Qt5, and Qt6"""

    try:
        return qimage.sizeInBytes() # Qt 5.10 and later
    except AttributeError:
        try:
            return qimage.byteCount() # Qt 4.6 and later
        except AttributeError:
            return qimage.numBytes()


# deprecated name for backwards compatibility
setNumColors = setColorCount
numColors = colorCount
numBytes = sizeInBytes
