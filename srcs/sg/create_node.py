from srcs.ast.nodes.branches.binary_operation_node import BinaryOperationNode as ASTBinaryOperationNode
from srcs.ast.nodes.branches.vector_node import VectorNode as ASTVectorNode
from srcs.ast.nodes.branches.question_node import QuestionNode as ASTQuestionNode
from srcs.ast.nodes.branches.function_call_node import FunctionCallNode as ASTFunctionCallNode

from srcs.ast.nodes.leaves.complex_number_node import ComplexNumberNode as ASTComplexNumberNode
from srcs.ast.nodes.leaves.name_node import NameNode as ASTNameNode
from srcs.ast.nodes.leaves.rational_number_node import RationalNumberNode as ASTRationalNumberNode


from srcs.sg.nodes.binary_operator_node import BinaryOperationGraphNode
from srcs.sg.nodes.complex_number_node import ComplexNumberGraphNode
from srcs.sg.nodes.equation_node import EquationGraphNode
from srcs.sg.nodes.function_call_node import FunctionCallGraphNode
from srcs.sg.nodes.function_definition_node import FunctionDefinitionGraphNode
from srcs.sg.nodes.matrix_node import MatrixGraphNode
from srcs.sg.nodes.name_definition_node import NameDefinitionGraphNode
from srcs.sg.nodes.name_load_node import NameLoadGraphNode
from srcs.sg.nodes.output_node import OutputGraphNode
from srcs.sg.nodes.rational_number_node import RationalNumberGraphNode
from srcs.sg.nodes.vector_node import VectorGraphNode

from srcs.errors import ASTError


def create_node(node, parent_node):
    if isinstance(parent_node, ASTQuestionNode) and isinstance(node, ASTBinaryOperationNode) and node.tokens[1].source == '=':
        return EquationGraphNode(node, create_node)
    elif isinstance(node, ASTQuestionNode):
        if len(node.tokens) != 1:
            raise ASTError('ambiguous question body', node)
        return create_node(node.tokens[0], node)
    elif isinstance(node, ASTComplexNumberNode):
        return ComplexNumberGraphNode(node, create_node)
    elif isinstance(node, ASTRationalNumberNode):
        return RationalNumberGraphNode(node, create_node)
    elif isinstance(node, ASTNameNode):
        if isinstance(parent_node, ASTBinaryOperationNode) and parent_node.tokens[1].source == '=' and parent_node.tokens[0] is node:
            return NameDefinitionGraphNode(node, create_node)
        else:
            return NameLoadGraphNode(node, create_node)
    elif isinstance(node, ASTVectorNode) and isinstance(parent_node, ASTVectorNode):
        return VectorGraphNode(node, create_node)
    elif isinstance(node, ASTVectorNode):
        return MatrixGraphNode(node, create_node)
    elif isinstance(node, ASTFunctionCallNode):
        if isinstance(parent_node, ASTBinaryOperationNode) and parent_node.tokens[1].source == '=':
            return FunctionDefinitionGraphNode(node, create_node)
        return FunctionCallGraphNode(node, create_node)
    elif isinstance(node, ASTBinaryOperationNode):
        return BinaryOperationGraphNode(node, create_node)
    raise ASTError('operation not defined', node)
