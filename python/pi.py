### Conversor de python para nb

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
# primitives (π Lib, inspired by `funcons` from the [Componenent Based
# Framework](https://plancomps.github.io/CBS-beta), by Peter D. Mosses)
# and their formal semantics (π Automata). In this notebook π is
# formally described. The syntax of π Lib is given as a BNF description.
# The π Automata for the dynamic semantics of π Lib is described in
# Maude syntax. We implement the π Framework in Python to start
# exploring notebook features together with different libraries
# available for the Python language such as ``llvm`` and ``SMV``
# bindings.

# <markdowncell>
## π Lib Expressions
# ### Grammar for π Lib Expressions
# $\begin{array}{rcl}
# Statement & ::= & Exp \\
# Exp       & ::= & ArithExp \mid BoolExp \\
# ArithExp  & ::= & \mathtt{Sum}(Exp, Exp)\mid \mathtt{Sub}(Exp, Exp)
# \mid \mathtt{Mul}(Exp, Exp) \\
# BoolExp  & ::= & \mathtt{Eq}(Exp, Exp) \mid \mathtt{Not}(Exp)
# \end{array}$

# <markdowncell>
# ### π Lib Expressions in Python
#
# We encode BNF rules as classes in Python. Every non-terminal gives
# rise to a class. The reduction relation $::=$ is encoded as
# inheritance. Operands are encoded as cells in a list object attribute,
# whose types are enforced by `assert` predicates on `isinstace` calls.
# The operand list `opr` is declared in the `Statement` class, whose
# constructor initializes the `opr` attribute with as many parameters as
# the subclass constructor might have.

# <codecell>
# π Lib
## Statement
class Statement:
    def __init__(self, *args):
        self.opr = args

    def __str__(self):
        ret = str(self.__class__.__name__) + "("
        for o in self.opr:
            ret += str(o)
        ret += ")"
        return ret


## Expressions
class Exp(Statement): pass


class ArithExp(Exp): pass


class Num(ArithExp):
    def __init__(self, f):
        assert (isinstance(f, int))
        ArithExp.__init__(self, f)


class Sum(ArithExp):
    def __init__(self, e1, e2):
        assert (isinstance(e1, Exp) and isinstance(e2, Exp))
        ArithExp.__init__(self, e1, e2)


class Sub(ArithExp):
    def __init__(self, e1, e2):
        assert (isinstance(e1, Exp) and isinstance(e2, Exp))
        ArithExp.__init__(self, e1, e2)


class Mul(ArithExp):
    def __init__(self, e1, e2):
        assert (isinstance(e1, Exp) and isinstance(e2, Exp))
        ArithExp.__init__(self, e1, e2)


class BoolExp(Exp): pass


class Eq(BoolExp):
    def __init__(self, e1, e2):
        assert (isinstance(e1, Exp) and isinstance(e2, Exp))
        BoolExp.__init__(self, e1, e2)


class Not(BoolExp):
    def __init__(self, e):
        assert (isinstance(e, Exp))
        BoolExp.__init__(self, e)


# In[15]:


exp = Sum(Num(1), Mul(Num(2), Num(4)))
print(exp)


# <markdowncell>
# However, if we create an ill-formed tree, an exception is raised.
#
# ```python
# exp2 = Mul(2, 1)
#
# ---------------------------------------------------------------------------
# AssertionError                            Traceback (most recent call last)
# <ipython-input-3-de6e358a117c> in <module>()
# ----> 1 exp2 = Mul(2.0, 1.0)
#
# <ipython-input-1-09d2d91ef407> in __init__(self, e1, e2)
#      28 class Mul(ArithExp):
#      29     def __init__(self, e1, e2):
# ---> 30         assert(isinstance(e1, Exp) and isinstance(e2, Exp))
#      31         super().__init__(e1, e2)
#      32 class BoolExp(Exp): pass
#
# AssertionError:
# ```

# <markdowncell>
# ### π Automaton for π Lib Expressions

# The π automaton for π Lib Expressions is implemented in the
# `ExpPiAut` class. Instances of `ExpPiAut` are dictionaries, that come
# initialized with two entries: one for the value stack, at index `val`,
# and antother for the control stack, indexed `cnt`.
# ```python
# class ExpPiAut(dict):
#     def __init__(self):
#         self["val"] = ValueStack()
#         self["cnt"] = ControlStack()
# # ...
# ```

# Class `ExpπAut` encapsulates the encoding for π Lib Expression rules
# as private methods that are called by the public (polymorphic) `eval`
# method. In the following code snippet it calls the function that
# evaluates a `Sum` expression.
# ```python
# def eval(self):
#     e = self.popCnt()
#     if isinstance(e, Sum):
#         self.__evalSum(e)
# # ...
# ```

