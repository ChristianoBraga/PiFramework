load fun

red out(exec(

fun idn('fib) (idn('x)) = 
    if idn('x) == rat(0)
    then rat(0)
    else if idn('x) == rat(1)
         then rat(1)
	 else
	      idn('fib)(idn('x) - rat(1)) + idn('fib)(idn('x) - rat(2)), 

idn('fib)(rat(4))

)) .

quit

red comp(

fun idn('fib) (idn('x)) = 
    if idn('x) == rat(0)
    then rat(0)
    else if idn('x) == rat(1)
         then rat(1)
	 else
	      idn('fib)(idn('x) - rat(1)) + idn('fib)(idn('x) - rat(2)), 

idn('fib)(rat(4))

) .

