from termcolor import colored

#
# Basic concepts
#

COLORED = False

class IllFormed(Exception):
    def __str__(self):
        return "Ill formed Π IR AST: " + colored(self.args, 'red')

class Statement:
    __opr = []
    def __init__(self, *args):
        self.__opr = list(args)
        
    def __str__(self):
        if COLORED:
            ret = colored(str(self.__class__.__name__), None, attrs = ['bold']) + "("
        else:
            ret = str(self.__class__.__name__) + "("
        if len(self.__opr) > 0:
            ret += str(self.__opr[0])
            if len(self.__opr) > 1:
                for i in range(1, len(self.__opr)):
                    ret += ", "
                    ret += str(self.__opr[i])
        ret += ")"
        return ret

    def __repr__(self):
        return str(self)

    def arity(self):
        return len(self.__opr)

    def operands(self):
        return self.__opr
    
    def operand(self, n):
        if self.arity() > 0:
            return self.__opr[n]
        else:
            raise IllFormed("Call to 'operand' on " +
                        str(self) + ": " + "No operands.")

    def operator(self):
        return str(self.__class__.__name__)

class ValueStack(list):
    pass


class ControlStack(list):
    pass


class EvaluationError(Exception):
    def __init__(self, args):
        self.trace = ""
    def __str__(self):
        return "Π automaton evluation error: " + str(self.args)

class PiAutomaton(dict):

    def __init__(self):
        self["val"] = ValueStack()
        self["cnt"] = ControlStack()

    def __str__(self):
        ret = ""
        for k, v in self.items():
            if COLORED:
                cidx = colored(str(k), 'blue')
            else:
                cidx = str(k)
            ret += cidx + " : " + str(v) + '\n'

        return ret

    def val(self):
        return self["val"]

    def cnt(self):
        return self["cnt"]

    def pushVal(self, v):
        vs = self.val()
        vs.append(v)

    def popVal(self):
        vs = self.val()
        if len(vs) > 0:
            v = vs[len(vs) - 1]
            vs.pop()
            return v
        else:
            raise EvaluationError(
                "Call to 'popVal' on empty value stack: <" + str(self) + ">.")

    def pushCnt(self, e):
        cnt = self.cnt()
        cnt.append(e)

    def popCnt(self):
        cs = self.cnt()
        if len(cs) > 0:
            c = cs[len(cs) - 1]
            cs.pop()
            return c
        else:
            raise IllFormed(
                "Call to 'popCnt' on empty control stack: <" + str(self) + ">.")


    def emptyCnt(self):
        return len(self.cnt()) == 0

#
# Expressions
#
    
class Exp(Statement):

    def left_operand(self):
        if self.arity() == 2:
            return self.operand(0)
        else:
            raise IllFormed("Call to 'left_operand' on " +
                            str(self) + ": " + "Operator is not binary.")


    def right_operand(self):
        if self.arity() == 2:
            return self.operand(1)
        else:
            raise IllFormed("Call to 'right_operand' on " +
                            str(self) + ": " + "Operator is not binary.")


class ArithExp(Exp):
    pass

class Num(ArithExp):
    def __init__(self, n):
        if isinstance(n, int):
            ArithExp.__init__(self, n)
        else:
            raise IllFormed(self, n)

    def __str__(self):
        if COLORED:
            ret = colored(self.num(), 'magenta')
        else:
            ret = str(self.num())
        return ret

        
    def num(self):
        return self.operand(0)


class Sum(ArithExp):
    def __init__(self, e1, e2):
        if isinstance(e1, Exp):
            if isinstance(e2, Exp):
                ArithExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Sub(ArithExp):
    def __init__(self, e1, e2):
        if isinstance(e1, Exp):
            if isinstance(e2, Exp):
                ArithExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Mul(ArithExp):
    def __init__(self, e1, e2):
        if isinstance(e1, Exp):
            if isinstance(e2, Exp):
                ArithExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Div(ArithExp):
    def __init__(self, e1, e2):
        if isinstance(e1, Exp):
            if isinstance(e2, Exp):
                ArithExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class BoolExp(Exp):
    pass


class Boo(BoolExp):
    def __init__(self, t):
        if isinstance(t, bool):
            BoolExp.__init__(self, t)
        else:
            raise IllFormed(self, t)

    def boo(self):
        return self.operand(0)


