from PyQt4 import QtGui, QtCore
import sys
import os

from GUI.MainWindow import Ui_MainWindow
#from GUI.WarningWindow import Ui_Window
from GUI.warning import WarningScreen

from CPU3D import pygletRunner

class MainScreen(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)

        self.worker = pygletRunner.PygletRunner()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        


        self.window()

    def window(self):
        self.headerFile = ""
        self.directory = ""
        self.fformat = ""
        self.filetype = "text"

        #LAYOUT
        self.playPause_button.clicked.connect(self.playPause)
        self.stop_button.clicked.connect(self.stop)
        self.nextFrame_button.clicked.connect(self.nextFrame)
        self.prevFrame_button.clicked.connect(self.prevFrame)
        self.animationMovement_horizontalSlider.valueChanged.connect(self.sliderChanged)
        

        #MENU
        self.actionLoad_File.triggered.connect(self.loadSingleFile)
        self.actionLoad_Data.triggered.connect(self.loadDirectory)
        self.actionLoad_Header_File.triggered.connect(self.loadHeader)
        self.actionShow_3D_Model.triggered.connect(self.worker.playAnimation)

    def filetypeCheckBox(self):
        if(self.binaryFiles_checkBox.isChecked()):
            self.filetype = "binary"
        else:
            self.filetype = "text"

    def loadSingleFile(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')

    def loadDirectory(self):
        self.filetypeCheckBox()
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
        self.directory = filename[:filename.rfind("/")+1]
        self.fformat = filename[filename.rfind("."):]
        self.directory_lineEdit.setText(self.directory)
        self.format_value_label.setText(self.fformat)

        self.worker.directory = self.directory
        self.worker.fformat = self.fformat
        self.worker.filetype = self.filetype

        #prawokultury/kurs

        tFileList = os.listdir(self.directory)
        c = 0
        for f in tFileList:
            #print(f)
            if(f[f.rfind("."):]==self.fformat):
                c+=1

        self.number_of_files_value_label.setText(str(c))
        self.animationMovement_horizontalSlider.setMaximum(c)

    def loadHeader(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
        self.headerFile = filename
        self.header_file_lineEdit.setText(self.headerFile)
        self.worker.headerFile = self.headerFile
    
    def playPause(self):
        if self.worker.play:
            self.nextFrame_button.setEnabled(True)
            self.prevFrame_button.setEnabled(True)
            self.playPause_button.setText("Play")
            self.worker.play = False
        else:
            self.nextFrame_button.setEnabled(False)
            self.prevFrame_button.setEnabled(False)
            self.playPause_button.setText("Pause")
            self.worker.play = True

    def stop(self):
        self.worker.stop = True
        self.playPause_button.setText("Play")

    def nextFrame(self):
        self.worker.nextFrame = True

    def prevFrame(self):
        self.worker.prevFrame = True
    
    def sliderChanged(self):
        self.worker.setFrame = True
        self.worker.frame = self.animationMovement_horizontalSlider.value()
        self.animationMovement_horizontalSlider.setValue(self.worker.frame)
    
        
    
    
def main():
    app = QtGui.QApplication(sys.argv)
    window = MainScreen()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
