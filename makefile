#!/bin/bash

tex: 
	noweave -delay bplc.noweb > doc/bplc.tex
	pdflatex -output-directory=doc doc/bplc.tex

maude: 
	notangle -Rbplc.maude bplc.noweb > maude/bplc.maude

clean:
	rm doc/*.aux
	rm doc/*.log
	rm doc/*.out
	rm doc/*.tex
