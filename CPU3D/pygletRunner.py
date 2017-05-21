try:
    from pyglet1 import *
except:
    from CPU3D.pyglet1 import *

from time import *

class PygletRunner(QtCore.QObject):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.play = False
        self.directory = ""
        self.fformat = ""
        self.headerFile = ""
        self.TIME_INTERVAL = 1/60
        
    def playAnimation(self):
        self.simulateDirectory(self.directory, self.fformat, self.headerFile)
        print("generating 3d structure...")
        animation3d = Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
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
                sleep(0.1)
            #print(self.play)
            else:
                sleep(1)
            
    def getAllFiles(self, directory, extension):
        tFileList = os.listdir(directory)
        fileList = []
        j = 0
        for file in tFileList:
            j += 1
            if j > control:
                break
            if file.find(extension) != -1:
                fileList.append(directory + file)

        base_data = []
        count = []
        data = []
        print("Reading data... {}".format(len(fileList)))
        fileList.sort()
        for filename in fileList:
            tbase_data, tcount = extract_base_data(filename)
            base_data.append(tbase_data)
            count.append(tcount)
            to_skip = [x for x in range(tcount)]
            df = form_dataframe(filename, to_skip)
            data.append(df)

        return data, base_data, count
    
    def simulateDirectory(self, path_to_folder, extension, path_to_header_file):
        '''global header ok
        global data
        global base_data
        global count
        global angle_list ok
        global vectors_list ok
        global color_list ok
        global tbase_data ok
        global tcount ok
        global colors'''

        self.tdata, self.tbase_data, self.tcount = self.getAllFiles(path_to_folder, extension)

        self.header = read_header_file(path_to_header_file)


        self.angle_list = []
        self.vectors_list = []
        self.color_list = []

        #start = time.time()

        pool = Pool()
        multiple_results = [pool.apply_async(process_batch, (self.tdata[i], self.tbase_data[i])) for i in range(len(tdata))]
        for result in multiple_results:
            angle, vectors, colors = result.get(timeout=25)
            angle_list.append(angle)
            vectors_list.append(vectors)
            color_list.append(colors)

        #end = time.time()
        #print("It has taken {}".format(end-start))


        self.data = tdata
        self.base_data = tbase_data[0]
        self.count = tcount[0]
        #Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
        #pyglet.app.run()

    def simulateFile(self, path_to_file, path_to_header_file):
        data, count = extract_base_data(path_to_file)
        header = read_header_file(path_to_header_file)
        Window(WINDOW, WINDOW, 'Pyglet Colored Cube')
        pyglet.app.run()