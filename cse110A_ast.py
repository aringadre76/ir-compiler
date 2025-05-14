from enum import Enum
from typing import Callable,List,Tuple,Optional

# enum for data types in ClassIeR
class Type(Enum):
    INT = 1
    FLOAT = 2

# base class for an AST node. Each node
# has a type and a VR
class ASTNode():
    def __init__(self) -> None:
        self.node_type = None
        self.vr = None

# AST leaf nodes
class ASTLeafNode(ASTNode):
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__()

    def __str__(self, level=""):
        ret = f"{level[:-3]}{'|_ '* bool(level)}<{self.value}, {self.node_type}, {self.vr}>\n"
        return ret

    def get_op(self) -> str:
        if self.node_type == Type.INT:
            return "int2vr"
        else:
            return "float2vr"
        
    def three_addr_code(self) -> str:
        return "%s = %s(%s);" % (self.vr, self.get_op(), self.value)
    
    def linearize_code(self) -> List[str]:
        return [self.three_addr_code()]

######
# A number leaf node

# The value passed in should be a number as a string.
######
class ASTNumNode(ASTLeafNode):
    def __init__(self, value: str) -> None:        
        super().__init__(value)

            # check if "." in value. If so: float, otherwise: int.
        if '.' in value:
            self.node_type = Type.FLOAT
        else:
            self.node_type = Type.INT


######
# A program variable leaf node

# The value passed in should be an id name
# eventually it should be the new name generated
# by the symbol table to handle scopes.

######
class ASTVarIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type
        self.vr = value

    def three_addr_code(self) -> str:
        assert(0)

    def linearize_code(self) -> List[str]:
        return []
    
######
# An IO leaf node

# The value passed in should be an id name.
# Because it is an IO node, you do not need
# to get a new name for it.

# When you create this node, you will also need
# to provide its data type. It is recorded in
# the symbol table
######
class ASTIOIDNode(ASTLeafNode):
    def __init__(self, value: str, value_type) -> None:
        super().__init__(value)
        self.node_type = value_type

######
# Binary operation AST Nodes

# These nodes require their left and right children to be
# provided on creation
######
class ASTBinOpNode(ASTNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) -> None:
        self.l_child = l_child
        self.r_child = r_child
        super().__init__()

    def __str__(self, level="") -> str:
        ret = f"{level[:-3]}{'|_ ' * bool(level)}<{self.__class__.__name__}, {self.node_type}, {self.vr}>\n"
        children = [self.l_child, self.r_child]
        for more, child in enumerate(children, 1 - len(children)):
            childIndent = "|  " if more else "   "
            ret += child.__str__(level + childIndent)
        return ret
    
    def three_addr_code(self) -> str:
        return "%s = %s(%s,%s);" % (self.vr, self.get_op(), self.l_child.vr, self.r_child.vr)
    
    def linearize_code(self) -> List[str]:
        return self.l_child.linearize_code() + self.r_child.linearize_code() + [self.three_addr_code()]


class ASTPlusNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) -> None:
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        if self.node_type == Type.INT:
            return "addi"
        else:
            return "addf"


class ASTMultNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) -> None:
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        if self.node_type == Type.INT:
            return "multi"
        else:
            return "multf"


class ASTMinusNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) -> None:
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        if self.node_type == Type.INT:
            return "subi"
        else:
            return "subf"


class ASTDivNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) ->None:
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        if self.node_type == Type.INT:
            return "divi"
        else:
            return "divf"

######
# Special BinOp nodes for comparisons

# These operations always return an int value
# (as an untyped register):
# 0 for false and 1 for true.

# Because of this, their node type is always
# an int. However, the operations (eq and lt)
# still need to be typed depending
# on their inputs. If their children are floats
# then you need to use eqf, ltf, etc.
######
class ASTEqNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) ->None:
        self.node_type = Type.INT
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        # Since our type is ALWAYS INT, check type of either child instead.
        if self.l_child.node_type == Type.INT:
            return "eqi"
        else:
            return "eqf"


class ASTLtNode(ASTBinOpNode):
    def __init__(self, l_child: ASTNode, r_child: ASTNode) -> None:
        self.node_type = Type.INT
        super().__init__(l_child,r_child)

    def get_op(self) -> str:
        # Since our type is ALWAYS INT, check type of either child instead.
        if self.l_child.node_type == Type.INT:
            return "lti"
        else:
            return "ltf"


######
# Unary operation AST Nodes

# The only operations here are converting
# the bits in a virtual register to another
# virtual register of a different type,
# i.e. corresponding to the CLASSIeR instructions:
# vr_int2float and vr_float2int
######
class ASTUnOpNode(ASTNode):
    def __init__(self, child: ASTNode) -> None:
        self.child = child
        super().__init__()

    def __str__(self, level="") -> str:
        ret = f"{level[:-3]}{'|_ ' * bool(level)}<{self.__class__.__name__}, {self.node_type}, {self.vr}>\n"
        ret += self.child.__str__(level + "   ")
        return ret
    
    def three_addr_code(self) -> str:
        return "%s = %s(%s);" % (self.vr, self.get_op(), self.child.vr)
    
    def linearize_code(self) -> List[str]:
        return self.child.linearize_code() + [self.three_addr_code()]

        
class ASTIntToFloatNode(ASTUnOpNode):
    def __init__(self, child: ASTNode) -> None:
        super().__init__(child)

    def get_op(self) -> str:
        return "vr_int2float"


class ASTFloatToIntNode(ASTUnOpNode):
    def __init__(self, child: ASTNode) -> None:
        super().__init__(child)

    def get_op(self) -> str:
        return "vr_float2int"

