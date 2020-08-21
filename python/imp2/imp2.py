# Author: Christiano Braga
# http://github.com/ChristianoBraga

import tatsu                            # Tatsu is the parser generator.
from impiler import Impiler             # Impiler is the compiler from Imπ to π IR.
from pi import run, EvaluationError     # pi is the Python implementation of the Π framework
import sys, traceback, getopt           # System and command line modules.
from pillvm import pi_llvm, pi_llvm_jit 
import pprint
from termcolor import colored

def print_help():
    print(colored('Imπ2 to Π IR compiler and interpreter, August 2020', 'green'))
    print(colored('http://github.com/ChristianoBraga/PiFramework', 'grey'))
    print(colored('imp2.py -f <impfile>' + 
                  '[-s | -a | -d | -p | -t | ' +
                  '--at | --pt | --stats | --state n | --last n | ' +
                  '--out | --no-color | --llvm | --llvm_jit]',
                  'yellow'))
    print('-s : Prints source code.')
    print('-a : Prints syntax tree.')
    print('-d : Prints parse trace.')    
    print('-p : Prints Π IR abstract syntax tree.')
    print('-t : Prints full Π automaton evaluation trace.')
    print('-b : Prints full Π automaton evaluation backtrace.')    
    print('--at : Prints the syntax tree and terminates.')
    print('--pt : Prints Π IR abstract syntax tree and terminates.')
    print('--td : Prints Π automaton evaluation backtrace on error.')    
    print('--stats : Prints execution statistics.')
    print('--state n : Prints the nth state of the trace.')
    print('--last n : Prints the (last - n)th state of the trace.')
    print('--out : Prints the oputput.')
    print('--no-color : Do not print colors in trace.')
    print('--llvm : Prints LLVM code.')
    print('--llvm_jit : Runs LLVM JIT code.')
    print(colored('Make sure you are in an ANSI terminal.', 'red'))

