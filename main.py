import argparse
from scanner import Scanner, tokens, Lexeme, Token
from cse110A_parser import Parser
from ir_compiler import IRCompiler

if __name__ == "__main__":

    # this is the command line parser, not the C-simple parser
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--local_value_numbering', '-lvn', action='store_true')
    parser.add_argument('--unroll_factor', '-uf', type=int)
    args = parser.parse_args()
    if args.unroll_factor is None:
        args.unroll_factor = 1
    if args.local_value_numbering is None:
        args.local_value_numbering = False

    #args = parser.parse_args()

    # get the program string
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    # create the scanner and make a token action for
    # tracking the line number
    s = Scanner()
    def track_lineno(l: Lexeme) -> Lexeme:
        if l.value == "\n":
            s.lineno += 1
        return l
    tokens = tokens + [(Token.IGNORE, " |\n|\t", track_lineno)]
    s.set_tokens(tokens)

    # create the parser with the scanner
    p = Parser(s)

    # create the IRCompiler with the parser
    compiler = IRCompiler(p)

    # compile the program into IR
    compiler.compile2ir(f_contents,args.local_value_numbering, args.unroll_factor)

    # print the IR
    print(compiler.ir_program)