# We use Maude syntax to specify π Automaton rules. This is the π rule
# for the evaluation of (floating point) numbers, described as an
# equation in Maude. It specifies that whenever a number is in the top
# of the control stack `C` is should be popped from `C` and pushed into
# the value stack `SK`.

# ```maude
# eq [num-exp] :
#    < cnt : (num(f:Float) C:ControlStack), val : SK:ValueStack, ... >
#  =
#    < cnt : C:ControlStack,
#      val : (val(f:Float) SK:ValueStack), ... > .```

# π rule `num-exp` is encoded in function `__evalNum(self, n)`. It
# receives a `Num` object in `n` whose sole attribute has the floating
# point number that `n` denotes. Method `pushVal(.)` pushes the given
# argument into the value stack.
# # ```python
# def __evalNum(self, n):
#     f = n.opr[0]
#     self.pushVal(f)
# ```

# <markdowncell>
# ### The complete π Automaton for π Lib Expressions in Python

# <codecell>
## Expressions
class ValueStack(list): pass


class ControlStack(list): pass


class ExpKW:
    SUM = "#SUM"
    SUB = "#SUB"
    MUL = "#MUL"
    EQ = "#EQ"
    NOT = "#NOT"


class ExpPiAut(dict):
    def __init__(self):
        self["val"] = ValueStack()
        self["cnt"] = ControlStack()

    def val(self):
        return self["val"]

    def cnt(self):
        return self["cnt"]

    def pushVal(self, v):
        vs = self.val()
        vs.append(v)

    def popVal(self):
        vs = self.val()
        v = vs[len(vs) - 1]
        vs.pop()
        return v

    def pushCnt(self, e):
        cnt = self.cnt()
        cnt.append(e)

    def popCnt(self):
        cs = self.cnt()
        c = cs[len(cs) - 1]
        cs.pop()
        return c

    def emptyCnt(self):
        return len(self.cnt()) == 0

    def __evalSum(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.SUM)
        self.pushCnt(e1)
        self.pushCnt(e2)

    def __evalSumKW(self, e):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 + v2)

    def __evalMul(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.MUL)
        self.pushCnt(e1)
        self.pushCnt(e2)

    def __evalMulKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 * v2)

    def __evalSub(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.SUB)
        self.pushCnt(e1)
        self.pushCnt(e2)

    def __evalSubKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 - v2)

    def __evalNum(self, n):
        f = n.opr[0]
        self.pushVal(f)

    def __evalEq(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.EQ)
        self.pushCnt(e1)
        self.pushCnt(e2)

    def __evalEqKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1 == v2)

    def __evalNot(self, e):
        e = e.opr[0]
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
        elif isinstance(e, Num):
            self.__evalNum(e)
        elif isinstance(e, Eq):
            self.__evalEq(e)
        elif e == ExpKW.EQ:
            self.__evalEqKW()
        elif isinstance(e, Not):
            self.__evalNot(e)
        elif e == ExpKW.NOT:
            self.__evalNotKW()
        else:
            raise Exception("Ill formed: ", e)


# <codecell>

ea = ExpPiAut()
print(exp)
ea.pushCnt(exp)
while not ea.emptyCnt():
    ea.eval()
    print(ea)


# <markdowncell>
# ## π Lib Commands
#
# ### Grammar for π Lib Commands
#
# $\begin{array}{rcl}
# Statement & ::= & Cmd \\
# Exp       & ::= & \mathtt{Id}(String) \\
# Cmd       & ::= & \mathtt{Assign}(Id, Exp) \mid
# \mathtt{Loop}(BoolExp, Cmd) \mid \mathtt{CSeq}(Cmd, Cmd)
# \end{array}$
#
# Commands are language constructions that require both an
# environement and a memory store to be evaluated.
# From a syntactic standpoint, they extend statements and expressions,
# as an identifier is an expression.

# <markdowncell>
# ### Grammar for π Lib Commands in Python
#
# The enconding of the grammar for commands follows the same mapping
# of BNF rules as classes we used for expressions.

# <codecell>

## Commands
class Cmd(Statement): pass


class Id(Exp):
    def __init__(self, s):
        assert (isinstance(s, str))
        Exp.__init__(self, s)


class Assign(Cmd):
    def __init__(self, i, e):
        assert (isinstance(i, Id) and isinstance(e, Exp))
        Cmd.__init__(self, i, e)


class Loop(Cmd):
    def __init__(self, be, c):
        assert (isinstance(be, BoolExp) and isinstance(c, Cmd))
        Cmd.__init__(self, be, c)


class CSeq(Cmd):
    def __init__(self, c1, c2):
        # assert (isinstance(c1, Cmd) and isinstance(c2, Cmd))
        Cmd.__init__(self, c1, c2)