class Eq(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, Exp):
            if isinstance(e2, Exp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Lt(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, ArithExp):
            if isinstance(e2, ArithExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Le(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, ArithExp):
            if isinstance(e2, ArithExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Gt(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, ArithExp):
            if isinstance(e2, ArithExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Ge(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, ArithExp):
            if isinstance(e2, ArithExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class And(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, BoolExp):
            if isinstance(e2, BoolExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Or(BoolExp):
    def __init__(self, e1, e2):
        if isinstance(e1, BoolExp):
            if isinstance(e2, BoolExp):
                BoolExp.__init__(self, e1, e2)
            else:
                raise IllFormed(self, e2)
        else:
            raise IllFormed(self, e1)


class Not(BoolExp):
    def __init__(self, e):
        if isinstance(e, BoolExp):
            BoolExp.__init__(self, e)
        else:
            raise IllFormed(self, e)

class ExpKW():
    SUM = "#SUM"
    SUB = "#SUB"
    MUL = "#MUL"
    DIV = "#DIV"
    EQ = "#EQ"
    LT = "#LT"
    LE = "#LE"
    GT = "#GT"
    GE = "#GE"
    AND = "#AND"
    OR = "#OR"
    NOT = "#NOT"

class ExpPiAut(PiAutomaton):

    def __evalSum(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.SUM)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalSumKW(self, e):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 + v2)


    def __evalDiv(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.DIV)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalDivKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        if v2 == 0:
            raise EvaluationError(str(self) + " Division by zero!")
        else:
            self.pushVal(v1 / v2)


    def __evalMul(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.MUL)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalMulKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()

        self.pushVal(v1 * v2)


    def __evalSub(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.SUB)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalSubKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 - v2)


    def __evalNum(self, n):
        f = n.num()
        self.pushVal(f)


    def __evalBoo(self, t):
        th = t.boo()
        self.pushVal(th)


    def __evalEq(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.EQ)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalEqKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 == v2)


    def __evalLt(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.LT)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalLtKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 < v2)


    def __evalGt(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.GT)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalGtKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 > v2)


    def __evalLe(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.LE)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalLeKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 <= v2)


    def __evalGe(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.GE)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalGeKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        if (isinstance(v1, Num)):
            v1 = v1.num()
        if (isinstance(v2, Num)):
            v2 = v2.num()
        self.pushVal(v1 >= v2)


    def __evalAnd(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.AND)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalAndKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 and v2)


    def __evalOr(self, e):
        e1 = e.left_operand()
        e2 = e.right_operand()
        self.pushCnt(ExpKW.OR)
        self.pushCnt(e1)
        self.pushCnt(e2)


    def __evalOrKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 or v2)


    def __evalNot(self, e):
        e = e.operand(0)
        self.pushCnt(ExpKW.NOT)
        self.pushCnt(e)


    def __evalNotKW(self):
        v = self.popVal()
        self.pushVal(not v)


    def eval(self):
        e = self.popCnt()
        if isinstance(e, Sum):
            self.__evalSum(e)
        elif e == ExpKW.SUM:
            self.__evalSumKW(e)
        elif isinstance(e, Sub):
            self.__evalSub(e)
        elif e == ExpKW.SUB:
            self.__evalSubKW()
        elif isinstance(e, Mul):
            self.__evalMul(e)
        elif e == ExpKW.MUL:
            self.__evalMulKW()
        elif isinstance(e, Div):
            self.__evalDiv(e)
        elif e == ExpKW.DIV:
            self.__evalDivKW()
        elif isinstance(e, Num):
            self.__evalNum(e)
        elif isinstance(e, Boo):
            self.__evalBoo(e)
        elif isinstance(e, Eq):
            self.__evalEq(e)
        elif e == ExpKW.EQ:
            self.__evalEqKW()
        elif isinstance(e, Lt):
            self.__evalLt(e)
        elif e == ExpKW.LT:
            self.__evalLtKW()
        elif isinstance(e, Le):
            self.__evalLe(e)
        elif e == ExpKW.LE:
            self.__evalLeKW()
        elif isinstance(e, Gt):
            self.__evalGt(e)
        elif e == ExpKW.GT:
            self.__evalGtKW()
        elif isinstance(e, Ge):
            self.__evalGe(e)
        elif e == ExpKW.GE:
            self.__evalGeKW()
        elif isinstance(e, And):
            self.__evalAnd(e)
        elif e == ExpKW.AND:
            self.__evalAndKW()
        elif isinstance(e, Or):
            self.__evalOr(e)
        elif e == ExpKW.OR:
            self.__evalOrKW()
        elif isinstance(e, Not):
            self.__evalNot(e)
        elif e == ExpKW.NOT:
            self.__evalNotKW()
        else:
            raise EvaluationError( \
                "Don't know how to evaluate " + str(e) + " of type " + str(type(e)) + "." + \
                "\nCall to 'eval' on \n" + str(self))

