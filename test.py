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
    x.filetype = 'text'
    x.headerFile = "data/voltage-spin-diode.odt"
<<<<<<< HEAD
    #x.headerFile = "0200nm/proba1.odt"
=======
>>>>>>> 4161641602d74f5d45d635d3e03c5822b0f031d7
    x.playAnimation()

# u can create your own simulations and then add it to makefile
if(str(sys.argv[1]) == ""):
    pass
