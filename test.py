import sys

if(len(sys.argv)>2):
    exit("Error expecting 1 argument")

if(str(sys.argv[1]) == "pyglet"):

    from CPU3D.pygletRunner import PygletRunner
    x = PygletRunner()
    x.play = True

    #example of usage
    x.directory = "data/firstData/"
    #x.directory = "0200nm/"
    x.fformat = ".omf"
    #x.filetype = 'binary'
    x.filetype = 'text'
    #x.headerFile = '0200nm/proba1.odt'
    x.headerFile = "data/firstData/voltage-spin-diode.odt"
    x.playAnimation()

if(str(sys.argv[1]) == "input_parser"):
    from CPU3D.input_parser import *
    filename ='data/firstData/voltage-spin-diode-Oxs_TimeDriver-Magnetization-00-0000000.omf'
    base_data, count = extract_base_data(filename)
    header = read_header_file('data/firstData/voltage-spin-diode.odt')
    to_skip = [x for x in range(count)]
    df = form_dataframe(filename, to_skip)

    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    for i in range(100):
        vectors, colors = process_batch(df, base_data)
    pr.disable()
    pr.print_stats(sort='time')
    #print(df.head(), df.shape)
    #print(vectors)
# u can create your own simulations and then add it to makefile
if(str(sys.argv[1]) == ""):
    pass
