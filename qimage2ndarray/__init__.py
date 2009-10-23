from qimageview import qimageview as _qimageview

def raw_view(qimage):
	"""Returns raw view of the given QImage's memory.  This will be a
	2D numpy.ndarray with an appropriately sized integral dtype."""
	return _qimageview(qimage)
