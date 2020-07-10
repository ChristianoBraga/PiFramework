import unittest
import tatsu
from impiler import Impiler

class TestImpToPiIR(unittest.TestCase):
    def setUp(self):
        imp_grammar_h = open('imp2.ebnf')
        imp_grammar = imp_grammar_h.read()
        imp_grammar_h.close()
        self.parser = tatsu.compile(imp_grammar)

    def __test_parse(self, file_name, ast):
        source_h = open(file_name)
        source = source_h.read()
        source_h.close()
        pi_ast = self.parser.parse(source, semantics=Impiler())
        self.assertEqual(str(pi_ast), ast)

    def test_cmd_parse0(self):
        self.__test_parse('examples/cmd-test0.imp2', "Blk(DSeq(Bind(Id(x), Ref(Num(10))), Bind(Id(y), Ref(Num(10)))), Loop(Gt(Id(x), Num(0)), Blk(CSeq(Assign(Id(y), Mul(Id(y), Id(x))), Assign(Id(x), Sub(Id(x), Num(1)))))))")

    def test_cmd_parse1(self):
        self.__test_parse('examples/cmd-test1.imp2',"Blk(DSeq(DSeq(Bind(Id(x), Ref(Num(1))), Bind(Id(y), Ref(Num(1)))), Bind(Id(z), Ref(Num(1)))), CSeq(CSeq(CSeq(Assign(Id(x), Num(0)), Assign(Id(y), Num(1))), Assign(Id(z), Num(3))), Cond(Lt(Id(x), Num(2)), Blk(Assign(Id(z), Num(3))), Nop())))")
        
if __name__ == '__main__':
    unittest.main()
