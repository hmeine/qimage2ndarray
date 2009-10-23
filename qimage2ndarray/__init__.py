import numpy as _np
from qimageview import qimageview as _qimageview

def raw_view(qimage):
	"""Returns raw 2D view of the given QImage's memory.  The result will be
	a 2-dimensional numpy.ndarray with an appropriately sized integral dtype."""
	return _qimageview(qimage)

def byte_view(qimage):
	"""Returns raw 3D view of the given QImage's memory.  This will be
	a 3-dimensional numpy.ndarray with dtype numpy.uint8."""
	raw = _qimageview(qimage)
	return raw.view(_np.uint8).reshape(raw.shape + (-1, ))