# <codecell>
cmd = Assign(Id("x"), Num(1))
print(type(cmd))
print(cmd)


# <markdowncell>
# ### Complete π Automaton for Commands in Python

# <codecell>
## Commands
class Env(dict): pass


class Loc(int): pass


class Sto(dict): pass


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

    def getLoc(self, i):
        en = self.env()
        return en[i]

    def sto(self):
        return self["sto"]

    def updateStore(self, l, v):
        st = self.sto()
        st[l] = v

    def __evalAssign(self, c):
        i = c.opr[0]
        e = c.opr[1]
        self.pushVal(i.opr[0])
        self.pushCnt(CmdKW.ASSIGN)
        self.pushCnt(e)

    def __evalAssignKW(self):
        v = self.popVal()
        i = self.popVal()
        l = self.getLoc(i)
        self.updateStore(l, v)

    def __evalId(self, i):
        s = self.sto()
        l = self.getLoc(i)
        self.pushVal(s[l])

    def __evalLoop(self, c):
        be = c.opr[0]
        bl = c.opr[1]
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
        c1 = c.opr[0]
        c2 = c.opr[1]
        self.pushCnt(c2)
        self.pushCnt(c1)

    def eval(self):
        c = self.popCnt()
        if isinstance(c, Assign):
            self.__evalAssign(c)
        elif c == CmdKW.ASSIGN:
            self.__evalAssignKW()
        elif isinstance(c, Id):
            self.__evalId(c.opr[0])
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
# ## π Lib Declarations
# ### Grammar for π Lib Declarations
#
# $
# \begin{array}{rcl}
# Statement & ::= & Dec \\
# Exp       & ::= & \mathtt{Ref}(Exp) \mid \mathtt{Cns}(Exp) \\
# Cmd       & ::= & \mathtt{Blk}(Dec, Cmd) \\
# Dec       & ::= & \mathtt{Bind}(Id, Exp) \mid \mathtt{DSeq}(Dec, Dec)
# \end{array}
# $

# <markdowncell>
# ### Grammar for π Lib Declarations in Python

# <codecell>
## Declarations
class Dec(Statement): pass


class Bind(Dec):
    def __init__(self, i, e):
        assert (isinstance(i, Id) and isinstance(e, Exp))
        Dec.__init__(self, i, e)


class Ref(Exp):
    def __init__(self, e):
        assert (isinstance(e, Exp))
        Exp.__init__(self, e)


class Cns(Exp):
    def __init__(self, e):
        assert (isinstance(e, Exp))
        Exp.__init__(self, e)


class Blk(Cmd):
    def __init__(self, d, c):
        assert (isinstance(d, Dec) and isinstance(c, Cmd))
        Cmd.__init__(self, d, c)


class DSeq(Dec):
    def __init__(self, d1, d2):
        assert (isinstance(d1, Dec) and isinstance(d2, Dec))
        Dec.__init__(self, d1, d2)


# <markdowncell>
# ### Complete π Automaton for π Lib Declarations in Python

# <codecell>
## Declarations
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
        ex = e.opr[0]
        self.pushCnt(DecExpKW.REF)
        self.pushCnt(ex)

    def __newLoc(self):
        sto = self.sto()
        if sto:
            return max(list(sto.keys())) + 1
        else:
            return 0.0

    def __evalRefKW(self):
        v = self.popVal()
        l = self.__newLoc()
        self.updateStore(l, v)
        self.pushLoc(l)
        self.pushVal(l)

    def __evalBind(self, d):
        i = d.opr[0]
        e = d.opr[1]
        self.pushVal(i)
        self.pushCnt(DecKW.BIND)
        self.pushCnt(e)

    def __evalBindKW(self):
        l = self.popVal()
        i = self.popVal()
        x = i.opr[0]
        self.pushVal({x: l})

    def __evalDSeq(self, ds):
        d1 = ds.opr[0]
        d2 = ds.opr[1]
        self.pushCnt(DecKW.DSEQ)
        self.pushCnt(d2)
        self.pushCnt(d1)

    def __evalDSeqKW(self):
        d2 = self.popVal()
        d1 = self.popVal()
        d1.update(d2)
        self.pushVal(d1)

    def __evalBlk(self, d):
        ld = d.opr[0]
        c = d.opr[1]
        l = self.locs()
        self.pushVal(list(l))
        self.pushVal(c)
        self.pushCnt(DecCmdKW.BLKDEC)
        self.pushCnt(ld)

    def __evalBlkDecKW(self):
        d = self.popVal()
        c = self.popVal()
        l = self.locs()
        self.pushVal(l)
        en = self.env()
        ne = en.copy()
        ne.update(d)
        self.pushVal(en)
        self["env"] = ne
        self.pushCnt(DecCmdKW.BLKCMD)
        self.pushCnt(c)

    def __evalBlkCmdKW(self):
        en = self.popVal()
        ls = self.popVal()
        self["env"] = en
        s = self.sto()
        s = {k: v for k, v in s.items() if k not in ls}
        self["sto"] = s
        # del ls
        ols = self.popVal()
        self["locs"] = ols

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
# ### Factorial example

