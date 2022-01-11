from srcs.sg.objects.abstract_object import AbstractObject

from srcs.errors import RuntimeASTError


class RationalNumberObject(AbstractObject):
    type_mark = 'r'

    def __init__(self, number, node):
        self.number = int(number) if int(number) == number else number
        self.node = node

    @classmethod
    def create_from_node(cls, node):
        source = node.ast_node.tokens[0].source.replace(' ', '')
        number = float(source) if '.' in source else int(source)
        return cls(number, node)

    def representation(self):
        return f'{self.number}'

    def type_representation(self):
        return 'rational number'

    def operation(self, other, operation, operation_node):
        if other.type_mark == self.type_mark:
            if operation == '+':
                number = self.number + other.number
                return RationalNumberObject(number, self.node)
            elif operation == '*':
                number = self.number * other.number
                return RationalNumberObject(number, self.node)
            elif operation == '/':
                if other.number == 0:
                    raise RuntimeASTError('division by 0', other.node)
                number = self.number / other.number
                return RationalNumberObject(number, self.node)
            elif operation == '-':
                number = self.number - other.number
                return RationalNumberObject(number, self.node)
            elif operation == '^':
                if type(other.number) is float:
                    raise RuntimeASTError('not a whole degree', other.node)
                if other.number < 0:
                    raise RuntimeASTError('the exponent is less than zero', other.node)
                number = (self.number)**(other.number)
                return RationalNumberObject(number, self.node)

        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)
