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

    def compileSum(self, node):
        pass
    def compileSub(self, node):
        pass
    def compileMul(self, node):
        pass
    def compileEq(self, node):
        pass
    def compileNot(self, node):
        pass








