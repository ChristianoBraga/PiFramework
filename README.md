<p align="left">
<img width=25% src="./logo/pi-logo.png">
</p>

The &pi; framework aims at being a simple formal framework for compiler construction. It is comprised of &pi;-lib and &pi;-automata. The &pi;-libcomponent is a library of basic programming languages constructs whose semantics are formally specified in &pi;-automata. To construct a compiler for a programming language one simply needs to define the &pi;-denotations of the statements of the given programming language in terms of &pi;-lib constructions. Using one of the implementations of &pi;-lib, one may then execute programs in the given language or validate it using formal verification tools. 
At the moment, there are implementaitions of the &pi; frmaework in [Maude](http://maude.cs.uiuc.edu) language and Python, deloped by Christiano Braga (<http://www.ic.uff.br/~cbraga>).

## System requirements

* This version of &pi;-lib runs on version 2.7.1 of the [Maude](http://maude.cs.uiuc.edu) system. 
* [iTerm 2](https://www.iterm2.com) on [macOS](https://www.apple.com/br/macos/) produces a nicer experience.

## Acknowledgements

&pi;-lib is a result of a collaboration with [Fabrício Chalub](http://fcbr.github.io), [José Meseguer](https://dblp.uni-trier.de/pers/hd/m/Meseguer:Jos=eacute=) and [Peter D. Mosses](http://www.cs.swan.ac.uk/~cspdm/). The signature of &pi;-lib has the same roots as the [Component Based Semantics](https://plancomps.csle.cs.rhul.ac.uk/taosd2015/) in the [Programming Language Components and Specifications project](https://plancomps.csle.cs.rhul.ac.uk/). The semantic framework that &pi;-lib implements is &pi;-automata, a generalization of Plotkin's Interpreting Automata.


