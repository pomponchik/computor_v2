from srcs.sg.nodes.abstract_node import AbstractGraphNode

from srcs.sg.objects.equation_result import EquationResultObject

from srcs.errors import RuntimeASTError

class EquationGraphNode(AbstractGraphNode):
    def calculate(self, context):
        return EquationResultObject.create_from_node(self, context, self.creator)
