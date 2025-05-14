from cse110A_ast import *
from typing import Callable,List,Tuple,Optional
from scanner import Lexeme,Token,Scanner
import re
# Extra classes:

# Keeps track of the type of an ID,
# i.e. whether it is a program variable
# or an IO variable
class IDType(Enum):
    IO = 1
    VAR = 2

# The data to be stored for each ID in the symbol table
class SymbolTableData:
    def __init__(self, id_type: IDType, data_type: Type, new_name: str) -> None:
        self.id_type = id_type      # if the variable is input/output
                                    # or variable
                                    
        self.data_type = data_type  # if the variable is an int or
                                    # float
                                    
        self.new_name = new_name    # a new name to resolve collisions
                                    # in scoping

    # Getters for each of the elements
    def get_id_type(self) -> IDType:
        return self.id_type

    def get_data_type(self) -> Type:
        return self.data_type

    def get_new_name(self) -> str:
        return self.new_name

# Symbol Table exception, requires a line number and ID
class SymbolTableException(Exception):
    def __init__(self, lineno: int, ID: str) -> None:
        message = "Symbol table error on line: " + str(lineno) + "\nUndeclared ID: " + str(ID)
        super().__init__(message)

# Generates a new label when needed
class NewLabelGenerator():
    def __init__(self) -> None:
        self.counter = 0
        
    def mk_new_label(self) -> str:
        new_label = "label" + str(self.counter)
        self.counter += 1
        return new_label

# Generates a new name (e.g. for program variables)
# when needed
class NewNameGenerator():
    def __init__(self) -> None:
        self.counter = 0
        self.new_names = []

    # You may want to make a better renaming scheme
    def mk_new_name(self) -> str:
        new_name = "_new_name" + str(self.counter)
        self.counter += 1
        self.new_names.append(new_name)
        return new_name
    
# Allocates virtual registers
class VRAllocator():
    def __init__(self) -> None:
        self.counter = 0
        
    def mk_new_vr(self) -> str:
        vr = "vr" + str(self.counter)
        self.counter += 1
        return vr

    # get variable declarations (needed for the C++ wrapper)
    def declare_variables(self) -> List[str]:
        ret = []
        for i in range(self.counter):
            ret.append("virtual_reg vr%d;" % i)

        return ret

# Symbol table class
class SymbolTable:
    def __init__(self) -> None:
        # stack of hashtables
        self.ht_stack = [dict()]

    def insert(self, ID: str, id_type: IDType, data_type: Type, nng : Optional[NewNameGenerator] = None) -> None:
                
        if id_type == IDType.VAR:
            new_name = nng.mk_new_name()
        else:
            new_name = ID

        info = SymbolTableData(id_type, data_type, new_name)  
        self.ht_stack[-1][ID] = info        


    # Lookup the symbol. If it is there, return the
    # info, otherwise return Noney
    def lookup(self, ID: str) -> Optional:
        for ht in reversed(self.ht_stack):
            if ID in ht:
                return ht[ID]
        return None

    def push_scope(self) -> None:
        self.ht_stack.append(dict())

    def pop_scope(self) -> None:
        self.ht_stack.pop()

# Parser Exception
class ParserException(Exception):
    
    # Pass a line number, current lexeme, and what tokens are expected
    def __init__(self, lineno: int, lexeme: Lexeme, tokens: List[Token]) -> None:
        message = "Parser error on line: " + str(lineno) + "\nExpected one of: " + str(tokens) + "\nGot: " + str(lexeme)
        super().__init__(message)

