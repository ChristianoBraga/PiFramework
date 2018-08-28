import llvmlite.ir as ir
import llvmlite.binding as llvm


class LLVMTypes:
    INT = ir.IntType(64)
    BOOL = ir.IntType(1)
    VOID = ir.VoidType()


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

    def compileNum(self, node):
        return ir.Constant(LLVMTypes.INT, node.opr[0])

    def compileSum(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        return self.builder.add(lhs, rhs, "tmp_sum")

    def compileSub(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        return self.builder.sub(lhs, rhs, "tmp_sub")

    def compileMul(self, node):
        lhs = self.compile(node.opr[0])
        rhs = self.compile(node.opr[1])
        return  self.builder.mul(lhs, rhs, "tmp_mul")


module = ir.Module('main_module')
func_type = ir.FunctionType(LLVMTypes.INT, [], False)
func = ir.Function(module, func_type, "main_function")

llvm_exp = LLVMExp(func)
llvm_exp.builder.ret(llvm_exp.compile(Sum(Sum(Num(1), Num(10)), Num(2))))
print(module)

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