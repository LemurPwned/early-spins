run:
	python3 -m main

pyglet:
	python3 -m test pyglet

profiler:
	python3 -m cProfile -o profiler_output test.py pyglet >> profiler.txt

parser:
	python3 -m test input_parser