# <codecell>
dc = DecPiAut()
fac = Loop(Not(Eq(Id("y"), Num(0))),
           CSeq(Assign(Id("x"), Mul(Id("x"), Id("y"))),
                Assign(Id("y"), Sub(Id("y"), Num(1)))))
dec = DSeq(Bind(Id("x"), Ref(Num(1))),
           Bind(Id("y"), Ref(Num(200))))
fac_blk = Blk(dec, fac)
dc.pushCnt(fac_blk)
while not dc.emptyCnt():
    aux = dc.copy()
    dc.eval()
    if dc.emptyCnt():
        print(aux)

# <codecell>
## LLVM Lite

import llvmlite.ir as ir
import llvmlite.binding as llvm


class LLVMTypes:
    INT = ir.IntType(64)
    BOOL = ir.IntType(1)
    VOID = ir.VoidType()


class LLVMConstants:
    TRUE = ir.Constant(LLVMTypes.BOOL, 1)
    FALSE = ir.Constant(LLVMTypes.BOOL, 0)


class LLVMExp():
    def __init__(self, function):
        self.function = function
        self.block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)

    def compile(self, node):
        if isinstance(node, Num):
            return self.compileNum(node)
        elif isinstance(node, Sum):
            return self.compileSum(node)
        elif isinstance(node, Sub):
            return self.compileSub(node)
        elif isinstance(node, Mul):
            return self.compileMul(node)
        elif isinstance(node, Eq):
            return self.compileEq(node)
        elif isinstance(node, Not):
            return self.compileNot(node)

    def compileNum(self, node):
        return ir.Constant(LLVMTypes.INT, node.opr[0])

    def compileSum(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        res = self.builder.add(lhs, rhs, "tmp_sum")
        return res

    def compileSub(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        res = self.builder.sub(lhs, rhs, "tmp_sub")
        return res

    def compileMul(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        res = self.builder.mul(lhs, rhs, "tmp_mul")
        return res

    def compileEq(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        res = self.builder.icmp_signed("==", lhs, rhs, "temp_eq")
        return res

    def compileNot(self, node):
        lhs = self.compile(node.opr[0])
        res = self.builder.neg(lhs, "temp_not")
        return res


class LLVMCmd(LLVMExp):
    def __init__(self, function):
        self.env = {}
        LLVMExp.__init__(self, function)

    def addEnv(self, id, pointer):
        self.env.update({id: pointer})

    def compileAssign(self, node):
        id = self.compileAssingId(node.opr[0])
        val = self.compile(node.opr[1])
        return self.builder.store(val, id)

    def compileAssingId(self, node):
        id = node.opr[0]
        if id in self.env:
            ptr = self.env[id]
        else:
            ptr = self.builder.alloca(LLVMTypes.INT, None, "ptr")
            self.addEnv(id, ptr)
        return ptr

    def compileId(self, node):
        id = node.opr[0]
        ptr = self.env[id]
        return self.builder.load(ptr, "val")

    def compileCSeq(self, node):
        self.compile(node.opr[0])
        self.compile(node.opr[1])

    def compileLoop(self, node):
        loop = self.builder.append_basic_block("loop")

    def compile(self, node):
        if isinstance(node, Assign):
            return self.compileAssign(node)
        elif isinstance(node, Id):
            return self.compileId(node)
        elif isinstance(node, CSeq):
            return self.compileCSeq(node)
        else:
            return LLVMExp.compile(self, node)


# <codecell>
module = ir.Module('main_module')
func_type = ir.FunctionType(LLVMTypes.INT, [], False)
func = ir.Function(module, func_type, "main_function")

llvm_exp = LLVMCmd(func)

res = llvm_exp.compile(CSeq(Assign(Id("x"), Num(1)), Assign(Id("x"), Num(7))))
# res = llvm_exp.compile(Not(Eq(Num(1), Num(0))))
print(res)
llvm_exp.builder.ret(llvm_exp.compile(Sum(Id("x"), Num(1))))
print(module)

# <codecell>
from ctypes import CFUNCTYPE, c_void_p

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one


def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


engine = create_execution_engine()
mod = compile_ir(engine, str(module))

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("main_function")

# Run the function via ctypes
cfunc = CFUNCTYPE(c_void_p)(func_ptr)
res = cfunc()
print("main_function() =", res)
