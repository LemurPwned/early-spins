from CPU3D.pyglet1 import *

import time
#from GUI.WarningWindow import Ui_Window
from GUI.warning import WarningScreen


class PygletRunner(QtCore.QObject):
    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.play = False
        self.nextFrame = False
        self.prevFrame = False
        self.stop = False
        self.setFrame = False
        self.frame = 0
        self.directory = ""
        self.fformat = ""
        self.headerFile = ""
        self.filetype = ""
        self.TIME_INTERVAL = 1/200
        self.control = 544
        self.average = 1 # one is no averaging
        self.layer = 4

    @QtCore.pyqtSlot()
    def playAnimation(self):
        if self.directory=="":
            self.signalStatus.emit("no_dir")
            return 0

        elif self.headerFile == "":
            self.signalStatus.emit("no_header")
            return 0

        self.simulateDirectory(self.directory, self.fformat, self.headerFile, self.filetype)
        print("Generating 3d structure...")
        animation3d = Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
        fps_display = pyglet.window.FPSDisplay(animation3d)
        animation3d.getDataFromRunner([self.vectors_list, self.color_list,
                    self.iterations, self.control, fps_display])
        t1 = threading.Thread(target = pyglet.app.run)
        pyglet.clock.schedule_interval(animation3d.update, self.TIME_INTERVAL)
        t1.start()
        #TODO: explanation
        #THE CLOCK funcion schedules the invocation of update function when
        #time interval passes, thus automatically increasing the counter self.i
        #IT CANNOT BE INCREASED at the same time by another function, because the
        #overflow will occur. Thus, either use clock or schdeule the change of
        #frame with the chunk of code below, but never both
        print("done!")
        while(True):
            if self.play:
                animation3d.i+=1
                animation3d.list_guard()

            if self.nextFrame:
                animation3d.i+=1
                animation3d.list_guard()
                self.nextFrame = False

            if self.prevFrame:
                animation3d.i-=1
                animation3d.list_guard()
                self.prevFrame = False

            if self.stop:
                animation3d.i = 0
                animation3d.list_guard()
                self.play = False
                self.stop = False

            if self.setFrame:
                animation3d.i = self.frame
                animation3d.list_guard()
                self.setFrame = False

            #time.sleep(0.1)
            #animation3d.update(1)
            time.sleep(self.TIME_INTERVAL*70)
            if animation3d.i%10:
                self.signalStatus.emit(str(animation3d.i))

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

        start = time.time()
        self.base_data = self.tbase_data[0]
        self.data = self.tdata ###????
        self.vectors_list = construct_layer_outline(self.base_data)
        self.vectors_list = self.vectors_list[0::self.average]
        self.color_list = []
        print("Elaped on constructing layer outline: {}".format(time.time()-start))
        xc = int(self.base_data['xnodes'])
        yc = int(self.base_data['ynodes'])
        zc = int(self.base_data['znodes'])
        print("{} layers detected, {} layer was selected".format(zc, self.layer))
        if self.layer:
            self.tdata = [self.tdata[i].reshape(zc, xc*yc,3)[self.layer-1] for i in range(self.iterations)]
            zc = 1
        pool = Pool()
        multiple_results = [pool.apply_async(process_fortran_list, (self.tdata[i], xc, yc, zc))
                            for i in range(len(self.tdata))]

        for result in multiple_results:
            colors = result.get(timeout=12)
            self.color_list.append(colors[0::self.average])
        print("Elaped on getting all vectors: {}".format(time.time()-start))