#
# Commands
#
        
class Cmd(Statement):
    pass

class Nop(Cmd):
    pass

class Id(ArithExp, BoolExp):
    def __init__(self, s):
        if isinstance(s, str):
            Exp.__init__(self, s)
        else:
            raise IllFormed(self, s)

    def id(self):
        return self.operand(0)


class Print(Cmd):

    def __init__(self, e):
        if isinstance(e, Exp):
            Cmd.__init__(self, e)
        else:
            raise IllFormed(self, e)

    def exp(self):
        return self.operand(0)

class Assign(Cmd):

    def __init__(self, i, e):
        if isinstance(i, Id):
            if isinstance(e, Exp):
                Cmd.__init__(self, i, e)
            else:
                raise IllFormed(self, e)
        else:
            raise IllFormed(self, i)


    def lvalue(self):
        return self.operand(0)


    def rvalue(self):
        return self.operand(1)


class Loop(Cmd):
    def __init__(self, be, c):
        if isinstance(be, BoolExp):
            if isinstance(c, Cmd):
                Cmd.__init__(self, be, c)
            else:
                raise IllFormed(self, c)
        else:
            raise IllFormed(self, be)

    def cond(self):
        return self.operand(0)

    def body(self):
        return self.operand(1)

class Cond(Cmd):
    def __init__(self, be, c1, c2):
        if isinstance(be, BoolExp):
            if isinstance(c1, Cmd):
                if isinstance(c2, Cmd):                
                    Cmd.__init__(self, be, c1, c2)
                else:
                    raise IllFormed(self, c2)
            else:
                raise IllFormed(self, c1)
        else:
            raise IllFormed(self, be)

    def cond(self):
        return self.operand(0)

    def then_branch(self):
        return self.operand(1)

    def else_branch(self):
        return self.operand(2)

class CSeq(Cmd):
    def __init__(self, c1, c2):
        if isinstance(c1, Cmd):
            if isinstance(c2, Cmd):
                Cmd.__init__(self, c1, c2)
            else:
                raise IllFormed(self, c2)
        else:
            raise IllFormed(self, c1)

    def left_cmd(self):
        return self.operand(0)

    def right_cmd(self):
        return self.operand(1)

class Env(dict):
    pass


class Loc(int):
    pass


class Sto(dict):
    pass


class CmdKW:
    ASSIGN = "#ASSIGN"
    LOOP   = "#LOOP"
    COND   = "#COND"
    PRINT  = "#PRINT" 

