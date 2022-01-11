from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.function_object import FunctionObject

from srcs.errors import RuntimeASTError


class NameLoadGraphNode(AbstractGraphNode):
    def calculate(self, context):
        result = context.get(self.name_content, None)
        if result is None:
            raise RuntimeASTError('nonexistent variable', self)
        if isinstance(result, FunctionObject):
            raise RuntimeASTError('the function is used as a variable', self)
        return result

    def fill_data(self, ast_node, creator):
        self.name_content = ast_node.tokens[0].source
