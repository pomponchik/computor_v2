from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.rational_number_object import RationalNumberObject

from srcs.errors import RuntimeASTError


class RationalNumberGraphNode(AbstractGraphNode):
    def calculate(self, context):
        return RationalNumberObject.create_from_node(self)
