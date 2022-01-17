from srcs.sg.objects.abstract_object import AbstractObject

from srcs.errors import RuntimeASTError


class EquationResultObject(AbstractObject):
    type_mark = 'e'

    def __init__(self, node):
        raise NotImplementedError('operation not defined')

    @classmethod
    def create_from_node(cls, node):
        raise NotImplementedError('operation not defined')

    def representation(self):
        raise NotImplementedError('operation not defined')

    def type_representation(self):
        return 'equation result'

    def operation(self, other, operation, operation_node):
        raise NotImplementedError('operation not defined')
