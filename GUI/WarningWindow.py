# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WarningWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName(_fromUtf8("Window"))
        Window.resize(383, 124)
        self.horizontalLayoutWidget = QtGui.QWidget(Window)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 381, 121))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.warning_pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.warning_pushButton.setObjectName(_fromUtf8("warning_pushButton"))
        self.gridLayout.addWidget(self.warning_pushButton, 1, 0, 1, 1)
        self.warning_Label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.warning_Label.setText(_fromUtf8(""))
        self.warning_Label.setObjectName(_fromUtf8("warning_Label"))
        self.gridLayout.addWidget(self.warning_Label, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        Window.setWindowTitle(_translate("Window", "Warning", None))
        self.warning_pushButton.setText(_translate("Window", "Close", None))

