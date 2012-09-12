// -*-c++-*-
%Module(name = qimageview, version = 0)

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip

%ModuleCode
#include <Python.h>
#define PY_ARRAY_UNIQUE_SYMBOL qimageview_PyArray_API
#include <qimageview.h>
%End

%PostInitialisationCode
import_array();
%End

SIP_PYOBJECT qimageview(QImage &image);
%MethodCode
{
	PyObject *view = qimageview(*a0, PyTuple_GetItem(sipArgs, 0));
	if(!view)
		return NULL;

	sipRes = view;
}
%End
