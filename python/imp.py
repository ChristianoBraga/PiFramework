
import tatsu                # Tatsu is the parser generator.
from impiler import Impiler # Impiler is the compiler from Imπ to π lib.
from pi import run          # pi is the Python implementation of the π framework
import sys, getopt          # System and command line modules.

def main(argv):    
    source = ''    
    print_ast = False
    print_pilib_ast = False
    print_source = False
    print_trace = False
    print_stats = False
    print_state = False
    print_last = False
    display_state = 0
    last_n_state = 0

    try:
        opts, args = getopt.getopt(argv,"f:sapte", ['state=', 'stats', 'last='])
    except getopt.GetoptError:
        print('imp.py -f <impfile> [-s | -a | -p | -t] ')
        print('-s : Prints source code.')
        print('-a : Prints syntax tree.')
        print('-p : Prints π lib abstract syntax tree.')
        print('-t : Prints full trace.')
        print('--stats : Prints execution statistics.')
        print('--state n : Prints the nth state of the automaton.')
        print('--last n : Prints the (last - n)th state of the automaton.')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-f':
            source = open(arg).read()
        elif opt == '-s':
            print_source = True
        elif opt == '-a':
            print_ast = True
        elif opt == '-p':
            print_pilib_ast = True
        elif opt == '-t':
            print_trace = True
        elif opt == '--stats':
            print_stats = True
        elif opt == '--state':
            print_state = True
            display_state = int(arg)
        elif opt == '--last':
            print_last = True
            last_n_state = int(arg)

    if print_source:
        print('Imπ source code: ')
        print(source)
        print()

    imp_grammar = open('imp.ebnf').read()
    parser = tatsu.compile(imp_grammar)

    if print_ast:
        try:
            ast = parser.parse(source)
            print('AST: ', ast)
            print()
        except Exception as e:
            print('Parser error: ' + str(e))
            exit()

    try:
        pi_ast = parser.parse(source, semantics=Impiler())
        if print_pilib_ast:
            print('π lib AST:', pi_ast)
            print()
    except Exception as e:
        print('Compilation error: ' + str(e))
        exit()

    try:
        (tr, ns, dt) = run(pi_ast)
    except Exception as e:
        print('Evaluation error: ', e)
        exit()

    if print_trace:
        for state_number in range(len(tr)):
            print('State #'+ str(state_number) + ' of the π automaton:')
            print(tr[state_number])
    else:
        if print_last:
            display_state = len(tr) - (last_n_state + 1)
        else:
            display_state = len(tr) - 1
        print('State #'+ str(display_state) + ' of the π automaton:')
        print(tr[display_state])

    if print_stats:
        print('Number of evaluation steps:', ns)
        print('Evaluation time:', dt)

if __name__ == '__main__':
    main(sys.argv[1:])
