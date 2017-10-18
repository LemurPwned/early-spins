import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from MainWindowTemplate import Ui_MainWindow

#from mainWindow import GLWidget, Helper
from structureDrawer import paintGL

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("ESE - Early Spins Enviroment")

        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(800, 600)
        self.openGLWidget.paintGL = paintGL

        timer = QTimer(self)
        timer.timeout.connect(self.openGLWidget.update)
        timer.start(1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
