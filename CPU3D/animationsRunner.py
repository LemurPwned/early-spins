from PyQt4 import QtGui, QtCore #TODO not neccesary later
from CPU3D.anims import *
from CPU3D.pygletRunner import *
from GUI.warning import WarningScreen

class AnimationsRunner(QtCore.QObject):
    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.play = False
        self.directory = ""
        self.fformat = ""
        self.headerFile = ""
        self.filetype = ""
        self.control = 544
        self.average = 1 # one is no averaging


    @QtCore.pyqtSlot()
    def playAnimation(self):
        if self.directory=="":
            self.signalStatus.emit("no_dir")
            return 0

        elif self.headerFile == "":
            self.signalStatus.emit("no_header")
            return 0

        self.simulateDirectory(self.directory, self.fformat, self.headerFile, self.filetype)
        print("Generating 2D animation...")

        myanim = Animation()
        myanim.base_data = self.tbase_data[0]
        myanim.tdata = self.tdata
        myanim.reshape_data()
        myanim.iterations = self.iterations
        myanim.current_layer = 0
        myanim.init_anim()


    def getAllFiles(self, directory, extension, filetype = 'binary'):
        tFileList = os.listdir(directory)
        fileList = []
        for file in tFileList:
            if file.find(extension) != -1:
                fileList.append(directory + file)
            if len(fileList) > self.control:
                break
        base_data = []
        data = []
        print("Reading data... {}, fileformat: {}".format(len(fileList), filetype))
        fileList.sort()
        self.iterations = len(fileList)
        if filetype == 'binary':
            for filename in fileList:
                tbase_data, tdf = binary_read(filename)
                base_data.append(tbase_data)
                data.append(tdf)
        elif filetype == 'text':
            for filename in fileList:
                tbase_data, _ = extract_base_data(filename)
                base_data.append(tbase_data)
                df = fortran_list(filename)
                data.append(df)
        return data, base_data

    def simulateDirectory(self, path_to_folder, extension, path_to_header_file, filetype):
        self.tdata, self.tbase_data = self.getAllFiles(path_to_folder, extension, filetype)
        self.header, self.stages = odt_reader(path_to_header_file) #new odt format reader, more universal
        print("Maximum number of iterations : {}".format(self.iterations))
