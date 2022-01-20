from srcs.sg.objects.abstract_object import AbstractObject

from srcs.errors import RuntimeASTError


class EquationResultObject(AbstractObject):
    type_mark = 'e'

    def __init__(self, node):
        raise NotImplementedError('operation not defined')

    @classmethod
    def create_from_node(cls, node):
        raise NotImplementedError('operation not defined')

    def representation(self, context):
        raise NotImplementedError('operation not defined')

    def type_representation(self):
        return 'equation result'

    def real_operation(self, other, operation, operation_node):
        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)
