# Author: Fernando Mendes
# https://github.com/fjmendes1994

from pi import *
import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_void_p # For JIT support

class LLVMTypes:
    INT = ir.IntType(64)
    BOOL = ir.IntType(1)
    VOID = ir.VoidType()

class LLVMConstants:
    TRUE = ir.Constant(LLVMTypes.BOOL, 1)
    FALSE = ir.Constant(LLVMTypes.BOOL, 0)

# <codecell>
class LLVMExp():
    def __init__(self, function):
        self.function = function
        self.block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)

    def compileNum(self, node):
        return ir.Constant(LLVMTypes.INT, node.num())

    def compileSum(self, node):
        lhs = self.compile(node.left_operand())
        rhs = self.compile(node.right_operand())
        res = self.builder.add(lhs, rhs, "tmp_sum")
        return res

    def compileSub(self, node):
        lhs = self.compile(node.left_operand())
        rhs = self.compile(node.right_operand())
        res = self.builder.sub(lhs, rhs, "tmp_sub")
        return res

    def compileMul(self, node):
        lhs = self.compile(node.left_operand())
        rhs = self.compile(node.right_operand())
        res = self.builder.mul(lhs, rhs, "tmp_mul")
        return res

    def compileEq(self, node):
        lhs = self.compile(node.left_operand())
        rhs = self.compile(node.right_operand())
        res = self.builder.icmp_signed("==", lhs, rhs, "temp_eq")
        return res

    def compileNot(self, node):
        lhs = self.compile(node.operand(0))
        res = self.builder.not_(lhs, "temp_not")
        return res

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

# <codecell>
class LLVMCmd(LLVMExp):
    def __init__(self, function):
        self.env = {}
        LLVMExp.__init__(self, function)

    def addEnv(self, id, pointer):
        self.env[id].append(pointer)

    def getLoc(self, id):
        return self.env[id][-1]

    def compileAssign(self, node):
        id = self.compileAssingId(node.lvalue())
        val = self.compile(node.rvalue())
        return self.builder.store(val, id)

    def compileAssingId(self, node):
        id = node.id()
        if self.env[id]:
            ptr = self.getLoc(id)
        else:
            ptr = self.builder.alloca(LLVMTypes.INT, None, "ptr")
            self.addEnv(id, ptr)
        return ptr

    def compileId(self, node):
        id = node.id()
        ptr = self.getLoc(id)
        return self.builder.load(ptr, "val")

    def compileCSeq(self, node):
        self.compile(node.left_cmd())
        self.compile(node.right_cmd())

    def compileLoop(self, node):
        loop = self.builder.append_basic_block("loop")
        after_loop = self.builder.append_basic_block("after_loop")
        self.builder.branch(loop)
        with self.builder.goto_block(loop):
            cond = self.compile(node.cond())
            block = self.compile(node.body())
            self.builder.cbranch(cond, loop, after_loop)

        self.builder.position_at_start(after_loop)

    def compile(self, node):
        if isinstance(node, Assign):
            return self.compileAssign(node)
        elif isinstance(node, Id):
            return self.compileId(node)
        elif isinstance(node, CSeq):
            return self.compileCSeq(node)
        elif isinstance(node, Loop):
            return self.compileLoop(node)
        else:
            return LLVMExp.compile(self, node)

class LLVMDcl(LLVMCmd):
    def __init__(self, function):
        LLVMCmd.__init__(self, function)
        self.locs = []

    def cleanLocs(self):
        for loc in self.locs[-1]:
            if loc in self.env:
                self.env[loc].pop()
        self.locs.pop()

    def pushLoc(self, id):
        self.locs[-1].append(id)

    def compileRef(self, node):
        return self.compile(node.exp())

    def compileBind(self, node):
        id = self.compileBindId(node.id())
        ref = self.compile(node.bindable())
        return self.builder.store(ref, id)

    def compileBindId(self, node):
        id = node.id()
        self.pushLoc(id)
        if id in self.env:
            return self.compileAssingId(node)
        else:
            self.env[id] = []
            return self.compileAssingId(node)

    def compileDSeq(self, node):
        self.compile(node.left_dec())
        self.compile(node.right_dec())

    def compileBlk(self, node):
        self.locs.append([])
        dec = self.compile(node.dec())
        cmd = self.compile(node.cmd())
        self.compile(dec)
        self.compile(cmd)
        # print("LOCS = " + self.locs.__repr__())
        # print("ENV = " + self.env.__repr__())
        self.cleanLocs()

    def compile(self, node):
        if isinstance(node, Ref):
            return self.compileRef(node)
        elif isinstance(node, Bind):
            return self.compileBind(node)
        elif isinstance(node, DSeq):
            return self.compileDSeq(node)
        elif isinstance(node, Blk):
            return self.compileBlk(node)
        else:
            return LLVMCmd.compile(self, node)

# <codecell>
def pi_llvm(pi_ast):
    module = ir.Module('main_module')
    module.triple = llvm.get_default_triple()
    func_type = ir.FunctionType(LLVMTypes.INT, [], False)
    func = ir.Function(module, func_type, "main_function")

    llvm_compiler = LLVMDcl(func)

    llvm_compiler.compile(pi_ast)

    llvm_compiler.builder.ret(llvm_compiler.compile(Num(0)))

    return module

# <codecell>
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

def pi_llvm_jit(module):
    # All these initializations are required for code generation!
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()  # yes, even this one

    engine = create_execution_engine()
    mod = compile_ir(engine, str(module))

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("main_function")

    # Run the function via ctypes
    cfunc = CFUNCTYPE(c_void_p)(func_ptr)
    res = cfunc()
    print("main_function() =", res)