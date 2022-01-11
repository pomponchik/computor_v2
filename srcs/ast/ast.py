from srcs.parser.tokens.unary_operator_token import UnaryOperatorToken
from srcs.parser.tokens.binary_operator_token import BinaryOperatorToken
from srcs.parser.tokens.rational_number_token import RationalNumberToken
from srcs.parser.tokens.complex_number_token import ComplexNumberToken
from srcs.parser.tokens.name_token import NameToken
from srcs.parser.tokens.open_bracket_token import OpenBracketToken
from srcs.parser.tokens.close_bracket_token import CloseBracketToken
from srcs.parser.tokens.function_definition_token import FunctionDefinitionToken
from srcs.parser.tokens.question_token import QuestionToken
from srcs.parser.tokens.equal_token import EqualToken
from srcs.parser.tokens.comma_token import CommaToken
from srcs.parser.tokens.square_open_bracket_token import SquareOpenBracketToken
from srcs.parser.tokens.square_close_bracket_token import SquareCloseBracketToken

from srcs.ast.nodes.abstract_node import AbstractNode
from srcs.ast.nodes.branches.abstract_branche_node import AbstractBrancheNode
from srcs.ast.nodes.leaves.abstract_leave_node import AbstractLeaveNode

from srcs.ast.nodes.branches.binary_operation_node import BinaryOperationNode
from srcs.ast.nodes.branches.bracked_node import BrackedNode
from srcs.ast.nodes.branches.vector_node import VectorNode
from srcs.ast.nodes.branches.question_node import QuestionNode
from srcs.ast.nodes.branches.function_call_node import FunctionCallNode

from srcs.ast.nodes.leaves.complex_number_node import ComplexNumberNode
from srcs.ast.nodes.leaves.name_node import NameNode
from srcs.ast.nodes.leaves.rational_number_node import RationalNumberNode

from srcs.errors import InternalSyntaxError
from srcs.errors import ASTError

from srcs.lexer.lexemes.other_lexeme import OtherLexeme


