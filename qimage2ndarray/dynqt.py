from .qt_driver import QtDriver

qt = QtDriver()
QtGui = qt.QtGui

QImage_Format = (
    QtGui.QImage if 'Format_Indexed8' in dir(QtGui.QImage) else QtGui.QImage.Format)
