GRAMMAR = '''
@@grammar::IMP

start =  @:cmd $ ;

cmd = let | assign | loop ;

loop = op:'while' ~ e:expression 'do' { c:cmd }+ ;

assign = id:identifier op:':=' ~ e:expression ;

let = op:'let' ~ d:dec 'in' { c:cmd }+ ; 

dec = op:'var' ~ id:identifier '=' e:expression ;

expression = @:bool_expression ;

bool_expression = negation | equality | conjunction | disjunction 
                | lowereq | greatereq | lowerthan | greaterthan 
                | add_expression ;

equality = left:add_expression op:"==" ~ right:bool_expression ;

conjunction = left:add_expression op:"and" ~ right:bool_expression ;

disjunction = left:add_expression op:"or" ~ right:bool_expression ;

lowereq = left:add_expression op:"<=" ~ right:add_expression ;

greatereq = left:add_expression op:">=" ~ right:add_expression ;

lowerthan = left:add_expression op:"<" ~ right:add_expression ;

greaterthan = left:add_expression op:">" ~ right:add_expression ;

parentesisexp = '(' ~ @:bool_expression ')' ;

negation = op:'not' ~ b:bool_expression ;

add_expression = addition | subtraction | @:mult_expression ;

addition = left:mult_expression op:"+" ~ right:add_expression ;

subtraction = left:mult_expression op:"-" ~ right:add_expression ;

mult_expression = multiplication | division 
                | atom 
                | parentesisexp ;

multiplication = left:atom op:"*" ~ right:mult_expression ;

division = left:atom op:"/" ~ right:mult_expression ;

atom = number | truth | identifier ;
 
number = /\d+/ ;

identifier = /(?!\d)\w+/ ;

truth = 'True' | 'False' ;
'''

from tatsu.ast import AST
import pi

class Impiler(object):
    def identifier(self, ast):
        return pi.Id(str(ast))

    def number(self, ast):
        return pi.Num(int(ast))

    def addition(self, ast):
        return pi.Sum(ast.left, ast.right)

    def subtraction(self, ast):
        return pi.Sub(ast.left, ast.right)

    def multiplication(self, ast):
        return pi.Mul(ast.left, ast.right)

    def division(self, ast):
        return pi.Div(ast.left, ast.right)

    def truth(self, ast):
        return pi.Boo(bool(ast))

    def negation(self, ast):
        return pi.Not(ast.b)    

    def equality(self, ast):
        return pi.Eq(ast.left, ast.right)

    def lowerthan(self,ast):
        return pi.Lt(ast.left, ast.right)

    def greaterthan(self,ast):
        return pi.Gt(ast.left, ast.right)

    def lowereq(self,ast):
        return pi.Le(ast.left, ast.right)

    def greatereq(self,ast):
        return pi.Ge(ast.left, ast.right)

    def conjunction(self, ast):
        return pi.And(ast.left, ast.right)

    def disjunction(self, ast):
        return pi.Or(ast.left, ast.right)

    def assign(self, ast):
        return pi.Assign(ast.id, ast.e)

    def dec(self, ast):
        return pi.Bind(ast.id, pi.Ref(ast.e))

    def let(self, ast):
        if isinstance(ast.c, pi.Cmd):
            return pi.Blk(ast.d, ast.c)
        else:
            cmd = ast.c[0]
            for i in range(1, len(ast.c)):
                cmd = pi.CSeq(cmd, ast.c[i])
            return pi.Blk(ast.d, cmd)

    def loop(self, ast):
        if isinstance(ast.c, pi.Cmd):
            return pi.Loop(ast.e, ast.c)
        else:
            cmd = ast.c[0]
            for i in range(1, len(ast.c)):
                cmd = pi.CSeq(cmd, ast.c[i])
            return pi.Loop(ast.e, cmd)

if __name__ == '__main__':
    import tatsu
    # grammar = open('calc.ebnf').read()
    # parser = tatsu.compile(grammar)
    parser = tatsu.compile(GRAMMAR)
    # source = "xyzn < 1" 
    # source = '2 * 3 + 5 / 4'
    # source = '( not ( (2 * 3 + 5) < (2 + 3) ) ) or (0 < 1)'
    # source = '(xyz + 1) > 0'
    
    source = \
    ''' 
    let var z = 1 
    in 
        let var y = 1000 
        in 
            while not (y == 0)
            do 
                z := z * y
                y := y - 1'''
    
    print('Imπ source code: \n', source, '\n')

    try:
        ast = parser.parse(source)
        print('AST: ', ast)
        print()
    except Exception as e:
        print('Parser error: ' + str(e))
        exit()

    try:
        pi_ast = parser.parse(source, semantics=Impiler())
        print('π lib AST:', pi_ast)
        print()
    except Exception as e:
        print('Compilation error: ' + str(e))
        exit()

    try:
        (tr, ns, dt) = pi.run(pi_ast)
    except Exception as e:
        print('Evaluation error: ', e)
        exit()

    print('State #'+ str(len(tr) - 2) + ' of the π automaton:')
    print(tr[len(tr) - 2])
    print('Number of evaluation steps:', ns)
    print('Execution time:', dt)
