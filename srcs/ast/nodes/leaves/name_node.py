from srcs.ast.nodes.leaves.abstract_leave_node import AbstractLeaveNode

from srcs.errors import InternalSyntaxError


class NameNode(AbstractLeaveNode):
    name = '6'

    def check_tokens(self, tokens):
        token  = tokens[0]

        if token.source.lower() == 'i':
            raise InternalSyntaxError('the name "i" is reserved for complex numbers', token)
