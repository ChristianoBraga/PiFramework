#!/bin/bash

export MAUDE

all:
	@$(MAKE) clean
	@echo ">>IMP make: creating shell..."
	@$(MAKE) imp
	@echo ">>IMP make: creating tex file..."
	@$(MAKE) tex
	@echo ">>IMP make: creating tex file - cleaning doc..."
	@$(MAKE) cleandoc
	@echo ">>IMP make: creating maude file..."
	@$(MAKE) maude
	@echo ">>IMP make: running examples..."
	@$(MAKE) test
	@echo ">>IMP make: done."

imp:
ifeq ($(MAUDE),)
	@echo ">>IMP make: Command line should be make imp -B MAUDE=maude-path"
	@exit 1
endif
	@./genimp $(MAUDE) $(PWD) > bin/imp.sh
ifneq (, $(wildcard ./bin/imp.sh))
	@chmod +x bin/imp.sh
endif
ifeq (, $(wildcard ./imp))
	@ln -s bin/imp.sh ./imp
	@chmod +x imp
endif

tex:
	@noweave -delay imp.noweb > doc/imp.tex
	@pdflatex -halt-on-error -output-directory=doc doc/imp.tex > /dev/null 2>&1
	@pdflatex -halt-on-error -output-directory=doc doc/imp.tex > /dev/null 2>&1

maude:
	@notangle -Rimp.maude imp.noweb > maude/imp.maude

clean:
	@$(MAKE) cleanbin
	@$(MAKE) cleandoc
ifneq (, $(wildcard ./maude/imp.maude))
	@rm ./maude/imp.maude
endif

cleanbin:
ifneq (, $(wildcard ./imp))
	@rm ./imp
endif
ifneq (, $(wildcard ./bin/imp.sh))
	@rm ./bin/imp.sh
endif

cleandoc:
ifneq (, $(wildcard ./doc/imp.aux))
	@rm ./doc/imp.aux
endif
ifneq (, $(wildcard ./doc/imp.out))
	@rm ./doc/imp.out
endif
ifneq (, $(wildcard ./doc/imp.log))
	@rm ./doc/imp.log
endif
ifneq (, $(wildcard ./doc/imp.tex))
	@rm ./doc/imp.tex
endif

test:
	./imp $(wildcard examples/*.imp)
