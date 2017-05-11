from PyQt4 import QtGui, QtCore
import sys 

from GUI.MainWindow import Ui_MainWindow

class MainScreen(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainScreen, self).__init__(parent)
		self.setupUi(self)
		self.progressBar.setProperty("value", 0)
		self.window()

	def window(self):
		#LAYOUT
		self.playPause_button.clicked.connect(self.playPause)
		self.stop_button.clicked.connect(self.stop)
		self.nextFrame_button.clicked.connect(self.nextFrame)
		self.prevFrame_button.clicked.connect(self.prevFrame)
		
		#MENU
		self.actionLoad_File.triggered.connect(self.loadSingleFile)
		self.actionLoad_Data.triggered.connect(self.loadDirectory)
		
	
	def loadSingleFile(self):
		w = QtGui.QWidget()
		filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
		
	def loadDirectory(self):
		w = QtGui.QWidget()
		filename = QtGui.QFileDialog.getOpenFileName(w, 'Open File', '.')
		#NOT WORKING PROPERLY ONLY ALLOWING TO OPEN FILE
	
	
		
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


def test():
	print("test")

def main():
	app = QtGui.QApplication(sys.argv)
	window = MainScreen()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