class CmdPiAut(ExpPiAut):

    def __init__(self):
        self["env"] = Env()
        self["sto"] = Sto()
        self["out"] = []
        ExpPiAut.__init__(self)

    def env(self):
        return self["env"]

    def out(self):
        return self["out"]

    def getBindable(self, i):
        en = self.env()
        if i in en.keys():
            return en[i]
        else:
            raise EvaluationError("Undeclared identifier: '" + \
                                  str(i) + "' not in environment " + str(en))

    def sto(self):
        return self["sto"]

    def __newLoc(self):
        sto = self.sto()
        if sto:
            return Loc(max(list(sto.keys())) + 1)
        else:
            return Loc()

    def extendStore(self, v):
        st = self.sto()
        l = self.__newLoc()
        st[l] = v
        return l

    def updateStore(self, l, v):
        st = self.sto()
        if l in st.keys():
            st[l] = v
        else:
            raise EvaluationError("Call to updateStore with location " + str(l) + " not in store.")

    def __emmit(self, e):
        self["out"].append(e)
        
    def __evalPrint(self, c):
        e = c.exp()
        self.pushCnt(CmdKW.PRINT)
        self.pushCnt(e)

    def __evalPrintKW(self):
        v = self.popVal()
        self.__emmit(v)
        
    def __evalAssign(self, c):
        i = c.lvalue()
        e = c.rvalue()
        self.pushVal(i.id())
        self.pushCnt(CmdKW.ASSIGN)
        self.pushCnt(e)


    def __evalAssignKW(self):
        v = self.popVal()
        i = self.popVal()
        l = self.getBindable(i)
        self.updateStore(l, v)


    def __evalId(self, i):
        s = self.sto()
        b = self.getBindable(i)
        if isinstance(b, Loc):
            self.pushVal(s[b])
        else:
            self.pushVal(b)

    def __evalCond(self, c):
        be = c.cond()
        self.pushVal(c)
        self.pushCnt(CmdKW.COND)
        self.pushCnt(be)

    def __evalCondKW(self):
        t = self.popVal()
        c = self.popVal()
        if t:
            self.pushCnt(c.then_branch())
        else:
            self.pushCnt(c.else_branch())            
        
    def __evalLoop(self, c):
        be = c.cond()
        bl = c.body()
        self.pushVal(Loop(be, bl))
        self.pushVal(bl)
        self.pushCnt(CmdKW.LOOP)
        self.pushCnt(be)


    def __evalLoopKW(self):
        t = self.popVal()
        if t:
            c = self.popVal()
            lo = self.popVal()
            self.pushCnt(lo)
            self.pushCnt(c)
        else:
            self.popVal()
            self.popVal()


    def __evalCSeq(self, c):
        c1 = c.left_cmd()
        c2 = c.right_cmd()
        self.pushCnt(c2)
        self.pushCnt(c1)


    def eval(self):
        c = self.popCnt()
        if isinstance(c, Print):
            self.__evalPrint(c)
        elif c == CmdKW.PRINT:
            self.__evalPrintKW()
        elif isinstance(c, Assign):
            self.__evalAssign(c)
        elif c == CmdKW.ASSIGN:
            self.__evalAssignKW()
        elif isinstance(c, Nop):
            return
        elif isinstance(c, Id):
            self.__evalId(c.id())
        elif isinstance(c, Cond):
            self.__evalCond(c)
        elif c == CmdKW.COND:
            self.__evalCondKW()
        elif isinstance(c, Loop):
            self.__evalLoop(c)
        elif c == CmdKW.LOOP:
            self.__evalLoopKW()
        elif isinstance(c, CSeq):
            self.__evalCSeq(c)
        else:
            self.pushCnt(c)
            super().eval()

#
# Declarations
#
            
class Dec(Statement):
    pass


class Bind(Dec):
    def __init__(self, *args):
        if args == ():
            Dec.__init__(self, ())
        else:
            if len(args) == 2:
                i = args[0]
                e = args[1]
                if isinstance(i, Id):
                    if isinstance(e, Exp):
                        Dec.__init__(self, i, e)
                    else:
                        raise IllFormed(self, e)
                else:
                    raise IllFormed(self, i)
            else:
                raise IllFormed(self, args)

    def id(self):
        return self.operand(0)

    def bindable(self):
        return self.operand(1)


class Ref(Exp):
    def __init__(self, e):
        if isinstance(e, Exp):
            Exp.__init__(self, e)
        else:
            raise IllFormed(self, e)

    def exp(self):
        return self.operand(0)


class Cns(Exp):
    def __init__(self, e):
        if isinstance(e, Exp):
            Exp.__init__(self, e)
        else:
            raise IllFormed(self, e)

    def exp(self):
        return self.operand(0)


class Blk(Cmd):

    def __init__(self, *args):
        # Blocks with declarations
        if len(args) == 2:
            d = args[0]
            c = args[1]
            if isinstance(d, Dec):
                if isinstance(c, Cmd):
                    Cmd.__init__(self, d, c)
                else:
                    raise IllFormed(self, c)
            else: 
               raise IllFormed(self, d)
        # Blocks with no declarations
        elif len(args) == 1:
            c = args[0] 
            if isinstance(c, Cmd):
                Cmd.__init__(self, c)
            else:
                raise IllFormed(self, c)

    def dec(self):
        if self.arity() == 1:
            return None
        elif self.arity() == 2:    
            return self.operand(0)
        else:
            raise IllFormed(self)

    def cmd(self):
        if self.arity() == 1:
            return self.operand(0)
        elif self.arity() == 2:    
            return self.operand(1)
        else:
            raise IllFormed(self)

class DSeq(Dec):

    def __init__(self, d1, d2):
        if isinstance(d1, Dec):
            if isinstance(d2, Dec):
                Dec.__init__(self, d1, d2)
            else:
                raise IllFormed(self, d2)
        else:
            raise IllFormed(self, d1)

    def left_dec(self):
        return self.operand(0)

    def right_dec(self):
        return self.operand(1)

class DecExpKW(ExpKW):
    REF = "#REF"
    CNS = "#CNS"

