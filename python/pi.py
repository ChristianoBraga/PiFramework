# <htmlcell>
# <!-- pi.py with Jupyter Notebook markups. Run py2nb.py to generate a pi notebook. -->

from nbformat import v3, v4

with open("pi.py") as fpin:
    text = fpin.read()

nbook = v3.reads_py(text)
nbook = v4.upgrade(nbook)  # Upgrade v3 to v4

jsonform = v4.writes(nbook) + "\n"
with open("pi.ipynb", "w") as fpout:
    fpout.write(jsonform)


### pi.py com markups para notebook

# coding: utf-8

# <markdowncell>
# # π$^2$: π Framework in Python
#
# __Christiano Braga__
# __Universidade Federal Fluminense__
#
# http://www.ic.uff.br/~cbraga
#
# The π Framework is a simple framework for teaching compiler
# construction. It defines a set of common programming languages
# primitives (π lib, inspired by `funcons` from the [Componenent Based
# Framework](https://plancomps.github.io/CBS-beta), by Peter D. Mosses)
# and their formal semantics (π Automata). In this notebook π is
# implemented in Python.

# <markdowncell>
# # π lib Statements

# <codecell>


class IllFormed(Exception):
    def __str__(self):
        return "π lib exception - ill formed AST: " + str(self.args)


class Statement:
    def __init__(self, *args):
        self._opr = args

    def __str__(self):
        ret = str(self.__class__.__name__) + "("
        if len(self._opr) > 0:
            ret += str(self._opr[0])
            if len(self._opr) > 1:
                for i in range(1, len(self._opr)):
                    ret += ", "
                    ret += str(self._opr[i])
        ret += ")"
        return ret

    def arity(self):
        return len(self._opr)

    def operand(self, n):
        if self.arity() > 0:
            return self._opr[n]
        else:
            raise IllFormed("Call to 'operand' on " +
                        str(self) + ": " + "No operands.")

    def operator(self):
        return str(self.__class__.__name__)

# <markdowncell>
# # π automaton

# <codecell>


class ValueStack(list):
    pass


class ControlStack(list):
    pass


class EvaluationError(Exception):
    def __str__(self):
        return "π automaton error: " + str(self.args)

