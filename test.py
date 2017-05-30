import sys

if(len(sys.argv)>2):
    exit("Error expecting 1 argument")

if(str(sys.argv[1]) == "pyglet"):

    from CPU3D.pygletRunner import PygletRunner
    x = PygletRunner()
    x.play = True

    #example of usage
    x.directory = "data/"
    #x.directory = "0200nm/"
    x.fformat = ".omf"
    #x.filetype = 'binary'
    x.filetype = 'text'
    #x.headerFile = '0200nm/proba1.odt'
    x.headerFile = "data/voltage-spin-diode.odt"
    x.playAnimation()

# u can create your own simulations and then add it to makefile
if(str(sys.argv[1]) == ""):
    pass