def main(argv):    
    source = ''    
    print_ast = False
    print_parse_trace = False
    print_trace_debug = False    
    print_pilib_ast = False
    print_source = False
    print_trace = False
    print_backtrace = False
    print_stats = False
    print_state = False
    print_last = False
    print_out = False
    color = True
    print_llvm = False
    run_llvm_jit = False
    terminate = False
    display_state = 0
    last_n_state = 0
    try:
        opts, args = getopt.getopt(argv,"f:saptb", ['at', 'pt', 'td', 'llvm', 'llvm_jit', 'stats', 'state=', 'last=', 'out', 'no-color'])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-f':
            source = open(arg).read()
        elif opt == '-s':
            print_source = True
        elif opt == '-a':
            print_ast = True
        elif opt == '-d':
            print_parse_trace = True
        elif opt == '-p':
            print_pilib_ast = True
        elif opt == '-t':
            print_trace = True
        elif opt == '-b':
            print_backtrace = True
        elif opt == '--at':
            print_ast = True
            terminate = True
        elif opt == '--pt':
            print_pilib_ast = True
            terminate = True
        elif opt == '--td':
            print_trace_debug = True
        elif opt == '--stats':
            print_stats = True
        elif opt == '--state':
            print_state = True
            display_state = int(arg)
        elif opt == '--last':
            print_last = True
            last_n_state = int(arg)
        elif opt == '--out':
            print_out = True
        elif opt == '--no-color':
            color= False
        elif opt == '--llvm':
            print_llvm = True
        elif opt == '--llvm_jit':
            run_llvm_jit = True

    if color:
        pi_symb = colored('Π', 'green')
    else:
        pi_symb = 'Π'
            
    if not source:
        print_help()
        exit(2)

    if print_source:
        print('Imπ source code: ')
        print(source)

    imp_grammar = open('imp2.ebnf').read()
    
    if print_parse_trace:
        parser = tatsu.compile(imp_grammar, trace=True, colorize=True)
    else:
        parser = tatsu.compile(imp_grammar)

    if print_ast:
        try:
            ast = parser.parse(source)
            print(ast)
            print('Concrete syntax tree: ')            
            pprint.pprint(ast, indent=2, width=20)
            if terminate:
                exit(1)
            print()
        except Exception as e:
            print('Parse error: ' + str(e))
            exit(2)

    try:
        pi_ast = parser.parse(source, semantics=Impiler())
        if print_pilib_ast:            
            print(pi_symb + ' IR syntax tree:')            
            pprint.pprint(pi_ast,indent=2, width=20)
            print()
        if terminate:
            exit(1)
        
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('Imπ compilation error: ')
        tbl = traceback.format_exception(exc_type, exc_value, exc_traceback)
        imp_tb = [e for e in tbl if 'PiFramework' in e]
        for ex in imp_tb:
            print(ex)
        print(exc_value)
        exit(2)

    try:
        (tr, ns, o, dt) = run(pi_ast, color=color)
    except EvaluationError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if color:
            msg = colored(str(exc_value.args[0]), 'red')
        else:
            msg = str(exc_value.args[0])
        print('Imπ evaluation error: ' + msg)
        if print_trace_debug:
            print(pi_symb + " automaton backtrace so far:")
            state_number = len(e.trace) - 1
            for state in reversed(e.trace):
                if color:
                    csn = colored('#' + str(state_number), 'blue')
                else:
                    csn = '#' + str(state_number)
                print('State '+ csn + ' of the ' + pi_symb + ' automaton:')
                print(state)
                state_number = state_number - 1
        print('Python ' + pi_symb + ' automaton call trace:')
        tbl = traceback.format_exception(exc_type, exc_value, exc_traceback)
        imp_tb = [e for e in tbl if 'pi.py' in e or 'imp2.py' in e]
        for ex in imp_tb:
            print(ex)
        exit(2)

    if print_llvm or run_llvm_jit:
        module = pi_llvm(pi_ast)
        if print_llvm:
            print(module)
        if run_llvm_jit:
            pi_llvm_jit(module)
    else:
        if print_state:
            print('State #'+ str(display_state) + ' of the ' + pi_symb + ' automaton:')
            print(tr[display_state])
            exit(1)

        if print_trace:
            for state_number in range(len(tr)):
                if color:
                    print('State '+ colored('#'+ str(state_number), 'blue') + \
                          ' of the ' + pi_symb + ' automaton:')
                else:
                    print('State '+ '#'+ str(state_number) + \
                          ' of the ' + pi_symb + ' automaton:')
                print(tr[state_number])
        else:
            if print_backtrace:
                state_number = len(tr) - 1
                for state in reversed(tr):
                    if color:
                        csn = colored('#' + str(state_number), 'blue')
                    else:
                        csn = '#' + str(state_number)
                    print('State '+ csn + ' of the ' + pi_symb + ' automaton:')
                    print(state)
                    state_number = state_number - 1
                    print(tr[state_number])
            else:    
                if print_last:
                    display_state = len(tr) - (last_n_state + 1)
                    if color:
                        print('State '+ colored('#'+ str(display_state), 'blue') +
                              ' of the ' + pi_symb + ' automaton:')
                    else:
                        print('State '+ '#'+ str(display_state) +
                              ' of the ' + pi_symb + ' automaton:')
                    print(tr[display_state])
                #else:
                #    display_state = len(tr) - 1
                # if color:
                #    print('State '+ colored('#'+ str(display_state), 'blue') + \
                #                 ' of the ' + pi_symb + ' automaton:')
                # else:
                #    print('State '+ '#'+ str(display_state) + \
                #          ' of the ' + pi_symb + ' automaton:')
                # print(tr[display_state])

        if print_out:
            if o:
                print("Output = " + str(o))
            else:
                print("No output.")
            
        if print_stats:
            print('Number of evaluation steps:', ns)
            print('Evaluation time:', dt)       
    
if __name__ == '__main__':
    main(sys.argv[1:])
