import llvmlite.ir as ir
import llvmlite.binding as llvm


class LLVMTypes:
    INT = ir.IntType(64)
    BOOL = ir.IntType(1)
    VOID = ir.VoidType()

class Node:
    opr = []
    def __init__(self):
        self.opr.append(ir.Constant(LLVMTypes.INT, 42))
        self.opr.append(ir.Constant(LLVMTypes.INT, 2))

class LLVMExp():
    def __init__(self, function):
        self.function = function
        self.block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)

    def compile(self, node):
        self.compileSum(node)
        print(self.function)

    def compileSum(self, node):
        lhs = node.opr[0]
        rhs = node.opr[1]
        self.builder.add(lhs, rhs)


    def compileSub(self, node):
        pass
    def compileMul(self, node):
        pass
    def compileEq(self, node):
        pass
    def compileNot(self, node):
        pass


module = ir.Module('main_module')
func_type = ir.FunctionType(LLVMTypes.INT, [], False)
lfunc = ir.Function(module, func_type, "main_function")

LLVMExp(lfunc).compile(Node())

print(module)









