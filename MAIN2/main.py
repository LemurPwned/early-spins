import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from MainWindowTemplate import Ui_MainWindow

#from mainWindow import GLWidget, Helper
from structureDrawer import DrawData
from pyqtMatplotlib import PlotCanvas

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ESE - Early Spins Enviroment")
        self.setGeometry(10,10,1280, 768)
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
        self.events()

    def events(self):
        #FILE SUBMENU
        #self.actionLoad_File.clicked.connect()
        #self.actionLoad_Directory.clicked.connect()

        #EDIT SUBMENU
        #self.actionPlot.clicked.connect()
        #self.actionAnimation.clicked.connect()

        #VIEW SUBMENU
        self.action2_Window_Grid.triggered.connect(self.make2WindowsGrid)
        #self.action4_Windows_Grid.clicked.connect()


    def make2WindowsGrid(self):
        middlePos = (self.width())/2
        self.openGLWidget.setGeometry(self.openGLWidget.pos().x(), self.openGLWidget.pos().y(), middlePos-50, self.height())

        #create matplotlib window
        self.canvasPlot1 = PlotCanvas(self, width=5, height=5)
        self.canvasPlot1.move(middlePos+50, self.openGLWidget.pos().y())
        self.canvasPlot1.resize(100, 100)

        #width of the other widget


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
