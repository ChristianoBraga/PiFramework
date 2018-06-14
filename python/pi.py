# π Lib

## Statement
class Statement: 
    def __init__(self, *args):
        self.opr = args

## Expressions
class Exp(Statement): pass
class ArithExp(Exp): pass
class Num(ArithExp): 
    def __init__(self, f): 
        assert(isinstance(f, float))
        super().__init__(f)
class Sum(ArithExp): 
    def __init__(self, e1, e2): 
        assert(isinstance(e1, Exp) and isinstance(e2, Exp) and 
        (not isinstance(e1, BoolExp)) and 
        (not isinstance(e2, BoolExp)))
        super().__init__(e1, e2)
class Sub(ArithExp): 
    def __init__(self, e1, e2): 
        assert(isinstance(e1, Exp) and isinstance(e2, Exp) and 
        (not isinstance(e1, BoolExp)) and 
        (not isinstance(e2, BoolExp)))
        super().__init__(e1, e2)
class Mul(ArithExp): 
    def __init__(self, e1, e2): 
        assert(isinstance(e1, Exp) and isinstance(e2, Exp) and 
        (not isinstance(e1, BoolExp)) and 
        (not isinstance(e2, BoolExp)))
        super().__init__(e1, e2)
class BoolExp(Exp): pass
class Eq(BoolExp):
    def __init__(self, e1, e2):
        assert(isinstance(e1, Exp) and isinstance(e2, Exp))
        super().__init__(e1, e2)
class Not(BoolExp):
    def __init__(self, e):
        assert(isinstance(e, Exp))
        super().__init__(e)

## Commands
class Cmd(Statement): pass
class Id(Exp):
    def __init__(self, s):
        assert(isinstance(s, str))
        super().__init__(s)
class Assign(Cmd):
    def __init__(self, i, e): 
        assert(isinstance(i, Id) and isinstance(e, Exp))
        super().__init__(i, e)
class Loop(Cmd):
    def __init__(self, be, c):
        assert(isinstance(be, BoolExp) and isinstance(c, Cmd))
        super().__init__(be, c)
class CSeq(Cmd):
    def __init__(self, c1, c2):
        assert(isinstance(c1, Cmd) and isinstance(c2, Cmd))
        super().__init__(c1, c2)

## Declarations
class Dec(Statement): pass
class Bind(Dec):
    def __init__(self, i, e):
        assert(isinstance(i, Id) and isinstance(e, Exp))
        super().__init__(i, e)
class Ref(Exp):
    def __init__(self, e):
        assert(isinstance(e, Exp))
        super().__init__(e)
class Cns(Exp):
    def __init__(self, e):
        assert(isinstance(e, Exp))
        super().__init__(e)
class Blk(Cmd):
    def __init__(self, d, c):
        assert(isinstance(d, Dec) and isinstance(c, Cmd))
        super().__init__(d, c)
class DSeq(Dec):
    def __init__(self, d1, d2):
        assert(isinstance(d1, Dec) and isinstance(d2, Dec))
        super().__init__(d1, d2)

# π Automaton

## Expressions
class ValueStack(list): pass
class ControlStack(list): pass
class ExpKW:
    SUM = "#SUM"
    SUB = "#SUB"
    MUL = "#MUL"
    EQ = "#EQ"
    NOT = "#NOT"
class ExpConf(dict):
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
        self.pushVal(v1+v2)
    def __evalMul(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.MUL)
        self.pushCnt(e1)
        self.pushCnt(e2)
    def __evalMulKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1*v2)
    def __evalSub(self, e):
        e1 = e.opr[0]
        e2 = e.opr[1]
        self.pushCnt(ExpKW.SUB)
        self.pushCnt(e1)
        self.pushCnt(e2)
    def __evalSubKW(self):
        v1 = self.popVal()
        v2 = self.popVal()
        self.pushVal(v1-v2)
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
            raise Exception("Ill formed:", e)

## Commands
class Env(dict): pass
class Loc(float): pass
class Sto(dict): pass
class CmdKW:
    ASSIGN = "#ASSIGN"
    LOOP = "#LOOP"
class CmdConf(ExpConf): 
    def __init__(self):    
        self["env"] = Env()
        self["sto"] = Sto()
        super().__init__()
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
            super().eval()

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
class DecConf(CmdConf):
    def __init__(self):
        self["locs"] = []
        super().__init__()
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
        self.pushVal({x:l})
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
        self.pushVal(l.copy())
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
        s = {k:v for k,v in s.items() if k not in ls}
        self["sto"] = s
        del ls
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
            super().eval()

# Test
dc = DecConf()
fac = Loop(Not(Eq(Id("y"), Num(0.0))), 
        CSeq(Assign(Id("x"), Mul(Id("x"), Id("y"))),
            Assign(Id("y"), Sub(Id("y"), Num(1.0)))))
dec = DSeq(Bind(Id("x"), Ref(Num(1.0))), 
           Bind(Id("y"), Ref(Num(20000.0))))
fac_blk = Blk(dec, fac)
dc.pushCnt(fac_blk)
print(dc)
while not dc.emptyCnt():
    dc.eval()
    print(dc)
    
