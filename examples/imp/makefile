export MAUDE
TEXINPUTS := $(PWD)/../../doc/:$(TEXINPUTS)

all:
	@echo ">>IMP make: cleaning up..."
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
	@chmod +x ./genimp
	@chmod +x ./imgcat
	@./genimp $(MAUDE) . > imp
	@chmod +x imp

tex:	
	@echo ">>IMP make: creating documentation..."
ifeq (, $(wildcard ./doc))
	@mkdir ./doc
endif
	@noweave -delay imp.noweb > ./doc/imp.tex
	@pdflatex -halt-on-error -output-directory=doc ./doc/imp.tex > /dev/null 2>&1
	@pdflatex -halt-on-error -output-directory=doc ./doc/imp.tex > /dev/null 2>&1

maude:
ifeq (, $(wildcard ./maude))
	@mkdir ./maude
endif
	@notangle -Rimp.maude imp.noweb > maude/imp.maude

clean:
ifneq (, $(wildcard ./imp))
	@rm ./imp
endif
ifneq (, $(wildcard ./bin))
	@rm -fr ./bin
endif
ifneq (, $(wildcard ./doc))
	@rm -fr ./doc
endif
ifneq (, $(wildcard ./maude))
	@rm -fr ./maude
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
	@./imp $(wildcard examples/*.imp)
