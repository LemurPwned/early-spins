from PyQt4 import QtGui, QtCore
from GUI.WarningWindow import Ui_Window


class WarningScreen(QtGui.QWidget, Ui_Window):
    def __init__(self, parent = None):
        super(WarningScreen, self).__init__(parent)
        self.setupUi(self)
        self._message = ""
        self.warning_pushButton.clicked.connect(lambda: self.close())
        
    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, msg):
        self._message = msg
        
    def showMsg(self):
        self.warning_Label.setText(str(self._message))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sc = WarningScreen()
    sc.show()
    sys.exit(app.exec_())