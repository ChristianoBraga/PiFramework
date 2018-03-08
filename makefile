#!/bin/bash

tex: doc/bplc.tex 
	noweave -delay bplc.noweb > doc/bplc.tex
	pdflatex -output-directory=doc bplc.tex

maude: maude/bplc.maude 
	notangle -Rbplc.maude bplc.noweb > maude/bplc.maude

clean:
	rm doc/*.aux
	rm doc/*.log
	rm doc/*.out
	rm doc/*.tex