class DecCmdKW(CmdKW):
    BLKDEC = "#BLKDEC"
    BLKCMD = "#BLKCMD"

class DecKW():
    BIND = "#BIND"
    DSEQ = "#DSEQ"

class DecPiAut(CmdPiAut):

    def __init__(self):
        self["locs"] = []
        CmdPiAut.__init__(self)

    def locs(self):
        return self["locs"]

    def pushLoc(self, l):
        ls = self.locs()
        ls.append(l)

    def __evalRef(self, e):
        ex = e.exp()
        self.pushCnt(DecExpKW.REF)
        self.pushCnt(ex)

    def __evalRefKW(self):
        v = self.popVal()
        l = self.extendStore(v)
        self.pushLoc(l)
        self.pushVal(l)

    def __evalBind(self, d):
        i = d.id()
        e = d.bindable()
        self.pushVal(i)
        self.pushCnt(DecKW.BIND)
        self.pushCnt(e)

    def __evalBindKW(self):
        l = self.popVal()
        i = self.popVal()
        x = i.id()
        self.pushVal({x : l})

    def __evalDSeq(self, ds):
        d1 = ds.left_dec()
        d2 = ds.right_dec()
        self.pushCnt(DecKW.DSEQ)
        self.pushCnt(d2)
        self.pushCnt(d1)

    def __evalDSeqKW(self):
        d2 = self.popVal()
        d1 = self.popVal()
        d1.update(d2)
        self.pushVal(d1)

    def __evalBlk(self, d):
        ld = d.dec()
        c = d.cmd()
        l = self.locs()
        self.pushVal(list(l.copy()))
        self["locs"] = []
        if ld:
            self.pushCnt(DecCmdKW.BLKDEC)
            self.pushCnt(ld)
            self.pushVal(c)
        else:
            # If the block has no declarations
            # we need to save the environment because the
            # evaluation of BLOCKCMD restores it.
            # There could be an opcode to capture this 
            # semantics such that saving and restoring an unchanged
            # environment does not happen, as it is now.
            self.pushVal(self.env())
            self.pushCnt(DecCmdKW.BLKCMD)
            self.pushCnt(c)

    def __evalBlkDecKW(self):
        d = self.popVal()
        c = self.popVal()
        en = self.env()
        ne = en.copy()
        ne.update(d)
        self.pushVal(en)
        self["env"] = ne
        self.pushCnt(DecCmdKW.BLKCMD)
        self.pushCnt(c)

    def __evalBlkCmdKW(self):
        # Retrieves the environment prior to the block evaluation.
        en = self.popVal()
        # Restores the environment prior to the block evaluation.
        self["env"] = en
        # Stores in 's' the locations prior to the block evaluation.
        cl = self.locs()
        s = self.sto()
        s = {k: v for k, v in s.items() if k not in cl}
        # Removes the locations created in the terminating block from the store.
        self["sto"] = s
        # Retrieves the locations prior to the start of the execution of the block.
        ls = self.popVal()
        self["locs"] = ls            

    def eval(self):
        d = self.popCnt()
        if isinstance(d, Bind):
            self.__evalBind(d)
        elif d == DecKW.BIND:
            self.__evalBindKW()
        elif isinstance(d, DSeq):
            self.__evalDSeq(d)
        elif d == DecKW.DSEQ:
            self.__evalDSeqKW()
        elif isinstance(d, Ref):
            self.__evalRef(d)
        elif d == DecExpKW.REF:
            self.__evalRefKW()
        elif isinstance(d, Blk):
            self.__evalBlk(d)
        elif d == DecCmdKW.BLKDEC:
            self.__evalBlkDecKW()
        elif d == DecCmdKW.BLKCMD:
            self.__evalBlkCmdKW()
        else:
            self.pushCnt(d)
            super().eval()
 
#            
# Abstractions
#

class Formals(list):
    def __init__(self, f):
        if isinstance(f, list): 
            for a in f:
                if not isinstance(a, Id):
                    raise IllFormed(self, a)
            self.append(f)
        else:
            raise IllFormed(self, f)

class Abs(Statement):
    def __init__(self, f, b):
        if isinstance(f, list):
            if isinstance(b, Blk):
                super().__init__(f, b)
            else:
                raise IllFormed(self, b)
        else:
            raise IllFormed(self, f)

    def formals(self):
        return self.operand(0)

    def blk(self):
        return self.operand(1)

