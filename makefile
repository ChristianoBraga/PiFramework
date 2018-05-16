#!/bin/bash
all: clean tex maude

tex:
	noweave -delay bplc.noweb > doc/bplc.tex
	pdflatex -output-directory=doc bplc.tex

maude:
	notangle -Rbplc.maude bplc.noweb > maude/bplc.maude

clean:
ifneq (, $(wildcard doc/*.aux))
	@rm ./doc/*.aux
endif
ifneq (, $(wildcard doc/*.log))
	@rm ./doc/*.log
endif
ifneq (, $(wildcard doc/*.out))
	@rm ./doc/*.out
endif
ifneq (, $(wildcard doc/*.tex))
	@rm ./doc/*.tex
endif
