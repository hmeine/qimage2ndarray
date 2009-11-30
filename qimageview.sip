// -*-c++-*-
%Module qimageview 0

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip

%ModuleCode
#include <Python.h>
#define PY_ARRAY_UNIQUE_SYMBOL qimageview_PyArray_API
#include <numpy/arrayobject.h>
%End

%PostInitialisationCode
import_array();
%End

SIP_PYOBJECT qimageview(QImage &image);
%MethodCode
{
	NPY_TYPES dtype = NPY_NOTYPE;

	npy_intp dims[2];
	dims[0] = a0->height();
	dims[1] = a0->width();

	npy_intp strides[2];
	strides[0] = a0->bytesPerLine();

	switch(a0->format())
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

	sipRes = PyArray_New(&PyArray_Type, 2, dims, dtype, strides, a0->bits(),
						 0/* itemsize (ignored) */, NPY_CARRAY, NULL);

	PyObject *image = PyTuple_GetItem(sipArgs, 0);
	PyArray_BASE(sipRes) = image;
	Py_INCREF(image);
}
%End
