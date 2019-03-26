# Π denotations for Imπ

Christiano Braga  
Universidade Federal Fluminense  
http://www.ic.uff.br/~cbraga  
\
March 2019  
\
http://github.com/ChristianoBraga/PiFramework

## Introduction

A compiler for the Imπ language is defined by means of functions mapping constructions from the Imπ language to π IR.

## Imπ grammar
```
<S> ::=  <cmd>

<cmd> ::= 'nop' | <let> | <assign> | <loop> | <call>

<call> ::= <identifier> '(' <actual> ')' 

<actual> ::= <expression> (',' <expression>)* | ε

<loop> ::= 'while' <expression> 'do' <cmd>+ 

<assign> ::= <identifier> ':=' <expression>

<let> ::= 'let' <dec> 'in' <cmd>+  

<dec> ::= <var> | <fn>
    
<var> ::= 'var' <identifier> '=' <expression>

<fn> ::= 'fn' <identifier> '(' <formal> ')' '=' <cmd>

<formal> ::= <identifier> (',' <identifier>)*  | ε

<expression> ::= <bool_expression> | <arith_expression>

<bool_expression> ::= <negation> | <equality> | <conjunction> | <disjunction>
                | <lowereq> | <greatereq> | <lowerthan> | <greaterthan> 
                
<equality> ::= <arith_expression> "==" <expression>

<conjunction> ::= <bool_expression> "and" <bool_expression>

<disjunction> ::= <bool_expression> "or" <bool_expression>

<lowereq> ::= <arith_expression> "<=" <arith_expression>

<greatereq> ::= <arith_expression> ">=" <arith_expression>

<lowerthan> ::= <arith_expression> "<" <arith_expression>

<greaterthan> ::= <arith_expression> ">" <arith_expression>

<parentesisexp> ::= '(' <bool_expression> ')' 

<negation> ::= 'not' <bool_expression> 

<arith_expression> ::= <addition> | <subtraction> | <mult_expression> | <division>

<addition> ::= <mult_expression> "+" <arith_expression>

<subtraction> ::= <mult_expression> "-" <arith_expression>

<mult_expression> ::= <multiplication> | <division> | <atom> | <parentesisexp> 

<multiplication> ::= <atom> "*" <mult_expression>

<division> ::= <atom> "/" <mult_expression>

<atom> ::= <number> | <truth> | <identifier>
 
<number> ::= /\d+/ 

<identifier> ::= /(?!\d)\w+/ 

<truth> ::= 'True' | 'False' 
```

## Π denotations

A π denotation for the Imπ language is a function 

> _⟦⋅⟧ : Gimp → Gπ_,   

intentionally defined, that associates (a class of) words derivable by Imπ's grammar with (a class of words) words derivable by π IR grammar.

### Expressions

Let _ast ∈ L(Gimp)_,

1. _⟦ identifier(ast) ⟧ = Id(str(ast))_, where function _str_ returns a string given an `<identifier>`. 

1. _⟦ number(ast) ⟧ = Num(int(ast))_, where function _int_ returns an integer given a `<number>`.

1. _⟦ addition(ast) ⟧ = Sum( ⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_, where functions _left_ and _right_ return the left branch and right branches of _ast_, respectively.

1. _⟦ subtraction(ast) ⟧ = Sub(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ multiplication(ast) ⟧ = Mul(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ division(ast) ⟧ = Div(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ truth(ast) ⟧ = Boo(bool(ast))_, where function _bool_ returns a Boolean value given a `<truth>` token.

1. _⟦ negation(ast) ⟧ = Not( ⟦ ast ⟧ )_

1. _⟦ equality(ast) ⟧ = Eq(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ lowerthan(ast) ⟧ = Lt(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ greaterthan(ast) ⟧ = Gt(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ lowereq(ast) ⟧ = Le⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ greatereq(ast) ⟧ = Ge(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ conjunction(ast) ⟧ = And(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ disconjunction(ast) ⟧ = Or(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ nop(ast) ⟧ = Nop_

### Declarations

Let _mkAbs : `<formal>` × `<cmd>` → `<Abs>` be
> _mkAbs([], c) = Abs([], ⟦ c ⟧)_
> _mkAbs(h :: ls, b) = Abs(⟦ h ⟧ :: mkFor(ls), ⟦ c ⟧)_  

and _mkFor : `<identifier>*` → `<Id>*`_
> _mkFor([]) = []  
> _mkFor(h :: ls) = ⟦ h ⟧ :: mkFor(ls)_

1. _⟦ var(ast) ⟧ = Bind(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ fn(ast) ⟧ = Bind(⟦ fst(ast) ⟧, mkAbs(snd(ast), trd(ast))_

### Commands

Let _mkCSeq : `<cmd>+` → `<CSeq>`_ be defined by the following equations,  
> _mkCSeq([h]) = h_,  
> _mkCSeq(h::ls) = CSeq(⟦ h ⟧ , mkCSeq(ls))_,  

and _mkAct : `<actual>` → `<Exp>*`_ be as follows
> _mkAct([]) = []_,  
> _mkAct(h::ls) = ⟦ h ⟧ :: mkAct(ls))_.


1. _⟦ assign(ast) ⟧ = Assign(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_

1. _⟦ let(ast) ⟧ = Blk(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_, if _right(ast) ∈ `<cmd>`
1. _⟦ let(ast) ⟧ = Blk(⟦ left(ast) ⟧, mkCSeq(right(ast)))_, if _right(ast) ∈ `<cmd>+`_  
1. _⟦ loop(ast) ⟧ = Loop(⟦ left(ast) ⟧, ⟦ right(ast) ⟧)_, if _right(ast) ∈ `<cmd>`_  
1. _⟦ loop(ast) ⟧ = Loop(⟦ left(ast) ⟧, mkCSeq(right(ast)))_, if _right(ast) ∈ `<cmd>+`_

1. _⟦ call(ast) ⟧ = Call(⟦ left(ast) ⟧, mkAct(right(ast)))_
