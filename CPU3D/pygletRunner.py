from CPU3D.pyglet1 import *
from time import *

class PygletRunner(QtCore.QObject):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.play = False
        self.directory = ""
        self.fformat = ""
        self.headerFile = ""
        self.filetype = ""
        self.TIME_INTERVAL = 1/30
        self.control = 10 #TODO: parametrize it

    def playAnimation(self):
        self.simulateDirectory(self.directory, self.fformat, self.headerFile, self.filetype)
        print("Generating 3d structure...")
        animation3d = Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
        animation3d.getDataFromRunner([self.vectors_list, self.color_list, self.tbase_data, self.header, self.iterations])
        t1 = threading.Thread(target = pyglet.app.run)
        t1.start()
        print("done!")

        while(True):
            if self.play:
                #print("next_frame")
                animation3d.i+=1
                pyglet.clock.schedule_interval(animation3d.update, self.TIME_INTERVAL)
                #animation3d.update()
                animation3d.list_guard()
                #animation3d.change_frame()
            sleep(0.01)
            #print(self.play)

    def getAllFiles(self, directory, extension, filetype = 'binary'):
        tFileList = os.listdir(directory)
        fileList = []
        j = 0
        for file in tFileList:
            j += 1
            if j > self.control:
                break
            if file.find(extension) != -1:
                fileList.append(directory + file)
        base_data = []
        data = []
        print("Reading data... {}, fileformat: {}".format(len(fileList), filetype))
        fileList.sort()
        if filetype == 'binary':
            for filename in fileList:
                tbase_data, tdf = binary_read(filename)
                base_data.append(tbase_data)
                data.append(tdf)
        elif filetype == 'text':
            for filename in fileList:
                tbase_data, tcount = extract_base_data(filename)
                base_data.append(tbase_data)
                #count.append(tcount)
                to_skip = [x for x in range(tcount)]
                df = form_dataframe(filename, to_skip)
                data.append(df)

        return data, base_data

    def simulateDirectory(self, path_to_folder, extension, path_to_header_file, filetype):
        self.tdata, self.tbase_data= self.getAllFiles(path_to_folder, extension, filetype)
        self.header, self.iterations = odt_reader(path_to_header_file) #new odt format reader, more universal

        self.vectors_list = []
        self.color_list = []

        pool = Pool()
        multiple_results = [pool.apply_async(process_batch, (self.tdata[i], self.tbase_data[i])) for i in range(len(self.tdata))]
        for result in multiple_results:
            vectors, colors = result.get(timeout=25)
            self.vectors_list.append(vectors)
            self.color_list.append(colors)

        self.data = self.tdata
        self.base_data = self.tbase_data[0]