class BindAbs(Bind):
    '''
    BindAbs is a form of bind but that receives an Abs instead of an
    expression.
    '''
    def __init__(self, i, p):
        if isinstance(i, Id):
            if isinstance(p, Abs):
                Dec.__init__(self, i, p)
            else:
                raise IllFormed(self, p)
        else:
            raise IllFormed(self, i)

class Actuals(list):
    def __init__(self, a):
        if isinstance(a, list):
            for e in a:
                if not isinstance(e, Exp):
                    raise IllFormed(self, e)
            self.append(a)
        else:
            raise IllFormed(self, a)

class Call(Cmd):
    def __init__(self, f, actuals):
        if isinstance(f, Id):
            if isinstance(actuals, list):
                Cmd.__init__(self, f, actuals)
            else:
                raise IllFormed(self, actuals)
        else:
            raise IllFormed(self, f)

    def caller(self):
        return self.operand(0)

    def actuals(self):
        return self.operand(1)

class Closure(dict):
    def __init__(self, f, b, e):
        if isinstance(f, list):
            if isinstance(b, Blk):
                # I wanted to write assert(isinstance(e, Env)) but it fails.
                if isinstance(e, dict):
                    self['for'] = f             # Formal parameters
                    self['block'] = b           # Procedure block
                    self['env'] = e             # Current environment
                else:
                    raise IllFormed(self, e)
            else:
                raise IllFormed(self, b)
        else:
            raise IllFormed(self, f)

    def __str__(self):
        ret = str(self.__class__.__name__) + "("
        formals = self.formals()
        fst_formal = formals[0]     # First formal argument
        ret += str(fst_formal)
        for i in range(1, len(formals)):
            ret += ", "
            formal = formals[i]     # Remaining formal arguments
            ret += str(formal)
        ret += ", "
        ret += "Blk(...)"
        # ret += str(self.blk())      # Closure block
        ret += ")"
        return ret

    def formals(self):
        return self['for']

    def env(self):
        return self['env']

    def blk(self):
        return self['block']

class CallKW(CmdKW):
    CALL = "#CALL"
    
class AbsPiAut(DecPiAut):
    def __evalAbs(self, a):
        if not isinstance(a, Abs):  # p must be an abstraction
            raise EvaluationError(self,
                                  "Function __evalAbs called with no abstraction but with " + \
                                  str(a) + " instead.")
        else:
            f = a.formals()             # Formal parameters
            b = a.blk()                 # Body
            e = self.env()              # Current environment
            # Closes the given abs. with the current env
            c = Closure(f, b, e)
            # Closure c is pushed to the value stack such that
            self.pushVal(c)
            # a BIND may create a new binding to a given identifier.

    def match(self, f, a):
        return self.__match(f, a)
        
    def __match(self, f, a):
        '''
        Given a list of formal parameters and a list of actual parameters,
        it returns an environment relating the elements of the former with the latter.
        '''
        if isinstance(f, list) and isinstance(a, list):
                if len(f) == 0:
                    return {}
                else:
                    if len(f) == len(a):
                    # For some reason, f[0] is a tuple, not an Id.
                        f0 = f[0]
                        a0 = a[0]
                        b0 = {f0.id(): a0}
                        if len(f) == 1:
                            return b0
                        else:
                        # For some reason, f[0] is a tuple, not an Id.
                            e = b0
                            f1 = f[1]
                            a1 = a[1]
                            b1 = {f1.id(): a1}
                            e.update(b1)
                            for i in range(2, len(f)):
                                fi = f[i][0]
                                ai = a[i][0]
                                e.update({fi.id(): ai})
                            return e
                    else:
                        raise EvaluationError("Call to '__match' on " + \
                                              str(self) + ": " +
                                              "formals and actuals differ in size.")
        else:
            raise EvaluationError("Call to '__match' on " + \
                                  str(self) + " with formals " + \
                                  str(f)    + " and actuals" + str(a))

    def __evalCall(self):
        '''
        Essentially, a call is translated into a block.
        If we were progrmming pi in a symbolic language,
        we could simply crete a proper block and push it to the control stack.
        However, the environment is not symbolic: is a dictionary of objects.
        To create a block we would need to "pi-IR-fy" it, that is, recreate the
        pi IR tree from the concrete environmnet and joint it with matches created
        also at pi IR level. These would be pushed back into the control stack and
        reobjectifyed. Thus, to avoid pi-IRfication and reevaluatuation of the
        environment we manipulate it at the object level, which is dangerous but
        seems to be correct.

        This function evaluates non-recursive funcntions with single parameter expressions.
        '''
        # if not isinstance(c, Call):    # c must be a Call object
        #     raise EvaluationError("Call to __evalCall with no Call object but with " + str(c) + " instead.")
        # else:
        # Retrieves the evaluated actual parameters from the system stack.
        acs = [self.popVal()]
        # Procedure to be called
        caller = self.popVal()
        self.pushVal(self.locs())
        # Saves the current environment in the value stack.
        self.pushVal(self.env())
        # Retrieves the closure associated with the caller function.
        clos = self.getBindable(caller.id())
        # Retrieves the formal parameters from the closure.
        f = clos.formals()
        # Matches formals and actuals, creating an environment.
        d = self.__match(f, acs)
        if not d:
            raise EvaluationError("Call to __match failed with formals "+ str(f) + \
                                  " and actuals " + str(acs))
        # Retrieves the current environment.
        # e = self.env().copy()
        # Retrives the closure's environment.
        ce = clos.env()      
        # The caller's block must run on the closure's environment
        # overwritten with the matches.
        # e.update(ce)
        ce.update(d)
        self["env"] = ce
        # Pushes the keyword BLKCMD for block completion.
        self.pushCnt(DecCmdKW.BLKCMD)
        # Pushes the body of the caller function into the control stack.
        self.pushCnt(clos.blk())

    def eval(self):
        d = self.popCnt()
        if isinstance(d, Abs):
            self.__evalAbs(d)
        elif isinstance(d, Call):
            self.pushCnt(CallKW.CALL)
            for a in d.actuals():
                self.pushCnt(a)
            self.pushVal(d.caller())
        elif d == CallKW.CALL:
            self.__evalCall()
        else:
            self.pushCnt(d)
            super().eval()

