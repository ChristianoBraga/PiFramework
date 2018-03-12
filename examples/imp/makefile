#!/bin/bash

export MAUDE

all:
	make imp

imp:
	./genimp $(MAUDE) $(PWD) > bin/imp.sh
	chmod +x bin/imp.sh
	ln -s bin/imp.sh ./imp

tex:
	noweave -delay imp.noweb > doc/imp.tex
	pdflatex -output-directory=doc doc/imp.tex
	pdflatex -output-directory=doc doc/imp.tex

maude:
	notangle -Rimp.maude imp.noweb > maude/imp.maude

clean:
	rm imp
	rm bin/imp.sh
	rm doc/*.aux
	rm doc/*.log
	rm doc/*.out
	rm doc/*.tex
