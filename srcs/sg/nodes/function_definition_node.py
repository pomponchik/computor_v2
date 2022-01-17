from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.function_object import FunctionObject

from srcs.errors import RuntimeASTError


class FunctionDefinitionGraphNode(AbstractGraphNode):
    def calculate(self, context, body):
        return FunctionObject.create_from_node(self, body)
