# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow2.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(390, 159)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 381, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(10, 70, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.nextFrame_button = QtGui.QPushButton(self.groupBox)
        self.nextFrame_button.setGeometry(QtCore.QRect(280, 30, 86, 25))
        self.nextFrame_button.setObjectName(_fromUtf8("nextFrame_button"))
        self.prevFrame_button = QtGui.QPushButton(self.groupBox)
        self.prevFrame_button.setGeometry(QtCore.QRect(10, 30, 86, 25))
        self.prevFrame_button.setObjectName(_fromUtf8("prevFrame_button"))
        self.playPause_button = QtGui.QPushButton(self.groupBox)
        self.playPause_button.setGeometry(QtCore.QRect(100, 30, 86, 25))
        self.playPause_button.setObjectName(_fromUtf8("playPause_button"))
        self.stop_button = QtGui.QPushButton(self.groupBox)
        self.stop_button.setGeometry(QtCore.QRect(190, 30, 86, 25))
        self.stop_button.setObjectName(_fromUtf8("stop_button"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuColors = QtGui.QMenu(self.menubar)
        self.menuColors.setObjectName(_fromUtf8("menuColors"))
        self.menuSimulation = QtGui.QMenu(self.menubar)
        self.menuSimulation.setObjectName(_fromUtf8("menuSimulation"))
        self.menuGraph = QtGui.QMenu(self.menubar)
        self.menuGraph.setObjectName(_fromUtf8("menuGraph"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_File = QtGui.QAction(MainWindow)
        self.actionSave_File.setObjectName(_fromUtf8("actionSave_File"))
        self.action_omf_file = QtGui.QAction(MainWindow)
        self.action_omf_file.setObjectName(_fromUtf8("action_omf_file"))
        self.action_ohf_file = QtGui.QAction(MainWindow)
        self.action_ohf_file.setObjectName(_fromUtf8("action_ohf_file"))
        self.actionLoad_File = QtGui.QAction(MainWindow)
        self.actionLoad_File.setObjectName(_fromUtf8("actionLoad_File"))
        self.actionLoad_Data = QtGui.QAction(MainWindow)
        self.actionLoad_Data.setObjectName(_fromUtf8("actionLoad_Data"))
        self.actionShow_3D_Model = QtGui.QAction(MainWindow)
        self.actionShow_3D_Model.setObjectName(_fromUtf8("actionShow_3D_Model"))
        self.actionShow_Range_Plot = QtGui.QAction(MainWindow)
        self.actionShow_Range_Plot.setObjectName(_fromUtf8("actionShow_Range_Plot"))
        self.actionShow_2D_layer_Plot = QtGui.QAction(MainWindow)
        self.actionShow_2D_layer_Plot.setObjectName(_fromUtf8("actionShow_2D_layer_Plot"))
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addAction(self.actionLoad_File)
        self.menuFile.addAction(self.actionLoad_Data)
        self.menuFile.addSeparator()
        self.menuSimulation.addAction(self.actionShow_3D_Model)
        self.menuGraph.addAction(self.actionShow_Range_Plot)
        self.menuGraph.addAction(self.actionShow_2D_layer_Plot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuColors.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuGraph.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Simulation", None))
        self.nextFrame_button.setText(_translate("MainWindow", ">>", None))
        self.prevFrame_button.setText(_translate("MainWindow", "<<", None))
        self.playPause_button.setText(_translate("MainWindow", "Play", None))
        self.stop_button.setText(_translate("MainWindow", "Stop", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuColors.setTitle(_translate("MainWindow", "Colors", None))
        self.menuSimulation.setTitle(_translate("MainWindow", "Simulation", None))
        self.menuGraph.setTitle(_translate("MainWindow", "Plot", None))
        self.actionSave_File.setText(_translate("MainWindow", "Save File", None))
        self.action_omf_file.setText(_translate("MainWindow", ".omf file", None))
        self.action_ohf_file.setText(_translate("MainWindow", ".ohf file", None))
        self.actionLoad_File.setText(_translate("MainWindow", "Load File", None))
        self.actionLoad_Data.setText(_translate("MainWindow", "Load Directory", None))
        self.actionShow_3D_Model.setText(_translate("MainWindow", "Show 3D Model", None))
        self.actionShow_Range_Plot.setText(_translate("MainWindow", "Show Range Plot", None))
        self.actionShow_2D_layer_Plot.setText(_translate("MainWindow", "Show 2D layer Plot", None))

