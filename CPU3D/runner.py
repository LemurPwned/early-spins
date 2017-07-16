from CPU3D.pyglet1 import *
from CPU3D.anims import *
from CPU3D.input_parser import *
import time
from multiprocessing import Pool
import threading


class Runner(QtCore.QObject):
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
        self.control = 1000
        self.average = 3 # one is no averaging
        self.layer = 4 # indexing starts from 1 to reduce redundancy
        self.wait_ended = False # control variable, orders one animation to wait for the other
        self.i = 0 # multiclass iterator to which all clases should synchronize
        self.bar = ""

    def prepare_run(self):
        if self.directory=="":
            self.signalStatus.emit("no_dir")
            return 0

        elif self.headerFile == "":
            self.signalStatus.emit("no_header")
            return 0

        self.simulateDirectory(self.directory, self.fformat, self.headerFile, self.filetype)
        print("Preparing to generate animations...")

    @QtCore.pyqtSlot()
    def play2DAnimation(self):
        """
        this instance allows for creating dynamic 2D animation of the layer
        surface that synchronizes with 3D animation
        """
        self.myanim = Animation()
        self.myanim.base_data = self.tbase_data[0]
        self.myanim.tdata = self.tdata
        self.myanim.reshape_data()
        self.myanim.iterations = self.iterations
        self.myanim.current_layer = 0
        self.myanim.create_canvas()
        self.wait_ended = True
        self.myanim.run_canvas()

    @QtCore.pyqtSlot()
    def play2DGraph(self):
        """
        this instance allows for creating dynamic graphs that follow an
        animation
        """
        self.myanim = Animation()
        self.myanim.base_data = self.tbase_data[0]
        self.myanim.tdata = self.tdata
        self.myanim.reshape_data()
        self.myanim.iterations = self.iterations
        self.myanim.current_layer = 0
        self.myanim.graph_data = self.header['UZeeman::Energy'].tolist()[0:self.iterations]
        self.myanim.title = 'Zeeman Energy'
        #TODO: ask about the above, it seems that header contains more data
        # than available in iterations
        self.myanim.create_plot_canvas()
        self.wait_ended = True
        self.myanim.run_canvas()

    @QtCore.pyqtSlot()
    def play3DAnimation(self):
        start = time.time()
        self.base_data = self.tbase_data[0]
        self.vectors_list = construct_layer_outline(self.base_data)
        #self.vectors_list = self.vectors_list[0::self.average] # moved to pyglet class
        self.color_list = []
        print("Elaped on constructing layer outline: {}".format(time.time()-start))
        xc = int(self.base_data['xnodes'])
        yc = int(self.base_data['ynodes'])
        zc = int(self.base_data['znodes'])
        print("{} layers detected, {} layer was selected".format(zc, self.layer))
        if self.layer:
            self.tdata = [self.tdata[i].reshape(zc, xc*yc,3)[self.layer-1] for i in range(self.iterations)]
            zc = 1  # this is to keep reshape function operational, and preserve
                    # layer outline structure, see below
        pool = Pool()
        multiple_results = [pool.apply_async(process_fortran_list, (self.tdata[i], xc, yc, zc))
                            for i in range(len(self.tdata))]
        self.color_list = [result.get(timeout=12) for result in multiple_results]

        print("Elaped on getting all vectors: {}".format(time.time()-start))
        animation3d = Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
        fps_display = pyglet.window.FPSDisplay(animation3d)
        animation3d.getDataFromRunner([self.vectors_list, self.color_list,
                    self.iterations, self.control, fps_display, self.average])
        t1 = threading.Thread(target = pyglet.app.run)
        while not self.wait_ended:
            time.sleep(0.01)
        pyglet.clock.schedule_interval(animation3d.update, self.TIME_INTERVAL)
        t1.start()
        while(True):
            if self.play:
                self.i += 1
                self.list_guard()
                animation3d.i = self.i
                self.myanim.i = self.i
                #self.myanim.replot_data()
                self.myanim.replot()
            if self.nextFrame:
                self.i += 1
                self.list_guard()
                animation3d.i = self.i
                self.myanim.i = self.i
                #self.myanim.replot_data()
                self.myanim.replot()
                self.nextFrame = False
            if self.prevFrame:
                self.i -= 1
                self.list_guard()
                animation3d.i = self.i
                self.myanim.i = self.i
                #self.myanim.replot_data()
                self.myanim.replot()
                self.prevFrame = False
            if self.stop:
                self.i = 0
                self.list_guard()
                animation3d.i = self.i
                self.myanim.i = self.i
                #self.myanim.replot_data()
                self.myanim.replot()
                self.play = False
                self.stop = False
            if self.setFrame:
                self.i = self.frame
                self.list_guard()
                animation3d.i = self.i
                self.myanim.i = self.i
                self.myanim.replot()
                #self.myanim.replot_data()
                self.setFrame = False
            time.sleep(self.TIME_INTERVAL*70)
            if animation3d.i%10:
                self.signalStatus.emit(str(animation3d.i))

    def simulateDirectory(self, path_to_folder, extension, path_to_header_file, filetype):
        t1 = time.time()
        self.tdata, self.tbase_data = self.getAllFiles(path_to_folder, extension, filetype)
        print("Reading files took: {}".format(time.time()-t1))
        self.header, self.stages = odt_reader(path_to_header_file) #new odt format reader, more universal
        print("Maximum number of iterations : {}".format(self.iterations))

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
        file_pool = Pool()
        self.init_progress_bar()
        p = 0
        if filetype == 'binary':
            multiple_results = [file_pool.apply_async(binary_read, (filename,))
                                    for filename in fileList]
            for result in multiple_results:
                self.update_progress_bar(p)
                tbd, tdf = result.get(timeout=12)
                data.append(tdf)
                p+= 1
                if len(base_data) == 0:
                    base_data.append(tbd)
        elif filetype == 'text':
            tbase_data, _ = extract_base_data(fileList[0])
            base_data.append(tbase_data)
            multiple_results = [file_pool.apply_async(fortran_list, (filename,))
                                    for filename in fileList]
            for result in multiple_results:
                self.update_progress_bar(p)
                df = result.get(timeout=12)
                data.append(df)
                p+=1
        return data, base_data

    def list_guard(self):
        if self.i >= self.control-1:
            self.i = 0
        if self.i > self.iterations-1:
            self.i = 0

    def init_progress_bar(self):
        for i in range(100):
            self.bar += "="

    def update_progress_bar(self, i):
        k = (i*100/self.iterations)
        k = int(k)
        stars = ""
        for i in range(k+1):
            stars+="*"
        self.bar = stars + self.bar[k+1:]
        print("[" + self.bar + "] {}%".format(i))
