from srcs.sg.objects.abstract_object import AbstractObject

from srcs.sg.objects.rational_number_object import RationalNumberObject

from srcs.errors import RuntimeASTError


class ComplexNumberObject(AbstractObject):
    type_mark = 'c'

    def __init__(self, node, real_part, imaginary_part):
        self.real_part = int(real_part) if int(real_part) == real_part else real_part
        self.imaginary_part = int(imaginary_part) if int(imaginary_part) == imaginary_part else imaginary_part
        self.node = node

    @classmethod
    def create_from_node(cls, node):
        source = node.ast_node.tokens[0].source.replace(' ', '').replace('\t', '')

        if source == 'i':
            source = '0+1' + source

        if '-' not in source and '+' not in source:
            source = '0+' + source

        real_part, imaginary_part, imaginary_multiplier = cls.split_source(source)
        imaginary_part = imaginary_part.replace('*', '').replace('i', '').strip()

        real_number = float(real_part) if '.' in real_part else int(real_part)
        imaginary_number = float(imaginary_part) if '.' in imaginary_part else int(imaginary_part)

        imaginary_number *= imaginary_multiplier

        return cls.create(real_number, imaginary_number, node)

    @classmethod
    def create(cls, real_number, imaginary_number, node):
        if not imaginary_number:
            return RationalNumberObject(real_number, node)
        return cls(node, real_number, imaginary_number)

    @staticmethod
    def split_source(source):
        splitted_by_minus = source.split('-')
        is_minus = (len(splitted_by_minus) == 2)
        splitted = splitted_by_minus if is_minus else source.split('+')
        index_real, index_imaginary = (0, 1) if 'i' in splitted[1] else (1, 0)
        return splitted[index_real], splitted[index_imaginary], -1 if is_minus else 1

    def representation(self):
        if self.real_part:
            return f'{self.real_part} + {self.imaginary_part}i'
        return f'{self.imaginary_part}i'

    def type_representation(self):
        return 'complex number'

    def real_operation(self, other, operation, operation_node):
        if other.type_mark == self.type_mark:
            if operation == '+':
                new_real_part = self.real_part + other.real_part
                new_imaginary_part = self.imaginary_part + other.imaginary_part
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '-':
                new_real_part = self.real_part - other.real_part
                new_imaginary_part = self.imaginary_part - other.imaginary_part
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '*':
                new_real_part = self.real_part * other.real_part - self.imaginary_part * other.imaginary_part
                new_imaginary_part = self.real_part * other.imaginary_part + self.imaginary_part * other.real_part
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '/':
                try:
                    x1 = self.real_part
                    y1 = self.imaginary_part
                    x2 = other.real_part
                    y2 = other.imaginary_part

                    new_real_part = (x1 * x2 + y1 * y2) / (x2 ** 2 + y2 ** 2)
                    new_imaginary_part = (y1 * x2 - x1 * y2) / (x2 ** 2 + y2 ** 2)

                    return self.create(new_real_part, new_imaginary_part, self.node)
                except ZeroDivisionError:
                    raise RuntimeASTError('division by 0', other.node)
        elif other.type_mark == 'r':
            if operation == '*':
                new_real_part = self.real_part * other.number
                new_imaginary_part = self.imaginary_part * other.number
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '^':
                if other.is_real_number:
                    raise RuntimeASTError('not a whole degree', other.node)
                if other.number < 0:
                    raise RuntimeASTError('the exponent is less than zero', other.node)
                if other.number == 0:
                    return type(other)(1, self.node)
                if other.number == 1:
                    return self
                else:
                    multiplier = self
                    result = self
                    degree = other.number
                    while degree - 1:
                        result = result.real_operation(multiplier, '*', self.node)
                        degree -= 1
                    return result

            elif operation == '/':
                if other.number == 0:
                    raise RuntimeASTError('division by 0', other.node)
                new_real_part = self.real_part / other.number
                new_imaginary_part = self.imaginary_part / other.number
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '+':
                new_real_part = self.real_part + other.number
                new_imaginary_part = self.imaginary_part
                return self.create(new_real_part, new_imaginary_part, self.node)
            elif operation == '-':
                new_real_part = self.real_part - other.number
                new_imaginary_part = self.imaginary_part
                return self.create(new_real_part, new_imaginary_part, self.node)

        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)
