import sys
import os

if(len(sys.argv)>2):
    exit("Error expecting 1 argument")

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
    #x.headerFile = "data/firstData/voltage-spin-diode.odt"
    x.playAnimation()

if(str(sys.argv[1]) == "input_parser"):
    from CPU3D.input_parser import *
    filename ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    base_data, count = extract_base_data(filename)
    header, iterations = odt_reader('data/firstData/voltage-spin-diode.odt')
    print(base_data)

if(str(sys.argv[1]) == "binary_parser"):
    from CPU3D.input_parser import *
    filename ='data/0520nm/proba1-Oxs_TimeDriver-Magnetization-00-0001296.omf'
    base_data, vectors = binary_read(filename)
    print(base_data)

if(str(sys.argv[1]) == "tester"):
    from CPU3D.input_parser import *
    filename ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    base_data, count = extract_base_data(filename)
    lists = fortran_list(filename)
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    for i in range(100):
        vectors, colors = process_fortran_list(lists, base_data)
    pr.disable()
    pr.print_stats(sort='time')
    print(len(colors))
    print(colors[1:100])

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

if(str(sys.argv[1]) == "anims"):
    from CPU3D.anims import *
    from CPU3D.input_parser import *

    filename ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    #filename2 ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000900.omf'
    #filename3 ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0001800.omf'
    base_data, _ = extract_base_data(filename)
    #lists = fortran_list(filename)
    #lists2 = fortran_list(filename2)
    #lists3 = fortran_list(filename3)
    '''
    k = lists[0]
    k = np.array([x[0] for x in k])
    print(k.shape)
    for j in zip(k):
        print(j)
    '''
    control = 100
    directory = 'data/firstData/'
    tFileList = os.listdir(directory)
    fileList = []
    tdata = []
    filetype = 'text'
    extension = '.omf'
    for file in tFileList:
        if file.find(extension) != -1:
            fileList.append(directory + file)
        if len(fileList) > control:
            break
    data = []
    control = len(fileList)
    print("Reading data... {}, fileformat: {}".format(len(fileList), filetype))
    fileList.sort()
    if filetype == 'text':
        for filename in fileList:
            _, _ = extract_base_data(filename)
            data = fortran_list(filename)
            tdata.append(data)


    myanim = Animation()
    myanim.base_data = base_data
    myanim.tdata = tdata
    myanim.reshape_data()
    myanim.iterations = control
    myanim.init_anim()
