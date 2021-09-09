# Fun Interpreter User Guide

Christiano Braga  
Universidade Federal Fluminense  
Beta version of September, 2021

## Fun syntax by example

### Factorial function
```python
fun fat(x) =
    if x == 0
    then 1
    else x * fat(x - 1),
fat(10)	
```

### Fibonacci funtion

```python
fun fib(x) =
    if x == 0 then 0
    else if x == 1 then 1
          else fib(x - 1) + fib(x - 2),
fibo(10)  
```

## Invoking the interpreter

```
$ ./fun
🎉 Fun Interpreter
Beta version, Sep. 2021
Fun > 
```

## Interpreter commands


### Quit
```
Fun > q
```

```
Fun > quit
```

### Loading

#### From string

```
Fun > load "fun fat(x) = if x == 0 then 1 else x * fat(x - 1), fat(10)"
```

#### From file

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun >
```

### Show

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun > show
fun fat(x) =
    if x == 0
    then 1
    else x * fat(x - 1)
Fun > 
```

### Invoking the lexer

#### From string
```
Fun > lex "fun fat(x) = if x == 0 then 1 else x * fat(x - 1), fat(10)"
token(fun) token(idn) token(() token('fat) token()) token(() token(idn) token(() token('x) token()) token()) token(=) token(if) token(idn) token(() token('x) token()) token(
    ==) token(rat) token(() token(0) token()) token(then) token(rat) token(() token(1) token()) token(else) token(idn) token(() token('x) token()) token(*) token(idn) token(()
    token('fat) token()) token(() token(idn) token(() token('x) token()) token(-) token(rat) token(() token(1) token()) token()) 
Fun > 
```

### From file

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun > lex
token(fun) token(idn) token(() token('fat) token()) token(() token(idn) token(() token('x) token()) token()) token(=) token(if) token(idn) token(() token('x) token()) token(
    ==) token(rat) token(() token(0) token()) token(then) token(rat) token(() token(1) token()) token(else) token(idn) token(() token('x) token()) token(*) token(idn) token(()
    token('fat) token()) token(() token(idn) token(() token('x) token()) token(-) token(rat) token(() token(1) token()) token()) 
Fun > 
```

### Invoking the parser

#### From string

```
Fun > parse "fun fat(x) = if x == 0 then 1 else x * fat(x - 1)"
fun idn('fat)(idn('x)) = if idn('x) == rat(0) then rat(1) else idn('x) * idn('fat)(idn('x) - rat(1)) :: Expr
Fun > 
```

#### From file

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun > parse
fun idn('fat)(idn('x)) = if idn('x) == rat(0) then rat(1) else idn('x) * idn('fat)(idn('x) - rat(1)) :: Expr
Fun > 
```

### Running the interpreter

#### From string
```
run "fun fat(x) = if x == 0 then 1 else x * fat(x - 1), fat(10)"
3628800
Fun > 
```

- Note: this command takes into account a previously loaded file. This
allows one to load a function declaration and apply it as many times
as one wants.

- In the example below, the file ```fat.fun``` only declares the
  factorial function, leaving the application (call) to the ```run``` command.

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun > run "fat(10)"
3628800
Fun > 
```

#### From file

```
Fun > fload "fat.fun"
File fat.fun loaded!
Fun > run
3628800
Fun > 
```

- If the code has already a function application than a simple
  ```run``` after loading the file will execute the application.
