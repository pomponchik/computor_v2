class AbstractObject:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def create_from_node(cls, node):
        raise NotImplementedError('operation not defined')

    def representation(self):
        raise NotImplementedError('operation not defined')

    def type_representation(self):
        raise NotImplementedError('operation not defined')

    def operation(self, other, operation, operation_node):
        raise NotImplementedError('operation not defined')
