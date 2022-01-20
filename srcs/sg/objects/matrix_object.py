from srcs.sg.objects.abstract_object import AbstractObject

from srcs.errors import RuntimeASTError

from srcs.parser.tokens.comma_token import CommaToken
from srcs.parser.tokens.semicolon_token import SemicolonToken
from srcs.ast.nodes.branches.vector_node import VectorNode as ASTVectorNode

from srcs.sg.objects.rational_number_object import RationalNumberObject


class MatrixObject(AbstractObject):
    type_mark = 'm'

    def __init__(self, node, vectors):
        self.node = node
        self.vectors = vectors
        self.check_size(vectors)
        self.height = len(vectors)
        self.width = 0 if not self.height else len(vectors[0])
        self.shape = (self.height, self.width)

    def get_column(self, index):
        if index < 0 or index >= self.width:
            raise KeyError(f'impossible column index: {index}')

        result = []

        for vector in self.vectors:
            result.append(vector[index])

        return result

    def get_line(self, index):
        if index < 0 or index >= self.height:
            raise KeyError(f'impossible column index: {index}')

        return self.vectors[index]

    @staticmethod
    def activate_vectors(vectors, context):
        result = []

        for vector in vectors:
            new_vector = []
            for element in vector:
                element = element.calculate(context)
                if not element.type_mark == 'r':
                    raise RuntimeASTError('the elements of the matrix can only be rational numbers', self.node)
                new_vector.append(element)
            result.append(new_vector)

        return result

    def check_size(self, vectors):
        if not len(vectors):
            return

        first_vector_size = len(vectors[0])

        for vector in vectors:
            if len(vector) != first_vector_size:
                raise RuntimeASTError('the length of the vectors in the matrix is not the same', self.node)

    @classmethod
    def create_from_node(cls, node, context):
        source_vectors = cls.create_sequence(node.ast_node.tokens, lambda x: isinstance(x, SemicolonToken), lambda x: isinstance(x, ASTVectorNode), lambda x: node.creator(x, node.ast_node), node)
        vectors = []
        for source_vector in source_vectors:
            tokens = cls.create_sequence(source_vector.ast_node.tokens, lambda x: isinstance(x, CommaToken), lambda x: True, lambda x: node.creator(x, source_vector), node)
            vectors.append(tokens)
        return MatrixObject(node, cls.activate_vectors(vectors, context))

    @classmethod
    def create_unit_matrix(cls, node, size):
        vectors = []

        for index in range(size):
            vector = []
            for index_2 in range(size):
                if index == index_2:
                    vector.append(RationalNumberObject(1))
                else:
                    vector.append(RationalNumberObject(0))
            vectors.append(vector)

        return cls(node, vectors)

    @staticmethod
    def create_sequence(tokens, is_separator, is_element, create_element, node):
        result = []

        for index, token in enumerate(tokens):
            if index % 2 == 0:
                if not is_element(token):
                    raise RuntimeASTError(f'incorrect matrix description format', node)
                element = create_element(token)
                result.append(element)
            else:
                if not is_separator(token):
                    raise RuntimeASTError(f'incorrect matrix description format', node)

        return result

    def representation(self):
        strings = []

        for vector in self.vectors:
            string = []
            for number in vector:
                string.append(f' {number.representation()} ')
            string = ','.join(string)
            string = f'[{string}]'
            strings.append(string)

        return '\n'.join(strings)


    def type_representation(self):
        return 'matrix'

    def real_operation(self, other, operation, operation_node):
        if other.type_mark == self.type_mark:
            if operation == '+':
                if self.shape != other.shape:
                    raise RuntimeASTError('the shape of the matrices is different', operation_node)
                new_vectors = []
                for vector_1, vector_2 in zip(self.vectors, other.vectors):
                    new_vector = []
                    for element_1, element_2 in zip(vector_1, vector_2):
                        new_vector.append(element_1.real_operation(element_2, '+', operation_node))
                    new_vectors.append(new_vector)
                return MatrixObject(operation_node, new_vectors)
            elif operation == '-':
                if self.shape != other.shape:
                    raise RuntimeASTError('the shape of the matrices is different', operation_node)
                new_vectors = []
                for vector_1, vector_2 in zip(self.vectors, other.vectors):
                    new_vector = []
                    for element_1, element_2 in zip(vector_1, vector_2):
                        new_vector.append(element_1.real_operation(element_2, '-', operation_node))
                    new_vectors.append(new_vector)
                return MatrixObject(operation_node, new_vectors)
            elif operation == '**':
                if self.width != other.height:
                    raise RuntimeASTError('matrix multiplication is possible only if the width of the first matrix is equal to the height of the second matrix', other.node)
                return self.multiplication(self, other, self.node)
        if other.type_mark == 'r':
            if operation == '*':
                new_vectors = []
                for vector in self.vectors:
                    new_vector = []
                    for element in vector:
                        new_vector.append(element.real_operation(other, '*', operation_node))
                    new_vectors.append(new_vector)
                return MatrixObject(operation_node, new_vectors)
            elif operation == '^':
                if other.is_real_number:
                    raise RuntimeASTError('not a whole degree', other.node)
                if other.number < 0:
                    raise RuntimeASTError('the exponent is less than zero', other.node)
                if not (self.height == self.width):
                    raise RuntimeASTError('exponentiation is possible only for a square matrix', other.node)
                if other.number == 0:
                    return self.create_unit_matrix(self.node, self.height)
                else:
                    multiplier = self
                    result = self
                    degree = other.number
                    while degree - 1:
                        result = result.real_operation(multiplier, '**', self.node)
                        degree -= 1
                    return result
            elif operation == '/':
                new_vectors = []
                for vector in self.vectors:
                    new_vector = []
                    for element in vector:
                        new_vector.append(element.real_operation(other, '/', operation_node))
                    new_vectors.append(new_vector)
                return MatrixObject(operation_node, new_vectors)

        raise RuntimeASTError(f'the "{operation}" operation between {self.type_representation()} and {other.type_representation()} is not defined', operation_node)

    @staticmethod
    def multiplication(first, second, node):
        result = []

        for index_1 in range(first.height):
            vector = []
            for index_2 in range(second.width):
                vector_1 = first.get_line(index_1)
                vector_2 = second.get_column(index_2)

                value = RationalNumberObject(0, node)

                for value_1, value_2 in zip(vector_1, vector_2):
                    mult = value_1.real_operation(value_2, '*', node)
                    value = value.real_operation(mult, '+', node)

                vector.append(value)

            result.append(vector)

        return MatrixObject(node, result)