class AbstractSyntaxTree:
    def __init__(self, tokens):
        self.tokens = tokens
        self.nodes = self.build_ast(tokens)

    def __repr__(self):
        return f'{type(self).__name__}({self.nodes})'

    def build_ast(self, tokens):
        nodes = self.create_leaves_nodes(tokens)
        nodes = self.create_bracked_nodes(nodes, OpenBracketToken, CloseBracketToken, BrackedNode)
        nodes = self.create_bracked_nodes(nodes, SquareOpenBracketToken, SquareCloseBracketToken, VectorNode)
        nodes = self.create_binary_operators_nodes(nodes, ['^', '*', '**', '/', '%', '+', '-'])
        nodes = self.create_question_node(nodes)

        nodes = self.create_implicit_multiple_operators_nodes(nodes)
        print('before',nodes)
        nodes = self.merge_functions_nodes(nodes)
        nodes = self.create_binary_operators_nodes(nodes, ['='])
        print('after',nodes)
        nodes = self.kill_bracked_nodes(nodes)
        self.check_double_questions(nodes)
        return nodes

    def merge_functions_nodes(self, nodes):
        if not nodes or len(nodes) == 1:
            return nodes

        result = []
        index = 1
        previous_node = nodes[0]
        result.append(previous_node)

        while index < len(nodes):
            node = nodes[index]

            if isinstance(node, BrackedNode) and isinstance(previous_node, NameNode):
                node = FunctionCallNode([previous_node, node])
                result.pop()

            result.append(node)

            previous_node = node
            index += 1

        return result

    def kill_bracked_nodes(self, nodes):
        result = []

        for node in nodes:
            while isinstance(node, BrackedNode):
                tokens = node.tokens
                if len(tokens) > 1:
                    raise ASTError('ambiguous operation', node)
                elif len(tokens) == 0:
                    raise ASTError('missing operation', node)
                node = tokens[0]
            if isinstance(node, AbstractBrancheNode):
                node.tokens = self.kill_bracked_nodes(node.tokens)
            result.append(node)

        return result

    def create_implicit_multiple_operators_nodes(self, nodes):
        if len(nodes) == 1:
            return nodes
        result = []
        index = 0
        flag = False
        while index < (len(nodes) - 1):
            flag = False
            node = nodes[index]
            next_node = nodes[index + 1]

            if isinstance(node, RationalNumberNode) and isinstance(next_node, NameNode):
                result.append(BinaryOperationNode([node, BinaryOperatorToken([OtherLexeme('*', 0, '*', 0)], 'o[*]'), next_node]))
                flag = True
                index += 1
            else:
                result.append(node)

            index += 1

        if not flag:
            result.append(nodes[-1])

        for node in nodes:
            if isinstance(node, AbstractNode):
                node.tokens = self.create_implicit_multiple_operators_nodes(node.tokens)

        return result

    def check_double_questions(self, nodes):
        for node in nodes:
            if isinstance(node, QuestionToken):
                raise InternalSyntaxError('the question is not at the root of the expression', node)
            elif isinstance(node, AbstractNode):
                self.check_double_questions(node.tokens)

    def create_question_node(self, nodes):
        if len(nodes) > 0 and isinstance(nodes[-1], QuestionToken):
            return [QuestionNode(nodes[:-1])]
        return nodes

    def create_binary_operators_nodes(self, nodes, operators):
        for operator in operators:
            nodes = self.create_binary_operator_nodes(nodes, operator)
        return nodes

    def create_binary_operator_nodes(self, nodes, operator):
        result = []
        index = 0

        while index < len(nodes):
            node = nodes[index]

            if isinstance(node, AbstractNode):
                node.tokens = self.create_binary_operator_nodes(node.tokens, operator)
            else:
                if node.source == operator:
                    if not result:
                        raise InternalSyntaxError('the first operand in the expression is missing', node)
                    if index == (len(nodes) - 1):
                        raise InternalSyntaxError('the second operand is missing in the expression', node)
                    first_operand = result.pop()
                    operator_of_expression = node
                    second_operand = nodes[index + 1]
                    if not isinstance(second_operand, AbstractNode):
                        raise InternalSyntaxError('invalid operand in the expression', second_operand)
                    second_operand.tokens = self.create_binary_operator_nodes(second_operand.tokens, operator)
                    node = BinaryOperationNode([first_operand, operator_of_expression, second_operand])
                    index += 1
            result.append(node)
            index += 1

        return result

    def create_leaves_nodes(self, tokens):
        result = []

        for token in tokens:
            if isinstance(token, ComplexNumberToken):
                token = ComplexNumberNode([token])
            elif isinstance(token, RationalNumberToken):
                token = RationalNumberNode([token])
            elif isinstance(token, NameToken):
                token = NameNode([token])
            result.append(token)

        return result

    def create_bracked_nodes(self, tokens, open_bracket_class, close_bracket_class, container_class):
        stack = []

        for token in tokens:
            if isinstance(token, close_bracket_class):
                buffer = []
                flag = False
                while stack:
                    temp_token = stack.pop()
                    if isinstance(temp_token, open_bracket_class):
                        flag = True
                        break
                    else:
                        buffer.append(temp_token)
                if not flag:
                    if isinstance(token, AbstractNode):
                        raise ASTError('extra closing parenthesis', token)
                    raise InternalSyntaxError('extra closing parenthesis', token)
                buffer.reverse()
                buffer = self.create_bracked_nodes(buffer, open_bracket_class, close_bracket_class, container_class)
                node = container_class(buffer)
                stack.append(node)
            elif isinstance(token, AbstractBrancheNode):
                token.tokens = self.create_bracked_nodes(token.tokens, open_bracket_class, close_bracket_class, container_class)
                stack.append(token)
            else:
                stack.append(token)

        open_index = None
        for index, token in enumerate(stack):
            if isinstance(token, open_bracket_class):
                open_index = index
        if open_index is not None:
            if isinstance(stack[open_index], AbstractNode):
                raise ASTError('extra closing parenthesis', stack[open_index])
            raise InternalSyntaxError('extra opening parenthesis', stack[open_index])

        return stack
