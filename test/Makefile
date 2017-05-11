BIAB=$(shell pyenv which biab)

all:
	$(BIAB) ANSI-C-grammar.bb
	$(BIAB) desk.bb
	$(BIAB) desk1.bb
	$(BIAB) meta.bb

clean:
	rm -f *.py *.tab.c *.y *.output *~
