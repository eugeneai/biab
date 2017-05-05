all: parse.py parse-debug.py

parse.py: parse.py.in
	python ../tools/ppp.py <parse.py.in >parse.py

parse-debug.py: parse.py.in
	python ../tools/ppp.py -DDEBUG <parse.py.in >parse-debug.py

clean:
	rm -f *~ *.output *.tab.c *.y *.pyc *.pyo *stats \
		parse.py parse-debug.py
