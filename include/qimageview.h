// ATTENTION: make sure to handle PY_ARRAY_UNIQUE_SYMBOL before including qimageview.h!
#include <numpy/arrayobject.h>
#include <QtGui/QImage>

PyObject *qimageview(QImage &image, PyObject *imageWrapper)
{
	NPY_TYPES dtype = NPY_NOTYPE;

	npy_intp dims[2];
	dims[0] = image.height();
	dims[1] = image.width();

	npy_intp strides[2];
	strides[0] = image.bytesPerLine();

	switch(image.format())
	{
	case QImage::Format_Indexed8:
		dtype = NPY_UINT8;
		strides[1] = 1;
		break;
	case QImage::Format_RGB32:
	case QImage::Format_ARGB32:
	case QImage::Format_ARGB32_Premultiplied:
		dtype = NPY_UINT32;
		strides[1] = 4;
		break;
	case QImage::Format_Invalid:
        PyErr_SetString(PyExc_ValueError,
                        "qimageview got invalid QImage");
		return NULL;
	default:
        PyErr_SetString(PyExc_ValueError,
                        "qimageview can only handle 8- or 32-bit QImages");
		return NULL;
	}

	PyObject *result = PyArray_New(&PyArray_Type, 2, dims, dtype, strides, image.bits(),
								   0/* itemsize (ignored) */, NPY_CARRAY, NULL);

	PyArray_BASE(result) = imageWrapper;
	Py_INCREF(imageWrapper);

	return result;
}
