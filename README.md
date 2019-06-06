<p align="left">
<img width=20% src="./logo/pi-logo.png">
</p>

The &pi; framework aims at being a simple formal framework for
compiler construction. It is comprised of &pi IR and
&Pi; automata. The &Pi; IR component is a simple language with basic
programming languages constructs, whose semantics are formally
specified in &Pi; automata. To construct a compiler for a programming
language one simply needs to define the &Pi; denotations of the
statements of the given programming language in terms of &Pi; IR
constructions. Using one of the implementations of &Pi; IR, one may
then execute programs in the given language or validate it using
formal verification tools.  At the moment, there are implementations
of the &Pi; framework in [Maude](http://maude.cs.uiuc.edu) and Python,
both developed by Christiano Braga (<http://www.ic.uff.br/~cbraga>).

## System requirements

* This version of &Pi; runs on version 2.7.1 of the
  [Maude](http://maude.cs.uiuc.edu) system and on [Python
  3](http://python.org).
* [iTerm 2](https://www.iterm2.com) on [macOS](https://www.apple.com/br/macos/) produces a nicer experience for the Maude implementation.

## Acknowledgements

The &Pi; framework is a result of a collaboration with [Fabrício
Chalub](http://fcbr.github.io), [José
Meseguer](https://dblp.uni-trier.de/pers/hd/m/Meseguer:Jos=eacute=)
and [Peter D. Mosses](http://www.cs.swan.ac.uk/~cspdm/). The signature
of &Pi; IR has the same roots as the [Component Based
Semantics](https://plancomps.csle.cs.rhul.ac.uk/taosd2015/) in the
[Programming Language Components and Specifications
project](https://plancomps.csle.cs.rhul.ac.uk/). The &Pi; automata
formalism is a generalization of Plotkin's Interpreting Automata.


