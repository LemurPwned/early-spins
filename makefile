run:
	python3 -m main

pyglet:
	python3 -m test pyglet

profiler:
	python3 -m cProfile test.py pyglet >> profiler.txt