# Parser class
class Parser:

    # Creating the parser requires a scanner
    def __init__(self, scanner: Scanner) -> None:
        
        self.scanner = scanner

        # Create a symbol table
        self.symbol_table = SymbolTable()

        # objects to create virtual registers,
        # labels, and new names
        self.vra = VRAllocator()
        self.nlg = NewLabelGenerator()
        self.nng = NewNameGenerator()

        self.function_name = None
        self.function_args = []

    # Do post order traversal of node and allocate vrs to every node in the tree
    def allocate_vrs(self, node:ASTNode) -> None:
        if is_leaf_node(node) and node.vr == None:
            node.vr = self.vra.mk_new_vr()
        elif is_binop_node(node):
            self.allocate_vrs(node.l_child)
            self.allocate_vrs(node.r_child)

            node.vr = self.vra.mk_new_vr()
        elif is_unop_node(node):
            self.allocate_vrs(node.child)

            node.vr = self.vra.mk_new_vr()


    def parse(self, s: str, uf: int) -> List[str]:

        # Set the scanner and get the first token
        self.scanner.input_string(s)
        self.to_match = self.scanner.token()
        self.uf = uf
        # start parsing. In your solution, p must contain a list of
        # three address instructions
        p = self.parse_function()
        self.eat(None)
        
        return p

    # Helper fuction: get the token ID
    def get_token_id(self, l: Lexeme) ->Token:
        if l is None:
            return None
        return l.token

    # Helper fuction: eat a token ID and advance
    # to the next token
    def eat(self, check: Token) -> None:
        token_id = self.get_token_id(self.to_match)
        if token_id != check:
            raise ParserException(self.scanner.get_lineno(),
                                  self.to_match,
                                  [check])      
        self.to_match = self.scanner.token()

    # The top level parse_function
    def parse_function(self) -> List[str]:

        # I am parsing the function header for you
        # You do not need to do anything with this.
        self.parse_function_header()    
        self.eat(Token.LBRACE)

        # your solution should have p containing a list
        # of three address instructions
        p = self.parse_statement_list()        
        self.eat(Token.RBRACE)
        return p

    # You do not need to modify this for your homework
    # but you can look :) 
    def parse_function_header(self) -> None:
        self.eat(Token.VOID)
        function_name = self.to_match.value
        self.eat(Token.ID)        
        self.eat(Token.LPAR)
        self.function_name = function_name
        args = self.parse_arg_list()
        self.function_args = args
        self.eat(Token.RPAR)

    # You do not need to modify this for your homework
    # but you can look :) 
    def parse_arg_list(self) -> List[Tuple[str, str]]:
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.RPAR:
            return
        arg = self.parse_arg()
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.RPAR:
            return [arg]
        self.eat(Token.COMMA)
        arg_l = self.parse_arg_list()
        return arg_l + [arg]

    # You do not need to modify this for your homework
    # but you can look :) 
    def parse_arg(self) -> Tuple[str, str]:
        token_id = self.get_token_id(self.to_match)
        if token_id == Token.FLOAT:
            self.eat(Token.FLOAT)
            data_type = Type.FLOAT
            data_type_str = "float"            
        elif token_id == Token.INT:
            self.eat(Token.INT)
            data_type = Type.INT
            data_type_str = "int"
        else:
            raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.INT, Token.FLOAT])
        self.eat(Token.AMP)
	# change strings and indexing token.names .value .token
        id_name = self.to_match.value
        self.eat(Token.ID)

        # storing an IO variable to the symbol table
        self.symbol_table.insert(id_name, IDType.IO, data_type)
        return (id_name, data_type_str)
        
    # The top level parsing function for your homework
    # This function needs to return a list of three address codes
    def parse_statement_list(self) -> List[str]:    
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT, Token.FLOAT, Token.ID, Token.IF, Token.LBRACE, Token.FOR]:
            a = self.parse_statement()
            b = self.parse_statement_list()
            return a + b
        if token_id in [Token.RBRACE]:
            return []
        
    # you need to return a list of three address instructions
    # from the statement that gets parsed
    def parse_statement(self) -> List[str]:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT, Token.FLOAT]:
            return self.parse_declaration_statement()
        elif token_id in [Token.ID]:
            return self.parse_assignment_statement()
        elif token_id in [Token.IF]:
            return self.parse_if_else_statement()
        elif token_id in [Token.LBRACE]:
            return self.parse_block_statement()
        elif token_id in [Token.FOR]:
            return self.parse_for_statement()
        else:
            raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.FOR, Token.IF, Token.LBRACE, Token.INT, Token.FLOAT, Token.ID])

    # you need to return a list of three address instructions
    def parse_declaration_statement(self) -> List[str]:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.INT]:
            self.eat(Token.INT)
            id_name = self.to_match.value
            # Think about what you want to insert into the symbol table
            # self.symbol_table.insert(...)
            self.eat(Token.ID)
            self.eat(Token.SEMI)
            data_type = Type.INT
            self.symbol_table.insert(id_name, IDType.VAR, data_type, self.nng)
            return []
        if token_id in [Token.FLOAT]:
            self.eat(Token.FLOAT)
            id_name = self.to_match.value
            # Think about what you want to insert into the symbol table
            # self.symbol_table.insert(...)
            self.eat(Token.ID)

            data_type = Type.FLOAT
            self.symbol_table.insert(id_name, IDType.VAR, data_type, self.nng)
            self.eat(Token.SEMI)
            return []
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.INT, Token.FLOAT])

    # you need to return a list of three address instructions
    def parse_assignment_statement(self) -> List[str]:
        i = self.parse_assignment_statement_base()
        self.eat(Token.SEMI)
        return i;

    # you need to return a list of three address instructions
    def parse_assignment_statement_base(self) -> List[str]:
        id_name = self.to_match.value
        id_data = self.symbol_table.lookup(id_name)
        if id_data == None:
            raise SymbolTableException(self.scanner.get_lineno(), id_name)
        self.eat(Token.ID)
        self.eat(Token.ASSIGN)
        expr_ast = self.parse_expr()
        type_inference(expr_ast)
        if id_data.data_type == Type.INT and expr_ast.node_type == Type.FLOAT:
            new_root = ASTFloatToIntNode(expr_ast)
            new_root.node_type = Type.INT
            expr_ast = new_root
        elif id_data.data_type == Type.FLOAT and expr_ast.node_type == Type.INT:
            new_root = ASTIntToFloatNode(expr_ast)
            new_root.node_type = Type.FLOAT
            expr_ast = new_root

        self.allocate_vrs(expr_ast)
        program = expr_ast.linearize_code()

        if id_data.id_type == IDType.IO:
            if id_data.data_type == Type.INT:
                assignment_instruction = ["%s = vr2int(%s);" % (id_name, expr_ast.vr)]
            else:
                assignment_instruction = ["%s = vr2float(%s);" % (id_name, expr_ast.vr)]
        else:
            assignment_instruction = ["%s = %s;" % (id_data.new_name, expr_ast.vr)]
        return program + assignment_instruction

    # you need to return a list of three address instructions
    def parse_if_else_statement(self) -> List[str]:
        self.eat(Token.IF)
        self.eat(Token.LPAR)
        expr_ast = self.parse_expr()
        type_inference(expr_ast)
        self.allocate_vrs(expr_ast)
        expr_program = expr_ast.linearize_code()

        else_label = self.nlg.mk_new_label()
        end_label = self.nlg.mk_new_label()

        zero_vr = self.vra.mk_new_vr() # VrX in the slides

        compare_ins = ["%s = int2vr(0);" % (zero_vr), "beq(%s, %s, %s);" % (expr_ast.vr, zero_vr, else_label)]
        branch_ins = ["branch(%s);" % (end_label)]


        self.eat(Token.RPAR)
        if_program = self.parse_statement()
        self.eat(Token.ELSE)
        else_program = self.parse_statement()
        return expr_program + compare_ins + if_program + branch_ins + ["%s:" % (else_label)] + else_program + ["%s:" % (end_label)]
    
    # you need to return a list of three address instructions
    def parse_block_statement(self) -> List[str]:
        self.eat(Token.LBRACE)
        self.symbol_table.push_scope()
        ret = self.parse_statement_list()
        self.symbol_table.pop_scope()
        self.eat(Token.RBRACE)
        return ret

    # you need to return a list of three address instructions
    def parse_for_statement(self) -> List[str]:
        self.eat(Token.FOR)
        self.eat(Token.LPAR)
        original_assignment_program = self.parse_assignment_statement()
        expr_ast = self.parse_expr()
        type_inference(expr_ast)
        self.allocate_vrs(expr_ast)
        expr_program = expr_ast.linearize_code() 

        self.eat(Token.SEMI)
        loop_end_assignment_program = self.parse_assignment_statement_base()
        self.eat(Token.RPAR)
        loop_program = self.parse_statement()
        print(f'//expr_program: {expr_program}')
        print(f'//original_assignment_program: {original_assignment_program}')
        print(f'//loop_end_assignment_program: {loop_end_assignment_program}')
        
        loop_start_label = self.nlg.mk_new_label()
        end_label = self.nlg.mk_new_label()
        zero_vr = self.vra.mk_new_vr()

        compare_ins = ["%s = int2vr(0);" % (zero_vr), "beq(%s, %s, %s);" % (expr_ast.vr, zero_vr, end_label)]  # Branch out if expression == 0
        branch_ins = ["branch(%s);" % (loop_start_label)]  # Instruction to branch back to the start of the loop (right before evaluating the expression again)

        pattern = r'\((.*?)\)'
        replacement = '(' + str(self.uf) + ')'
        iter = re.search(pattern, expr_program[0]).group(1)
        print(f'//val: {iter}')


        # assume it's valid, screw the conditions for now
        if self.uf != None and self.uf != 1:
            print(f'// uf: {self.uf}')
            print(f'//loop_end_assignment_program[0]: {loop_end_assignment_program[0]}')
            result = re.sub(pattern, replacement, loop_end_assignment_program[0])
            print('//' + result)
            loop_program *= self.uf
            loop_end_assignment_program[0] = result
            return original_assignment_program + ["%s:" % (loop_start_label)] + expr_program + compare_ins + loop_program + loop_end_assignment_program + branch_ins + ["%s:" % (end_label)]
        else:
            return original_assignment_program + ["%s:" % (loop_start_label)] + expr_program + compare_ins + loop_program + loop_end_assignment_program + branch_ins + ["%s:" % (end_label)]

    # you need to build and return an AST
    def parse_expr(self) -> ASTNode:
        node = self.parse_comp()
        ret = self.parse_expr2(node)
        return ret

    # you need to build and return an AST
    def parse_expr2(self, lhs_node: ASTNode) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.EQ]:
            self.eat(Token.EQ)
            rhs_node = self.parse_comp()
            n = ASTEqNode(lhs_node, rhs_node)
            return self.parse_expr2(n)
        
        if token_id in [Token.SEMI, Token.RPAR]:
            return lhs_node
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR])
    
    # you need to build and return an AST
    def parse_comp(self) -> ASTNode:
        node = self.parse_factor()
        ret = self.parse_comp2(node)
        return ret

    # you need to build and return an AST
    def parse_comp2(self, lhs_node: ASTNode) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.LT]:
            self.eat(Token.LT)
            rhs_node = self.parse_factor()
            ret = ASTLtNode(lhs_node, rhs_node)
            return self.parse_comp2(ret)
        if token_id in [Token.SEMI, Token.RPAR, Token.EQ]:
            return lhs_node
        
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT])

    # you need to build and return an AST
    def parse_factor(self) -> ASTNode:
        node = self.parse_term()
        ret = self.parse_factor2(node)
        return ret

    # you need to build and return an AST
    def parse_factor2(self, lhs_node:ASTNode) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.PLUS]:
            self.eat(Token.PLUS)
            rhs_node = self.parse_term()
            ret = ASTPlusNode(lhs_node, rhs_node)    
            ret = self.parse_factor2(ret)
            return ret
        if token_id in [Token.MINUS]:
            self.eat(Token.MINUS)
            rhs_node = self.parse_term()
            ret = ASTMinusNode(lhs_node, rhs_node)    
            ret = self.parse_factor2(ret)
            return ret
        if token_id in [Token.EQ, Token.SEMI, Token.RPAR, Token.LT]:
            return lhs_node

        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS])
    
    # you need to build and return an AST
    def parse_term(self) -> ASTNode:
        node = self.parse_unit()
        ret = self.parse_term2(node)
        return ret

    # you need to build and return an AST
    def parse_term2(self, lhs_node:ASTNode) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.DIV]:
            self.eat(Token.DIV)
            rhs_node = self.parse_unit()
            ret = ASTDivNode(lhs_node, rhs_node)
            ret = self.parse_term2(ret)
            return ret
        
        if token_id in [Token.MUL]:            
            self.eat(Token.MUL)
            rhs_node = self.parse_unit()
            ret = ASTMultNode(lhs_node, rhs_node)
            ret = self.parse_term2(ret)
            return ret
        
        if token_id in [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS]:
            return lhs_node

        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.EQ, Token.SEMI, Token.RPAR, Token.LT, Token.PLUS, Token.MINUS, Token.MUL, Token.DIV])


    # you need to build and return an AST
    def parse_unit(self) -> ASTNode:
        token_id = self.get_token_id(self.to_match)
        if token_id in [Token.NUM]:
            value = self.to_match.value
            node = ASTNumNode(value)
            self.eat(Token.NUM)            
            return node
        if token_id in [Token.ID]:
            id_name = self.to_match.value
            id_data = self.symbol_table.lookup(id_name)
            if id_data == None:
                raise SymbolTableException(self.scanner.get_lineno(), id_name)
            self.eat(Token.ID)

            if (id_data.id_type == IDType.IO):
                node = ASTIOIDNode(id_name, id_data.data_type)
            # For Program Variable
            else:
                node = ASTVarIDNode(id_data.new_name, id_data.data_type)

            return node
        if token_id in [Token.LPAR]:
            self.eat(Token.LPAR)
            ret = self.parse_expr()
            self.eat(Token.RPAR)
            return ret
            
        raise ParserException(self.scanner.get_lineno(),
                              self.to_match,            
                              [Token.NUM, Token.ID, Token.LPAR])    