#            
# Recursive abstractions
#

class BindRecAbs(BindAbs):
    pass

class RecKW(CmdKW):
    REC = "#REC"
    RECCALL = "#RECCALL"

class Rec(Closure):
    def __init__(self, f, b, e1, e2):
        super().__init__(f, b, e1)
        self['recenv'] = e2
        # if isinstance(e1, Env):
        #     if isinstance(e2, Env):
        #         self['recenv'] = e2
        #     else:
        #         raise IllFormed(e2)
        # else:
        #     raise IllFormed(e1)

    def setRecEnv(self, e):
        if isinstance(e, Env):
            self['recenv'] = e2
        else:
            raise EvaluationError(self, e)
        
    def recenv(self):
        return self['recenv']
        
def unfold(e):
    return reclose(e, e)
    # if isinstance(e, Env):
    #     return reclose(e, e)
    # else:
    #     raise EvaluationError("Can't unfold term " + str(e) + \
    #                           ". It is not an Environnment. It's type is " + str(type(e)) + ".")

def reclose(e1, e2):
    if len(e2) >= 1:
        for k, v in e2.items():
            if isinstance(v, Closure):
                e2[k] = Rec(v.formals(), v.blk(), v.env(), e1)
                del v
            elif isinstance(v, Rec):
                e2[k] = v.setRecEnv(e1)
    return e2

    # if isinstance(e2, Env):
    #     if len(e2) >= 1:
    #         for k, v in e2.items():
    #             if isinstance(v, Closure):
    #                 e2[k] = Rec(v.formals(), v.blk(), v.env(), e1)
    #                 del v
    #             elif isinstance(v, Rec):
    #                 e2[k] = v.setRecEnv(e1)
    #     return e2
    # else:
    #     raise EvaluationError(e2)

