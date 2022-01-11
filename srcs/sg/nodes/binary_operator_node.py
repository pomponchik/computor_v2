from srcs.sg.nodes.abstract_node import AbstractGraphNode
from srcs.sg.nodes.name_definition_node import NameDefinitionGraphNode

from srcs.errors import RuntimeASTError


class BinaryOperationGraphNode(AbstractGraphNode):
    def calculate(self, context):
        if self.sign == '=':
            if not isinstance(self.left_operand, NameDefinitionGraphNode):
                raise RuntimeASTError('to the left of the assignment operation should be the name', self)
            result = self.right_operand.calculate(context)
            context[self.ast_node.tokens[0].tokens[0].source] = result
            return result
        else:
            left = self.left_operand.calculate(context)
            right = self.right_operand.calculate(context)

            return left.operation(right, self.sign, self)

    def fill_data(self, ast_node, creator):
        self.sign = ast_node.tokens[1].source
        self.left_operand = creator(ast_node.tokens[0], ast_node)
        self.right_operand = creator(ast_node.tokens[2], ast_node)
