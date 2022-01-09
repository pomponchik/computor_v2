from srcs.ast.nodes.branches.binary_operation_node import BinaryOperationNode as ASTBinaryOperationNode
from srcs.ast.nodes.branches.bracked_node import BrackedNode as ASTBrackedNode
from srcs.ast.nodes.branches.vector_node import VectorNode as ASTVectorNode
from srcs.ast.nodes.branches.question_node import QuestionNode as ASTQuestionNode

from srcs.ast.nodes.leaves.complex_number_node import ComplexNumberNode as ASTComplexNumberNode
from srcs.ast.nodes.leaves.name_node import NameNode as ASTNameNode
from srcs.ast.nodes.leaves.rational_number_node import RationalNumberNode as ASTRationalNumberNode

from srcs.errors import ASTError, InternalError

from srcs.matcher.matcher import PatternMatcher


class SemanticGraph:
    def __init__(self, ast):
        #self.matcher = PatternMatcher(
        #    {
        #        ''
        #    },
        #    lambda x: x.name,
        #    lambda x: x,
        #)
        self.root = self.create_nodes(ast)

    def __repr__(self):
        return f'{type(self).__name__}({self.root})'

    def create_nodes(self, ast):
        """
        BinaryOperationNode - 1.
        BrackedNode - 2.
        QuestionNode - 3.
        VectorNode - 4.
        ComplexNumberNode - 5.
        NameNode - 6.
        RationalNumberNode - 7.
        """
        if len(ast.nodes) > 1:
            print('TOKENS:', ast.nodes)
            raise InternalError('the expression is ambiguous')
        elif len(ast.nodes) == 0:
            raise InternalError('empty expression')
        return self.create_nodes_dfs(ast.nodes[0], None)

    def create_nodes_dfs(self, node, parent_node):
        if isinstance(parent_node, ASTQuestionNode):
            pass
