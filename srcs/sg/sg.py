from srcs.sg.create_node import create_node

from srcs.errors import ASTError, InternalError


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
        FunctionCallNode - 8.

        ?
        > a + 2 = ?
        14
        > funA(2) + funB(4) = ?
        41
        > funC(3) = ?
        15
        > funA(x) = y ?
        x^2 + 2x + 1 = 0
        Une solution sur R :
        -1
        #> funA(funB(x)) = ?
        #4x^2 + 2 * x + 1
        """
        if len(ast.nodes) > 1:
            raise InternalError('the expression is ambiguous')
        elif len(ast.nodes) == 0:
            raise InternalError('empty expression')
        return create_node(ast.nodes[0], None)
