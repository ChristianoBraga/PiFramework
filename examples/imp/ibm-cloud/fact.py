y = 1
def fact(x) :
      while not(x == 0) :
         global y
         y = y * x
         x = x - 1
      z = y
      y = 1
      return z
