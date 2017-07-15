import sys
import os
import threading
from threading import Thread

if(len(sys.argv)>2):
    exit("Error expecting 1 argument")

if (str(sys.argv[1]) == "run"):
    from CPU3D.runner import Runner
    x = Runner()
    x.play = True
    #x.directory = "data/0520nm/"
    x.directory = "data/firstData/"
    x.fformat = ".omf"
    x.filetype = 'text'
    #x.headerFile = 'data/0520nm/proba1.odt'
    x.headerFile = "data/firstData/voltage-spin-diode.odt"
    x.prepare_run()
    Thread(target = x.play2DGraph).start()
    Thread(target = x.play3DAnimation).start()

if(str(sys.argv[1]) == "pyglet"):
    from CPU3D.pygletRunner import PygletRunner
    x = PygletRunner()
    x.play = True
    #example of usage
    #x.directory = "data/firstData/"
    x.directory = "data/0200nm/"
    x.fformat = ".omf"
    x.filetype = 'binary'
    #x.filetype = 'text'
    x.headerFile = 'data/0200nm/proba1.odt'
    x.playAnimation()

if(str(sys.argv[1])== 'runner'):
    from CPU3D.animationsRunner import *
    x = AnimationsRunner()
    x.play = True
    #example of usage
    #x.directory = "data/firstData/"
    x.directory = "data/0200nm/"
    x.fformat = ".omf"
    x.filetype = 'binary'
    #x.filetype = 'text'
    x.headerFile = 'data/0200nm/proba1.odt'
    #x.headerFile = "data/firstData/voltage-spin-diode.odt"
    x.playAnimation()

if(str(sys.argv[1]) == "tester"):
    from CPU3D.input_parser import *
    filename ='data/0520nm/proba1-Oxs_TimeDriver-Magnetization-01-0002265.omf'
    _, vectors1 = binary_read3(filename)
    _, vectors2 = binary_read2(filename)
    #for i in range(100):
    #    print(vectors1[i], vectors2[i])
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    for i in range(1):
        base_data, vectors = binary_read2(filename)
        #vectors, colors = process_fortran_list(lists, base_data)
    pr.disable()
    pr.print_stats(sort='time')
    #print(len(colors))
    #print(colors[1:100])