class RecPiAut(AbsPiAut):
    def __evalRec(self, b):
        v = self.popVal()
        self.pushVal(unfold(v))

    def __evalRecCall(self):
        '''
        Essentially, a call is translated into a block.
        If we were progrmming pi in a symbolic language,
        we could simply crete a proper block and push it to the control stack.
        However, the environment is not symbolic: is a dictionary of objects.
        To create a block we would need to "pi-IR-fy" it, that is, recreate the
        pi IR tree from the concrete environmnet and joint it with matches created
        also at pi IR level. These would be pushed back into the control stack and
        reobjectifyed. Thus, to avoid pi-IRfication and reevaluatuation of the
        environment we manipulate it at the object level, which is dangerous but
        seems to be correct.

        There is only support for one-parameter expressions in actuals.
        '''
        #if not isinstance(c, Call):    # c must be a Call object
        #    raise EvaluationError("Call to __evalCall with no Call object but with " + \
        #                          str(c) + " instead.")
        # Retrieves the evaluated actual parameters from the system stack.
        acs = [self.popVal()]
        # Procedure to be called
        caller = self.popVal()
        # Retrieves the closure associated with the caller function.
        reclos = self.getBindable(caller.id())
        if not isinstance(reclos, Rec):
            raise EvaluationError("No recursive closure bound to " + \
                                  str(caller.id()) + " in call to recursive procedure.")
        # Retrieves the formal parameters from the closure.
        f = reclos.formals()
        # Matches formals and actuals, creating an environment.
        # d = self.__match(f, acs)
        d = self.match(f, acs)
        if not d:
            raise EvaluationError("Call to __match failed with formals "+ str(f) + \
                                  " and actuals " + str(acs))
        # Retrieves the current environment.
        # e = self.env()
        # Retrives the recursive closure's environment.
        rce = reclos.env()      
        # Retrives the recursive closure's recursive environment.
        rcre = reclos.recenv()      
        # The caller's block must run on the current environment
        # overwritten with the recursive (unfolded) environments and matches.
        # Is it the current env. or the reclosure's?
        # ep = rce.update(unfold(rcre)).update(d)
        # ep = e.update(rce).update(unfold(rcre)).update(d)
        # e.update(rce)
        rce.update(unfold(rcre))
        rce.update(d)
        self["env"] = rce
        self.pushVal(self.locs())
        # Saves the current environment in the value stack.
        self.pushVal(rce)
        # Pushes the keyword BLKCMD for block completion.
        self.pushCnt(DecCmdKW.BLKCMD)
        # Pushes the body of the caller function into the control stack.
        self.pushCnt(reclos.blk())

    def __evalRecKW(self):
        b = self.popVal()
        self.pushVal(unfold(b))
        
    def eval(self):
        c = self.popCnt()
        if isinstance(c, BindRecAbs):
            self.pushCnt(RecKW.REC)
            self.pushCnt(BindAbs(c.id(), c.bindable()))
        elif c == RecKW.REC:
            self.__evalRecKW()
        elif isinstance(c, Call):
            caller = c.caller()
            env = self.env()
            if caller.id() in env.keys():
                # If this is a call to a non-recursive function,
                # the caller must be in the environment and
                # bound to a closure.
                if type(env[caller.id()]) == Closure:
                    self.pushCnt(c)
                    AbsPiAut.eval(self)
                    return
                elif type(env[caller.id()]) == Rec:
                    self.pushCnt(RecKW.RECCALL)
                    for a in c.actuals():
                        self.pushCnt(a)
                        self.pushVal(c.caller())
                else:
                    raise EvaluationError("Call to " + str(caller) + " with no (rec)closure.")
            else:
                raise EvaluationError("Call to " + str(caller) + " not in env.")
        elif c == RecKW.RECCALL:
            self.__evalRecCall()
        else:
            self.pushCnt(c)
            super().eval()

import datetime

def run(ast, color=True):
    global COLORED
    COLORED = color
    aut = RecPiAut()
    aut.pushCnt(ast)
    step = 0
    t0 = datetime.datetime.now()
    trace = []
    while not aut.emptyCnt():
        try:
            aut.eval()
        except EvaluationError as e:
            e.trace = trace
            raise e
        trace.append(str(aut))
        step = step + 1
    t1 = datetime.datetime.now()
    out = aut.out()
    return (trace, step, out, (t1 - t0))

# if __name__ == '__main__':
#     # The classic iterative factorial example within a function.
#     bl1 = Blk(Bind(Id("y"), Ref(Num(1))),
#             CSeq(Assign(Id("y"), Id("x")),
#                 Loop(Not(Eq(Id("y"), Num(0))),
#                     CSeq(Assign(Id("z"), Mul(Id("z"), Id("y"))),
#                         Assign(Id("y"), Sub(Id("y"), Num(1)))))))

#     abs = Abs(Formals(Id("x")), bl1)
#     ba = BindAbs(Id("fac"), abs)
#     ast = Blk(Bind(Id("z"), Ref(Num(1))), Blk(ba, Call(Id("fac"), Actuals(Num(1500)))))

#     try:
#         (tr, ns, dt) = run(ast)
#     except Exception as e:
#         print('Evaluation error: ', e)
#         exit()

#     print('Last state of the π automaton:')
#     print(tr[len(tr) - 2])
#     print('Number of evaluation steps:', ns)
#     print('Evaluation time:', dt)
