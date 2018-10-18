# Imπ

Imπ is a simple imperative programming language created to illustrate the use of the Python implementation of [π framework](http://github/ChristianoBraga/PiFraework), by [Christiano Braga](http://github.com/ChristianoBraga).

Support for LLVM code generation being developed by [Fernando Mendes](https://github.com/fjmendes1994).

## Requirements

* Python 3
* [竜 Tatsu](https://github.com/neogeny/TatSu) parser generator.
* [LLVM lite](https://github.com/numba/llvmlite).

## Example

Running the command line 

`python imp.py -f iter-fact.imp --last 1 -s --stats` 

should produce the following output:

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