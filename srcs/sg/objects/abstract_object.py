from srcs.errors import RuntimeASTError


class AbstractObject:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def create_from_node(cls, node):
        raise NotImplementedError('operation not defined')

    def representation(self, context):
        raise NotImplementedError('operation not defined')

    def type_representation(self):
        raise NotImplementedError('operation not defined')

    def one_string_representation(self, context):
        return self.representation(context)

    def operation(self, other, operation, operation_node):
        if operation in ('*', '+', '**'):
            try:
                return self.real_operation(other, operation, operation_node)
            except RuntimeASTError as e:
                if not self.type_mark == 'm':
                    return other.real_operation(self, operation, operation_node)
                raise e
        else:
            return self.real_operation(other, operation, operation_node)

    def real_operation(self, other, operation, operation_node):
        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)
