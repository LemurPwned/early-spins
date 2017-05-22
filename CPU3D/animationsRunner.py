from PyQt4 import QtGui, QtCore #TODO not neccesary later
from CPU3D.animations import *
    
class AnimationsRunner(QtCore.QObject):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.play = False
        self.directory = ""
        self.fformat = ""
        self.headerFile = ""
        self.N = 100 ##TODO CHECK
        
    def playAnimation(self):
        pass
    
    def loadFiles(self):
        self.file_list = batch_load(self.directory, self.N, process_batch)
        batches_to_animate = []
        for filename in self.file_list:
            batches_to_animate.append(process_batch(filename))
        print(len(batches_to_animate))
        init_anim(batches_to_animate, 'Magnetization direction', self.N, 35, 35)