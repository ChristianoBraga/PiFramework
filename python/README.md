# Imπ

Imπ is a simple imperative programming language created to illustrate the use of the Python implementation of [π framework](http://github/ChristianoBraga/PiFraework), by [Christiano Braga](http://github.com/ChristianoBraga).

Support for LLVM code generation being developed by [Fernando Mendes](https://github.com/fjmendes1994).

## Documentation

* Christiano Braga, Notes on formal compiler construction with the π Framework, Oct. 2018 ([slides](https://github.com/ChristianoBraga/PiFramework/blob/master/slides/slides.pdf)).
* Fernando Mendes, Geração de código LLVM - π Framework, 25/10/2018 ([slides](http://github.com/ChristianoBraga/PiFramework/blob/master/python/Pi_Framework___LLVM.pdf), in Portuguese).

## Requirements

* Python 3
* [竜 Tatsu](https://github.com/neogeny/TatSu) parser generator.
* [LLVM lite](https://github.com/numba/llvmlite).

## Example

Running the command line 

`python imp.py -f iter-fact.imp --last 1 -s --stats` 

produces the following output:

```shell
Imπ source code:
# The classic iterative factorial example
let var z = 1
in
    let var y = 10
    in
        while not (y == 0)
        do
            z := z * y
            y := y - 1

State #232 of the π automaton:
locs : [0]
env : {'z': 0}
sto : {0: 3628800}
val : [[], {}]
cnt : ['#BLKCMD']

Number of evaluation steps: 234
Evaluation time: 0:00:00.004149
```
while 
`python imp.py -f fun-fact.imp --last 1 -s --stats` 

produces the following one:

```shell
Imπ source code:
# In this example we encapsulate the iterative calculation
# of the factorial within a function call.
let var z = 1
in
    let fn f(x) =
        let var y = x
        in
            while not (y == 0)
            do
                z := z * y
                y := y - 1
    in f(10)


State #240 of the π automaton:
locs : [0]
env : {'z': 0}
sto : {0: 3628800}
val : [[], {}]
cnt : ['#BLKCMD']

Number of evaluation steps: 242
Evaluation time: 0:00:00.006342
```

LLVM code is generated using option `--llvm` as in
`python imp.py -f iter-fact.imp --llvm`
producing the following output:

```llvm
; ModuleID = "main_module"
target triple = "x86_64-apple-darwin18.0.0"
target datalayout = ""

define i64 @"main_function"()
{
entry:
  %"ptr" = alloca i64
  store i64 1, i64* %"ptr"
  %"ptr.1" = alloca i64
  store i64 10, i64* %"ptr.1"
  br label %"loop"
loop:
  %"val" = load i64, i64* %"ptr.1"
  %"temp_eq" = icmp eq i64 %"val", 0
  %"temp_not" = xor i1 %"temp_eq", -1
  %"val.1" = load i64, i64* %"ptr"
  %"val.2" = load i64, i64* %"ptr.1"
  %"tmp_mul" = mul i64 %"val.1", %"val.2"
  store i64 %"tmp_mul", i64* %"ptr"
  %"val.3" = load i64, i64* %"ptr.1"
  %"tmp_sub" = sub i64 %"val.3", 1
  store i64 %"tmp_sub", i64* %"ptr.1"
  br i1 %"temp_not", label %"loop", label %"after_loop"
after_loop:
  ret i64 0
}
```
