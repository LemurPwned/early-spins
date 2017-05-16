from PyQt4 import QtGui, QtCore
import sys
import os

from GUI.MainWindow import Ui_MainWindow
from CPU3D import pyglet1

class MainScreen(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        
        self.worker = WorkerObject()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        
        self.window()

    def window(self):
        self.headerFile = ""
        self.directory = ""
        self.fformat = ""
        
        #LAYOUT
        self.playPause_button.clicked.connect(self.playPause)
        self.stop_button.clicked.connect(self.stop)
        self.nextFrame_button.clicked.connect(self.nextFrame)
        self.prevFrame_button.clicked.connect(self.prevFrame)

        #MENU
        self.actionLoad_File.triggered.connect(self.loadSingleFile)
        self.actionLoad_Data.triggered.connect(self.loadDirectory)
        self.actionLoad_Header_File.triggered.connect(self.loadHeader)
        self.actionShow_3D_Model.triggered.connect(self.load3Dsim)
        


    def loadSingleFile(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
		
    def loadDirectory(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
        self.directory = filename[:filename.rfind("/")+1]
        self.fformat = filename[filename.rfind("."):]
        self.directory_lineEdit.setText(self.directory)
        self.format_value_label.setText(self.fformat)
        
        tFileList = os.listdir(self.directory)
        c = 0
        for f in tFileList:
            #print(f)
            if(f[f.rfind("."):]==self.fformat):
                c+=1
        
        self.number_of_files_value_label.setText(str(c))
	
    def loadHeader(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
        self.headerFile = filename
        self.header_file_lineEdit.setText(self.headerFile)
	
    def load3Dsim(self):
        if self.headerFile == "":
            #TODO error
            pass
        
        if self.directory == "":
            #TODO error
            pass
        
        pyglet1.simulateDirectory(self.directory, self.fformat, self.headerFile)
	
	
    #INSTEAD OF THESE WE WILL GIVE OUR FUNCTIONS!
    def playPause(self):
        print("Play")

    def stop(self):
        print("Stop")

    def nextFrame(self):
        print("next frame")

    def prevFrame(self):
        print("prev frame")
    #INSTEAD OF THESE WE WILL GIVE OUR FUNCTIONS!

class WorkerObject(QtCore.QObject):

    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
    
    def startWork(self):
        for i in range(1000):
            print("test")
            tm.sleep(1)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainScreen()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
	main()
