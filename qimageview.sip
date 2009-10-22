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
	NPY_TYPES dtype = NPY_UINT8;
	npy_intp dims[2];
	dims[0] = a0->height();
	dims[1] = a0->width();
	sipRes = PyArray_SimpleNewFromData(2, dims, dtype, a0->bits());
}
%End
