from srcs.parser.tokens.unary_operator_token import UnaryOperatorToken
from srcs.parser.tokens.binary_operator_token import BinaryOperatorToken
from srcs.parser.tokens.rational_number_token import RationalNumberToken
from srcs.parser.tokens.complex_number_token import ComplexNumberToken
from srcs.parser.tokens.name_token import NameToken
from srcs.parser.tokens.name_definition_token import NameDefinitionToken
from srcs.parser.tokens.open_bracket_token import OpenBracketToken
from srcs.parser.tokens.close_bracket_token import CloseBracketToken
from srcs.parser.tokens.function_definition_token import FunctionDefinitionToken
from srcs.parser.tokens.function_call_token import FunctionCallToken
from srcs.parser.tokens.question_token import QuestionToken
from srcs.parser.tokens.equal_token import EqualToken
from srcs.parser.tokens.comma_token import CommaToken

from srcs.ast.nodes.branches.binary_operation_node import BinaryOperationNode
from srcs.ast.nodes.branches.anonymous_node import AnonymousNode

from srcs.errors import InternalSyntaxError


class AbstractSyntaxTree:
    def __init__(self, tokens):
        self.tokens = tokens
        self.nodes = self.build_ast(tokens)

    def __repr__(self):
        return f'{type(self).__name__}({self.nodes})'

    def build_ast(self, tokens):
        stack = []
        index = 0

        nodes = self.create_anonymous_nodes(tokens)

    def create_anonymous_nodes(self, tokens):
        stack = []

        for token in tokens:
            if isinstance(token, CloseBracketToken):
                buffer = []
                flag = False
                temp_token = token
                while stack:
                    temp_token = stack.pop()
                    if isinstance(temp_token, OpenBracketToken):
                        flag = True
                        break
                    else:
                        buffer.append(temp_token)
                if not flag:
                    raise InternalSyntaxError('extra closing parenthesis', temp_token)
                buffer.reverse()
                buffer = self.create_anonymous_nodes(buffer)
                node = AnonymousNode(buffer)
                stack.append(node)
            else:
                stack.append(token)

        open_index = None
        #print(tokens, '===>>', stack)
        for index, token in enumerate(stack):
            if isinstance(token, OpenBracketToken):
                open_index = index
        if open_index is not None:
            raise InternalSyntaxError('extra opening parenthesis', stack[open_index])

        return stack
