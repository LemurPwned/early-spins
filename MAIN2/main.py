import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from MainWindowTemplate import Ui_MainWindow

#from mainWindow import GLWidget, Helper
from structureDrawer import DrawData

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ESE - Early Spins Enviroment")

        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(800, 600)
        self.canvas = DrawData()
        self.canvas.initialSettings()
        #self.openGLWidget = canvas
        self.openGLWidget.paintGL = self.canvas.paintGL #canvas.draw_cordinate_system()

        timer = QTimer(self)
        timer.timeout.connect(self.openGLWidget.update)
        timer.start(0)
        self.addButtons()

    def events(self):
        self.actionLoad_Directory.clicked.connect()


    def addButtons(self):
        '''temp function unless mouse operation disabled'''
        camLeft = QPushButton("Camera Left", self)
        camRight = QPushButton("Camera Right", self)
        camLeft.move(1000, 200)
        camRight.move(1000, 250)
        camLeft.clicked.connect(self.canvas.cameraLeft)
        camRight.clicked.connect(self.canvas.cameraRight)
        #self.openGLWidget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
