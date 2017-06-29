import sys

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
