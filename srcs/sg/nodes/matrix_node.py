from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.matrix_object import MatrixObject


class MatrixGraphNode(AbstractGraphNode):
    def calculate(self, context):
        return MatrixObject.create_from_node(self, context)
