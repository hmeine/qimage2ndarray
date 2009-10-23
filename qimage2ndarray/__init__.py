import numpy as _np
from qimageview import qimageview as _qimageview

bgra_dtype = _np.dtype({'b': (_np.uint8, 0, 'blue'),
						'g': (_np.uint8, 1, 'green'),
						'r': (_np.uint8, 2, 'red'),
						'a': (_np.uint8, 3, 'alpha')})

def raw_view(qimage):
	"""Returns raw 2D view of the given QImage's memory.  The result will be
	a 2-dimensional numpy.ndarray with an appropriately sized integral dtype."""
	return _qimageview(qimage)

def byte_view(qimage):
	"""Returns raw 3D view of the given QImage's memory.  This will be
	a 3-dimensional numpy.ndarray with dtype numpy.uint8.  Note that
	due to QImage's memory layout, the last dimension will be in the
	[B,G,R,A] order for 32-bit images."""
	raw = _qimageview(qimage)
	return raw.view(_np.uint8).reshape(raw.shape + (-1, ))

def rgb_view(qimage):
	"""Returns RGB view of a given 32-bit color QImage's memory.
	Similarly to byte_view(), the result is a 3D numpy.uint8 array,
	but reduced to the rgb dimensions (without alpha), and reordered
	(using negative strides in the last dimension) to have the usual
	[R,G,B] order.  The image must have 32 bit pixel size, i.e. be
	RGB32, ARGB32, or ARGB32_Premultiplied.  (Note that in the latter
	case, the values are of course premultiplied with alpha.)"""
	bytes = byte_view(qimage)
	if bytes.shape[2] != 4:
		raise ValueError, "For rgb_view, the image must have 32 bit pixel size (use RGB32, ARGB32, or ARGB32_Premultiplied)"
	return bytes[...,2::-1]

def recarray_view(qimage):
	"""Returns recarray view of a given 32-bit color QImage's memory.

	The result is a 2D array with a complex record dtype, offering the
	named fields 'r','g','b', and 'a' and corresponding long names.
	Thus, each color components can be accessed either via string
	indexing or via attribute lookup (through numpy.recarray):

	>>> from PyQt4.QtGui import QImage, qRgb
	>>> qimg = QImage(320, 240, QImage.Format_ARGB32)
	>>> qimg.fill(qRgb(12,34,56))
	>>>
	>>> import qimage2ndarray
	>>> v = qimage2ndarray.recarray_view(qimg)
	>>>
	>>> red = v["r"]
	>>> red[10,10]
	12
	>>> pixel = v[10,10]
	>>> pixel["r"]
	12
	>>> (v.g == v["g"]).all()
	True
	>>> (v.alpha == 255).all()
	True"""
	raw = _qimageview(qimage)
	if raw.itemsize != 4:
		raise ValueError, "For rgb_view, the image must have 32 bit pixel size (use RGB32, ARGB32, or ARGB32_Premultiplied)"
	return raw.view(bgra_dtype, _np.recarray)
