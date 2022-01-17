from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.function_object import FunctionObject

from srcs.errors import RuntimeASTError


class FunctionCallGraphNode(AbstractGraphNode):
    def calculate(self, context):
        function = context.get(self.function_name, None)
        if function is None:
            raise RuntimeASTError(f'a function named {self.function_name} does not exist', self)
        if not isinstance(function, FunctionObject):
            raise RuntimeASTError(f'object "{function.representation()}" ({function.type_representation()}) is not a function.', self)

        argument = self.argument.calculate(context)

        return function.call(argument, context, self.creator)

    def fill_data(self, ast_node, creator):
        self.function_name = ast_node.tokens[0].tokens[0].source
        self.argument = creator(ast_node.tokens[1], ast_node)