# Type inference start
def is_leaf_node(node: ASTNode) -> bool:
    return issubclass(type(node), ASTLeafNode)

def is_binop_node(node: ASTNode) -> bool:
    return issubclass(type(node), ASTBinOpNode)

def is_unop_node(node: ASTNode) -> bool:
    return issubclass(type(node), ASTUnOpNode)

def convert_children_type(node: ASTNode) -> None:
    if node.l_child.node_type == Type.INT and node.r_child.node_type == Type.FLOAT:
        conv = ASTIntToFloatNode(node.l_child)
        type_inference(conv)
        node.l_child = conv
    elif node.l_child.node_type == Type.FLOAT and node.r_child.node_type == Type.INT:
        conv = ASTIntToFloatNode(node.r_child)
        type_inference(conv)
        node.r_child = conv

# Type inference top level
def type_inference(node: ASTNode) -> Type:
    
    if is_leaf_node(node):
        return node.node_type

    elif is_binop_node(node):
        # do type inference on children
        type_inference(node.l_child)
        type_inference(node.r_child)

        # do inference for arithmetic operators
        if type(node) in [ASTPlusNode, ASTMinusNode, ASTMultNode, ASTDivNode]:
            # if either child is float type, we become a float too.
            if node.l_child.node_type == Type.FLOAT or node.r_child.node_type == Type.FLOAT:
                node.node_type = Type.FLOAT
            # otherwise, both children are int types. we become an int.
            else:
                node.node_type = Type.INT

            convert_children_type(node)
            
        # types for Eq and Lt Nodes already set in ast.py
        elif type(node) in [ASTEqNode, ASTLtNode]:
            # node_type is always INT
            node.node_type = Type.INT

            # convert types of children
            convert_children_type(node)

    elif is_unop_node(node):
        # do type inference on children
        # type_inference(node.child) # NOTE: Should not be necessary. child node should definitely already have a type
        
        # Set our node_type and check child type
        if type(node) in [ASTIntToFloatNode]:
            node.node_type = Type.FLOAT

            # Make sure chlid is right type
            assert(node.child.node_type == Type.INT)
            
        elif type(node) in [ASTFloatToIntNode]:
            node.node_type = Type.INT

            # Make sure chlid is right type
            assert(node.child.node_type == Type.FLOAT)
    