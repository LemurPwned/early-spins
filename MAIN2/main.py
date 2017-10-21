import sys

from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from MainWindowTemplate import Ui_MainWindow

#from mainWindow import GLWidget, Helper
from structureDrawer import DrawData
from plotCanvas import PlotCanvas

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ESE - Early Spins Enviroment")
        self.setGeometry(10,10,1280, 768)
        self.setupGL()

        self.addButtons() #temp function
        self.events()

        self.gridSize = 1

    def setupGL(self):
        self.openGLWidget.initializeGL()

        self.canvas = DrawData()
        self.canvas.initialSettings()
        self.openGLWidget.paintGL = self.canvas.paintGL

        timer = QTimer(self)
        timer.timeout.connect(self.openGLWidget.update)
        timer.start(0)

        self.make1WindowGrid()

    def events(self):
        #FILE SUBMENU
        #self.actionLoad_File.clicked.connect()
        #self.actionLoad_Directory.clicked.connect()

        #EDIT SUBMENU
        #self.actionPlot.clicked.connect()
        #self.actionAnimation.clicked.connect()

        #VIEW SUBMENU
        self.action1_Window_Grid.triggered.connect(self.make1WindowGrid)
        self.action2_Windows_Grid.triggered.connect(self.make2WindowsGrid)
        self.action4_Windows_Grid.triggered.connect(self.make4WindowsGrid)

    def resizeEvent(self, event):
        if self.gridSize == 1:
            self.make1WindowGrid()
        elif self.gridSize == 2:
            self.make2WindowsGrid()
        elif self.gridSize == 4:
            self.make4WindowsGrid
        #print(event)


    def make1WindowGrid(self):
        self.gridSize = 1
        try:
            self.canvasPlot1.hide()
        except:
            pass

        try:
            self.canvasPlot2.hide()
        except:
            pass

        try:
            self.canvasPlot3.hide()
        except:
            pass

        self.openGLWidget.setGeometry(50, 15, self.width()-100, self.height()-50)


    def make2WindowsGrid(self):
        self.gridSize = 2
        middlePos = (self.width())/2
        self.openGLWidget.setGeometry(self.openGLWidget.pos().x(), self.openGLWidget.pos().y(), middlePos-50, self.height())

        #create matplotlib window
        try:
            self.canvasPlot1.show()
        except:
            self.canvasPlot1 = PlotCanvas(self, width=5, height=4)
        self.canvasPlot1.move(middlePos+50, 10)
        self.canvasPlot1.resize((self.width()/2)-50, self.height()-25)
        self.canvasPlot1.show()

        try:
            self.canvasPlot2.hide()
            self.canvasPlot3.hide()
        except:
            pass


    def make4WindowsGrid(self):
        self.gridSize = 4
        middleWidthPos = (self.width())/2
        middleHeightPos = (self.height())/2

        self.openGLWidget.setGeometry(self.openGLWidget.pos().x(), self.openGLWidget.pos().y(), middleWidthPos - 50, middleHeightPos - 25)

        #create matplotlib window right top corner
        try:
            self.canvasPlot1.show()
        except:
            self.canvasPlot1 = PlotCanvas(self, width=5, height=4)
        self.canvasPlot1.setGeometry(middleWidthPos+25, 15, (self.width()/2-25), (self.height()/2)-15)
        self.canvasPlot1.show()

        #create matplotlib window left bottom corner
        try:
            self.canvasPlot2.show()
        except:
            self.canvasPlot2 = PlotCanvas(self, width=5, height=4)
        self.canvasPlot2.setGeometry(25, middleHeightPos + 15, (self.width()/2-25), (self.height()/2)-30)
        self.canvasPlot2.show()

        #create matplotlib window left bottom corner
        try:
            self.canvasPlot3.show()
        except:
            self.canvasPlot3 = PlotCanvas(self, width=5, height=4)
        self.canvasPlot3.setGeometry(middleWidthPos + 25, middleHeightPos + 15, (self.width()/2-25), (self.height()/2)-30)
        self.canvasPlot3.show()

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
