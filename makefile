run:
	python3 -m main

pyglet:
	python3 -m test pyglet

profiler:
	python3 -m cProfile -o profiler_output test.py pyglet >> profiler.txt

parser:
	python3 -m test input_parser
	#for profiling custom function
tester:
	python3 -m test tester

binary:
	python3 -m test binary_parser
