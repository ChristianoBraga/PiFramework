# Author: Christiano Braga
# http://github.com/ChristianoBraga

import pi
from tatsu import ast

class Impiler(object):
    def paren_exp(self, ast):
        return ast.e
    
    def identifier(self, ast):
        return pi.Id(str(ast))

    def number(self, ast):
        return pi.Num(int(ast))

    def un_exp(self, ast):
        if ast.op == "not":
            return pi.Not(ast.e)
        
    def bin_exp(self, ast):
        if ast.op == "+":
            return pi.Sum(ast.e1, ast.e2)
        elif ast.op == "-":
            return pi.Sub(ast.e1, ast.e2)        
        elif ast.op == "*":
            return pi.Mul(ast.e1, ast.e2)        
        elif ast.op == "/":
            return pi.Div(ast.e1, ast.e2)        
        elif ast.op == "and":
            return pi.And(ast.e1, ast.e2)        
        elif ast.op == "or":
            return pi.Or(ast.e1, ast.e2)        
        elif ast.op == "<":
            return pi.Lt(ast.e1, ast.e2)        
        elif ast.op == "<=":
            return pi.Le(ast.e1, ast.e2)        
        elif ast.op == ">":
            return pi.Gt(ast.e1, ast.e2)        
        elif ast.op == ">=":
            return pi.Ge(ast.e1, ast.e2)        
        elif ast.op == "==":
            return pi.Eq(ast.e1, ast.e2)        
    
    def truth(self, ast):
        return pi.Boo(bool(ast))

    def assign(self, ast):
        return pi.Assign(ast.idn, ast.e)

    def print(self, ast):
        return pi.Print(ast.e)
    
    def const(self, ast):
        return pi.Bind(ast.idn, ast.e) 

    def var(self, ast):
        if isinstance(ast.idn, list):
            bind = pi.Bind(ast.idn[0], pi.Ref(ast.e[0]))
            for i in range(1, len(ast.idn)):
                bind = pi.DSeq(bind, pi.Bind(ast.idn[i], pi.Ref(ast.e[i])))
            return bind
        else:
            return pi.Bind(ast.idn, pi.Ref(ast.e))

    def skip(self, ast):
        return pi.Nop() 

    def decSeq(self, ast):
        if ast:
            if isinstance(ast.d, list):
                bind = ast.d[0]
                for e in ast.d[1:]:
                    bind = pi.DSeq(bind, e)
                return bind
            else:
                return ast.d

    def __blk_aux(self, ds, cs):
        if len(ds) > 1:
            return pi.Blk(ds[0], self.__blk_aux(ds[1:], cs))
        else:
            return pi.Blk(ds[0], cs)
            
    def __blk(self, ds, cs):
        if isinstance(ds, pi.Bind):
            return pi.Blk(ds, cs)
        elif isinstance(ds, pi.DSeq):
            return self.__blk_aux(ds.operands(), cs)
        else:
            raise Exception("Block parse error: " + str(ds) + " "  + str(cs) + ".")
            
    def blk(self, ast):
        if ast.ds:
            if ast.cs:
                return self.__blk(ast.ds, ast.cs)
            else:
                return self.__blk(ast.ds, pi.Nop())
        else:
            if ast.cs:
                return pi.Blk(ast.cs)
            else:
                return pi.Blk(pi.Nop())
        
    def start(self, ast):
        return self.blk(ast)

    def cmd_seq(self, ast):
        if isinstance(ast.ac, list):
            cs = ast.ac[0]
            for c in ast.ac[1:]:
                cs = pi.CSeq(cs, c)
            return cs
        else:
            return ast.ac
        
    def let(self, ast):
        return pi.Blk(ast.ds, ast.c)

    def loop(self, ast):
        return pi.Loop(ast.t, ast.b)

    def cond(self, ast):
        if ast.b2:
            return pi.Cond(ast.t, ast.b1, ast.b2)
        else:
            return pi.Cond(ast.t, ast.b1, pi.Nop())        

    def __makeAbs(self, f, c):
        assert(isinstance(f, list))
        if isinstance(c, pi.Blk):
            body = c
        else:
            body = pi.Blk(c)
        if f == []:
            return pi.Abs(pi.Formals(), body)
        else:
            # Tatsu roduces list of identifiers and commas from
            # formals = ','%{ identifiers }
            formals = [e for e in f if e != ',']
            return pi.Abs(formals, body)

    def fn(self, ast):
        body = self.__makeAbs(ast.f, ast.b)
        return pi.BindAbs(ast.idn, body)

    def rec(self, ast):
        body = self.__makeAbs(ast.f, ast.b)
        return pi.BindRecAbs(ast.idn, body)

    def call(self, ast):
        actuals = [e for e in ast.a if e != ',']
        return pi.Call(ast.idn, actuals)
