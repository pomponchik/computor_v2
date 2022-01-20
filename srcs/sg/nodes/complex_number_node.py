from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.complex_number_object import ComplexNumberObject

from srcs.errors import RuntimeASTError


class ComplexNumberGraphNode(AbstractGraphNode):
    def calculate(self, context):
        return ComplexNumberObject.create_from_node(self)

    def fill_data(self, ast_node, creator):
        pass
