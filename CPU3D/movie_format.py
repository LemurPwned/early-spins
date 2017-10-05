import PIL
import skvideo.io as skv
import skimage.io as ski
from skimage import color
import numpy as np
import os
from CPU3D.runner import Runner

class Movie(Runner):
    def __init__(self):
        super(Runner).__init__()
        self.directory = ""
        self.framerate = 5
        #regulate the framerate, not usual standard, see below
        self.filename = ""
        self.format = ".avi"

    def create_video(self):
        '''
        composes video from .jpg files, requires ffmpeg
        '''
        fileList = os.listdir(self.directory)
        total_movie = []
        fileList.sort()
        for filename in fileList:
            if filename.endswith('.jpg'):
                print(self.directory+"/"+filename)
                img = ski.imread(self.directory+"/"+filename)
                for i in range(self.framerate):
                    total_movie.append(img)
        total_movie = np.array(total_movie)
        skv.vwrite(self.filename+self.format, total_movie)