class PiAutomaton(dict):

    def __init__(self):
        self["val"] = ValueStack()
        self["cnt"] = ControlStack()

    def __str__(self):
        ret = ""
        for k, v in self.items():
            ret = ret + str(k) + " : " + str(v) + "\n"
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
            raise IllFormed(
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

# <markdowncell>
# # π lib Expressions

# <codecell>


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

# <markdowncell>
# # π automaton for π lib Expressions

# <codecell>


class ExpKW:
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
        if v2 == 0:
            raise EvaluationError(self, "Division by zero.")
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
            raise EvaluationError(
                "Call to 'eval' on " + str(self) + ": " + "Ill formed expression " + str(e))

# <markdowncell>
# # π lib Commands

# <codecell>


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

# <codecell>
# # π automaton for π lib Commands


class Env(dict):
    pass


class Loc(int):
    pass


class Sto(dict):
    pass


class CmdKW:
    ASSIGN = "#ASSIGN"
    LOOP = "#LOOP"


class CmdPiAut(ExpPiAut):


    def __init__(self):
        self["env"] = Env()
        self["sto"] = Sto()
        ExpPiAut.__init__(self)


    def env(self):
        return self["env"]


    def getBindable(self, i):
        en = self.env()
        if i in en.keys():
            return en[i]
        else:
            raise EvaluationError(self, "Identifier ", i, "not in environment.")


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
        if st[l]:
            st[l] = v
        else:
            raise EvaluationError(self, "Call to updateStore woth location", l, "not in store.")

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
        if isinstance(c, Assign):
            self.__evalAssign(c)
        elif c == CmdKW.ASSIGN:
            self.__evalAssignKW()
        elif isinstance(c, Nop):
            return
        elif isinstance(c, Id):
            self.__evalId(c.id())
        elif isinstance(c, Loop):
            self.__evalLoop(c)
        elif c == CmdKW.LOOP:
            self.__evalLoopKW()
        elif isinstance(c, CSeq):
            self.__evalCSeq(c)
        else:
            self.pushCnt(c)
            ExpPiAut.eval(self)

# <markdowncell>
# # π lib Declarations
# ## Grammar for π lib Declarations
#
# $
# \begin{array}{rcl}
# Statement & ::= & Dec \\
# Exp       & ::= & \mathtt{Ref}(Exp) \mid \mathtt{Cns}(Exp) \\
# Cmd       & ::= & \mathtt{Blk}(Dec, Cmd) \\
# Dec       & ::= & \mathtt{Bind}(Id, Exp) \mid \mathtt{DSeq}(Dec, Dec)
# \end{array}
# $

# <codecell>


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
                raise IllFormed(self, c)
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

# <markdowncell>
# # π Automaton for π lib Declarations

# <codecell>

class DecExpKW(ExpKW):
    REF = "#REF"
    CNS = "#CNS"

class DecCmdKW(CmdKW):
    BLKDEC = "#BLKDEC"
    BLKCMD = "#BLKCMD"

class DecKW:
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
        self.pushVal({x: l})

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
        # Retrieves the locations prior to the block evaluation.
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
            CmdPiAut.eval(self)

# <markdowncell>
# # π lib Abstractions

# To give semantics to functions with _static bindings_, we use the concept of _closures_ which essentially create a "proto" enviroment for the evaluation of given expressions.

# <codecell>

class Formals(list):
    def __init__(self, f):
        if isinstance(f, list): 
            for a in f:
                if not isinstance(a, Id):
                    raise IllFormed(self, a)
            self.append(f)
        else:
            raise IllFormed(self, f)

class Abs:
    def __init__(self, f, b):
        if isinstance(f, list):
            if isinstance(b, Blk):
                self._opr = [f, b]
            else:
                raise IllFormed(self, b)
        else:
            raise IllFormed(self, f)

    def formals(self):
        return self._opr[0]

    def blk(self):
        return self._opr[1]

    def __str__(self):
        ret = str(self.__class__.__name__) + "("
        formals = self.formals()
        ret += str(formals[0])              # First formal argument
        for i in range(1, len(formals)):
            ret += ", "
            ret += str(formals[i])          # Remaining formal arguments
        ret += ", "
        ret += str(self.blk())              # Abstraction block
        ret += ")"
        return ret

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

# <markdowncell>
# # π Automaton for π lib Abstractions

# <codecell>
class Closure(dict):
    def __init__(self, f, b, e):
        if isinstance(f, list):
            if isinstance(b, Blk):
                # I wanted to write assert(isinstance(e, Env)) but it fails.
                if isinstance(e, dict):
                    self["for"] = f             # Formal parameters
                    self["env"] = e             # Current environment
                    self["block"] = b           # Procedure block
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
        ret += str(self.blk())      # Closure block
        ret += ")"
        return ret

    def formals(self):
        return self['for']

    def env(self):
        return self['env']

    def blk(self):
        return self['block']

class AbsPiAut(DecPiAut):
    def __evalAbs(self, a):
        if not isinstance(a, Abs):  # p must be an abstraction
            raise EvaluationError(self, "Function __evalAbs called with no abstraction but with ", a, " instead.")
        else:
            f = a.formals()             # Formal parameters
            b = a.blk()                 # Body
            e = self.env()              # Current environment
            # Closes the given abs. with the current env
            c = Closure(f, b, e)
            # Closure c is pushed to the value stack such that
            self.pushVal(c)
            # a BIND may create a new binding to a given identifier.

    def __match(self, f, a):
        '''
        Given a list of formal parameters and a list of actual parameters,
        it returns an environment relating the elements of the former with the latter.
        '''
        if isinstance(f, list):
            if isinstance(a, list):
                if len(f) == 0:
                    return {}
                if len(f) == len(a) and len(f) > 0:
                # For some reason, f[0] is a tuple, not an Id.
                    f0 = f[0]
                    a0 = a[0]
                    b0 = {f0.id(): a0.num()}
                if len(f) == 1:
                    return b0
                else:
                    # For some reason, f[0] is a tuple, not an Id.
                    f1 = f[1]
                    a1 = a[1]
                    b1 = {f1.id(): a1.num()}
                    e = b0.update(b1)
                    for i in range(2, len(f)):
                        fi = f[i][0]
                        ai = a[i][0]
                        e.update({fi.id(): ai.num()})
                    return e
            else:
                raise EvaluationError("Call to '__match' on " + str(self) + ": " + "formals and actuals differ in size.")
        else:
            raise EvaluationError("Call to '__match' on " + str(self) + ": " + " no formals, but with ", f, " instead.")

    def __evalCall(self, c):
        '''
        Essentially, a call is translated into a block.
        If we were progrmming pi in a symbolic language,
        we could simply crete a proper block and push it to the control stack.
        However, the environment is not symbolic: is a dictionary of objects.
        To create a block we would need to "pi-lib-fy" it, that is, recreate the
        pi lib tree from the concrete environmnet and joint it with matches created
        also at pi lib level. These would be pushed back into the control stack and
        reobjectifyed. Thus, to avoid pi-libfication and reevaluatuation of the
        environment we manipulate it at the object level, which is dangerous but
        seems to be correct.
        '''
        if not isinstance(c, Call):    # c must be a Call object
            raise EvaluationError("Call to __evalCall with no Call object but with ", c, " instead.")
        else:
            # Procedure to be called
            caller = c.caller()            
            # Retrieves the current environment.
            e = self.env()                 
            # Retrieves the closure associated with the caller function.
            clos = e[caller.id()]
            # Retrieves the actual parameters from the call.
            a = c.actuals()
            # Retrieves the formal parameters from the closure.
            f = clos.formals()
            # Matches formals and actuals, creating an environment.
            d = self.__match(f, a)
            # Retrives the closure's environment.
            ce = clos.env()      
            # The caller's block must run on the closures environment
            # overwritten with the matches.
            d.update(ce)
            self["env"] = d
            self.pushVal(self.locs())
            # Saves the current environment in the value stack.
            self.pushVal(e)
            # Pushes the keyword BLKCMD for block completion.
            self.pushCnt(DecCmdKW.BLKCMD)
            # Pushes the body of the caller function into the control stack.
            self.pushCnt(clos.blk())

    def eval(self):
        d = self.popCnt()
        if isinstance(d, Abs):
            self.__evalAbs(d)
        elif isinstance(d, Call):
            self.__evalCall(d)
        else:
            self.pushCnt(d)
            DecPiAut.eval(self)

import datetime

def run(ast):
    aut = AbsPiAut()
    aut.pushCnt(ast)
    step = 0
    t0 = datetime.datetime.now()
    trace = []
    while not aut.emptyCnt():
        aut.eval()
        trace.append(str(aut))
        step = step + 1
    t1 = datetime.datetime.now()
    return (trace, step, (t1 - t0))

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
