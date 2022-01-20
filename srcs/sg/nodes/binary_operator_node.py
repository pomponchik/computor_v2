from srcs.sg.nodes.abstract_node import AbstractGraphNode
from srcs.sg.nodes.name_definition_node import NameDefinitionGraphNode
from srcs.sg.nodes.function_call_node import FunctionCallGraphNode
from srcs.sg.nodes.function_definition_node import FunctionDefinitionGraphNode

from srcs.errors import RuntimeASTError


class BinaryOperationGraphNode(AbstractGraphNode):
    def calculate(self, context):
        if self.sign == '=':
            if isinstance(self.left_operand, NameDefinitionGraphNode):
                result = self.right_operand.calculate(context)
                context[self.ast_node.tokens[0].tokens[0].source] = result
                return result
            elif isinstance(self.left_operand, FunctionDefinitionGraphNode):
                result = self.left_operand.calculate(context, self.right_operand.ast_node)
                context[result.name] = result
                return result
            else:
                print('LEFT:', self.left_operand)
                raise RuntimeASTError('to the left of the assignment operation should be the name', self)

        else:
            left = self.left_operand.calculate(context)
            right = self.right_operand.calculate(context)

            return left.operation(right, self.sign, self)

    def fill_data(self, ast_node, creator):
        self.sign = ast_node.tokens[1].source
        self.left_operand = creator(ast_node.tokens[0], ast_node)
        self.right_operand = creator(ast_node.tokens[2], ast_node)
